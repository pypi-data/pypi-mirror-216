# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2020 ifm electronic gmbh
#
# THE PROGRAM IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.
#
import logging
import numpy as np
import cv2
from scipy import optimize
from o3r_algo_utilities.rotmat import rotMat, rotMatReverse

logger = logging.getLogger(__name__)

def find_transformation(world, imgpoints, invIC, fixed_translation, binning, camRefToOpticalSystem, optMode):
    '''
    Estimates a rotation r, and translation t such that
        inverse_intrinsic_projection(R.T*(world - t)) approx. imgpoints

    :param world: 3xn points in world coordinates
    :param imgpoints: 2xn points in image coordinates corresponding to world
    :param invIC: inverse intrinsic calibration
    :param fixed_translation: either a vector containing the fixed camera position or None
    :param binning: whether binning should be applied to the calibration
    :param camRefToOpticalSystem: internal transformation between head reference and optical system
    :param optMode: must be either "lsq" (use scipy least square optimization) or "min" (use scipy minimization)
    :return: r=[rotX, rotY, rotZ], t=[transX, transY, transZ], MSE
    '''
    assert world.shape[0] == 3, 'world must be 3xn, but is {}'.format(world.shape)
    assert imgpoints.shape[0] == 2, 'imgpoints must be 2xn, but is {}'.format(imgpoints.shape)
    assert imgpoints.shape[1] == world.shape[1], 'imgpoints and world must have the same number of points'

    def cost(rt, fixed_translation, world, imgpoints, mode):
        if fixed_translation is None:
            r, t = rt[:3], rt[3:]
        else:
            r, t = rt, fixed_translation
        world2cam = project(world, r, t, inverse=True)
        # z must be positive
        if np.any(world2cam[2, :] <= 0):
            logger.warning("z <= 0")
            nz = world2cam[2, world2cam[2, :] <= 0]
            return np.sum(nz ** 2) * 1e10
        cam = inverse_intrinsic_projection(world2cam, invIC, binning, camRefToOpticalSystem)
        if mode == "lsq":
            return np.linalg.norm(cam - imgpoints, axis=0)
        elif mode == "min":
            return np.mean(np.linalg.norm(cam - imgpoints, axis=0)**2)
        elif mode == "minabs":
            return np.mean(np.abs(np.linalg.norm(cam - imgpoints, axis=0)))
        raise RuntimeError("unknown mode %s" % mode)

    # find starting value
    r, t = PnP(world, imgpoints, invIC, binning)
    r = np.array(r)
    t = np.array(t)
    logger.debug("PnP result: r=%s t=%s", r, t)
    # optimize brute force
    if fixed_translation is None:
        x0 = np.array([r, t]).flatten()
    else:
        x0 = np.array(r).flatten()
        
    if optMode == "lsq":
        opt = optimize.least_squares(cost, x0, args=(fixed_translation, world, imgpoints, optMode))
        r = opt.x[:3]
        t = opt.x[3:] if fixed_translation is None else fixed_translation
        rms = np.sqrt(np.mean(opt.fun**2))
        rms_unit = "rms"
    elif optMode in ["min", "minabs"]:
        opt = optimize.minimize(cost, x0, args=(fixed_translation, world, imgpoints, optMode))
        r = opt.x[:3]
        t = opt.x[3:] if fixed_translation is None else fixed_translation
        if optMode == "min":
            rms = np.sqrt(opt.fun)
            rms_unit = "rms"
        else:
            rms = opt.fun
            rms_unit = "mae"

    assert np.all(project(world, r, t, inverse=True)[2, :] > 0), 'z values must be positive'
    return r, t, rms, rms_unit


def PnP(world, image, invIC, binning):
    """
    Calls cv2.solvePnP with all invIC parameters translated to openCV. The result can be used as 
    an initial estimate of the calibration
    
    :param world: 3xN world coordinates of the inner corners
    :param image: 2xN image coordinates of the inner corners
    :param invIC: inverse intrinsic calibration
    :param binning: flag indicating whether the image coordinates are binned
    :return: r=[rotX, rotY, rotZ], t=[transX, transY, transZ]
    """
    fb = 0.5 if binning else 1.0

    assert invIC["modelID"] in [1, 3]
    fx, fy, mx, my, alpha, k1, k2, k3, k4, k5 = invIC["modelParameters"][:10]

    cameraMatrix = np.array([
        [fx * fb, 0, mx * fb],
        [0, fy * fb, my * fb],
        [0, 0, 1],
    ])

    # opencv uses different variable names:
    # https://docs.opencv.org/2.4/doc/tutorials/calib3d/camera_calibration/camera_calibration.html
    distCoeff = np.array([k1, k2, k3, k4, k5])

    # Undistort image coordinates for fisheye model, solvePnP does not support it
    if invIC["modelID"] == 3:
        # image = undistort_fisheye(invIC, image, binning)
        image = cv2.fisheye.undistortPoints(image.T.reshape(-1, 1, 2), K=cameraMatrix, D=np.array([k1, k2, k3, k4]), P=np.eye(3)).reshape(-1, 2).T
        # There seems to be a small, constant offset between the two implementations
        # This is probably due to the definition of the origin of the coordinate systems
        cameraMatrix = np.eye(3)
        distCoeff = np.zeros((5,))

    retval, rvec, t = cv2.solvePnP(world.T, image.T, cameraMatrix, distCoeff)
    R, _ = cv2.Rodrigues(rvec)
    # algo expects cam -> world transformation
    r = rotMatReverse(R.T)
    t = -R.T.dot(t.squeeze())
    return r, t


def project(data, r, t, inverse=False):
    '''
    :return: R.dot(data) + t if inverse=False else R.T.dot(data - t)
    '''
    if inverse:
        return rotMat(*r).T.dot(data - np.array(t)[..., np.newaxis])
    else:
        return rotMat(*r).dot(data) + np.array(t)[..., np.newaxis]


def inverse_intrinsic_projection(camXYZ, invIC, binning, camRefToOpticalSystem):
    '''
    3D points to pixel coordinates
    :param camXYZ: 3xn camera coordinates
    :param invIC: inverse intrinsic calibration
    :param internalTransRot: (forward) internal TransRot
    :return: 2xn pixel coordinates
    '''

    # reverse internalTransRot
    r = np.array(camRefToOpticalSystem["rot"])
    t = np.array(camRefToOpticalSystem["trans"])
    P = project(camXYZ, r, t, inverse=True)

    X = P[0, :]
    Y = P[1, :]
    Z = P[2, :]

    tz = np.maximum(0.001, Z)
    ixn = X / tz
    iyn = Y / tz

    # apply distortion
    fb = 0.5 if binning else 1.0
    if invIC["modelID"] == 1:
        fx, fy, mx, my, alpha, k1, k2, k3, k4, k5 = invIC["modelParameters"][:10]

        rd2 = ixn ** 2 + iyn ** 2
        radial = rd2 * (k1 + rd2 * (k2 + rd2 * k5)) + 1
        ixd = ixn * radial
        iyd = iyn * radial
        if k3 != 0 or k4 != 0:
            h = 2 * ixn * iyn
            tangx = k3 * h + k4 * (rd2 + 2 * ixn ** 2)
            tangy = k3 * (rd2 + 2 * iyn ** 2) + k4 * h
            ixd += tangx
            iyd += tangy

    elif invIC["modelID"] == 3:
        fx, fy, mx, my, alpha, k1, k2, k3, k4, theta_max = invIC["modelParameters"][:10]

        lxy = np.sqrt(X**2 + Y**2)
        theta = np.arctan2(lxy, Z)
        phi = np.minimum(theta, theta_max)**2
        p_radial = 1 + phi*(k1 + phi*(k2 + phi*(k3 + phi*k4)))
        theta_s = p_radial * theta
        f_radial = np.choose(lxy > 0, (0, theta_s/lxy))
        ixd = f_radial * X
        iyd = f_radial * Y

    else:
        raise RuntimeError('Unknown intrinsic model ID %d'%invIC["modelID"])

    # transform to imager
    ix = ((fx * fb * (ixd - alpha * iyd)) + mx * fb) - 0.5
    iy = ((fy * fb * (iyd)) + my * fb) - 0.5
    

    return np.vstack([ix, iy])


def undistort_fisheye(inverseIntrinsicCalib, imgCoords, binningEnabled=False):
    ix = imgCoords[0, :]
    iy = imgCoords[1, :]
    cx = np.zeros_like(ix)
    cy = np.zeros_like(iy)

    assert inverseIntrinsicCalib["modelID"] == 3
    fx, fy, mx, my, alpha, k1, k2, k3, k4, theta_max = inverseIntrinsicCalib["modelParameters"][:10]
    fb = 0.5 if binningEnabled else 1.0
    tx = (ix + 0.5 - mx * fb) / (fx * fb)
    ty = (iy + 0.5 - my * fb) / (fy * fb)
    tx -= alpha * ty
    r2 = tx ** 2 + ty ** 2
    r = np.sqrt(r2)

    n = r.shape[0]

    # The code below is adapted from OpenCV (modules/calib3d/src/fisheye.cpp)

    # Define max count for solver iterations
    maxCount = 10
    epsilon = 1e-12

    for i in range(n):
        theta_d = r[i]

        # the current camera model is only valid up to 180 FOV
        # for larger FOV the loop below does not converge
        # clip values so we still get plausible results for super fisheye images > 180 grad
        theta_d = np.minimum(np.maximum(-np.pi / 2, theta_d), np.pi / 2)  # (How to) use theta_max here?

        converged = False
        theta = theta_d

        scale = 0

        if np.abs(theta_d) > epsilon:
            # compensate distortion iteratively
            for j in range(maxCount):
                theta2 = theta * theta
                theta4 = theta2 * theta2
                theta6 = theta4 * theta2
                theta8 = theta6 * theta2

                k0_theta2 = k1 * theta2
                k1_theta4 = k2 * theta4
                k2_theta6 = k3 * theta6
                k3_theta8 = k4 * theta8

                # new_theta = theta - theta_fix, theta_fix = f0(theta) / f0'(theta)
                theta_fix = (theta * (1 + k0_theta2 + k1_theta4 + k2_theta6 + k3_theta8) - theta_d) / (1 + 3 * k0_theta2 + 5 * k1_theta4 + 7 * k2_theta6 + 9 * k3_theta8)
                theta = theta - theta_fix

                if np.abs(theta_fix) < epsilon:
                    converged = True
                    break

                scale = np.tan(theta) / theta_d
            else:
                converged = True

            # theta is monotonously increasing or decreasing depending on the sign of theta
            # if theta has flipped, it might converge due to symmetry but on the opposite of the camera center
            # so we can check whether theta has changed the sign during the optimization
            theta_flipped = (theta_d < 0 and theta > 0) or (theta_d > 0 and theta < 0)

            if converged and not theta_flipped:
                cx[i] = tx[i] * scale
                cy[i] = ty[i] * scale

    return np.vstack([cx, cy])
