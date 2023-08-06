# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2020 ifm electronic gmbh
#
# THE PROGRAM IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.
#

import logging
import string
import numpy as np
import argparse
from o3r_algo_utilities.calib.corner_detector import findChessboardCorners 
from o3r_algo_utilities.calib import sources
from o3r_algo_utilities.calib import point_correspondences as cpc

logger = logging.getLogger(__name__)

help="""
IFM ODS CALIBRATION
 
This script allows us to estimate the extrinsic camera calibration using the coordinates of the 4 corners
of the pattern:

      (A)                      (B)
        ffffffffffffffffffffffff
        f++--++--++--++--++--++f
        f--++--++--++--++--++--f
        f++--++--++--++--++--++f
        f--++--++--++--++--++--f
        f++--++--++--++--++--++f
        ffffffffffffffffffffffff
      (C)                      (D)

Here, the 'f' is a white frame around the pattern, ++ and -- are the black and white checkerboard 
regions and (A), (B), (C) and (D) are the 4 corner points with known 3D coordinates in the robot coordinate 
system. 

Target Orientation
------------------
AB is defined as the target width direction and AC is defined as the target height direction. The target 
width is defined as the number of inner corner points, this number is 10 in the example above while the 
target height is 4. The point A must be in the upper part of the image (viewed in the default orientation).

There are different ways to specifiy the coordinates:

    1. Using 3D coordinates for all four corner points: 
            -cc "A=(<Ax>,<Ay>,<Az>),B=(<Bx>,<By>,<Bz>),C=(<Cx>,<Cy>,<Cz>),D=(<Dx>,<Dy>,<Dz>)"
            
    2. Using common coordinates (useful if the target is aligned in the robot coordinate system): 
            -cc "X_AB=<Ax>,X_CD=<Cx>,Z_AB=<Az>,Z_CD=<Cz>,Y_AC=<Ay>,Y_BD=<By>"

The coordinates should be in the order indicated above and comprise 3 coordinates (x, y, z) in the robot 
coordinate system.

The extrinsic camera calibration consists of a translation and rotation. It may be more accurate to use the
translation part from a blueprint and only estimate the rotation part. In this case the translation can be 
provided using the `fixed_translation` parameter.
"""

def calibrate(pattern_corner_coordinates, o3r_frame, optMode, fixed_translation, max_allowed_validation_error, 
              max_allowed_reconstruction_error, display, target_size, image_selection):
    """
    Main calibration function. 
    
    :param pattern_corner_coordinates: Must be a tuple (A,B,C,D) where the elements are the respective 
        3D world coordinates of the target corners (with the white frame removed)
    :param o3r_frame: Dictionary containing an o3r frame with keys "A" (amplitude), "D" (distance), 
        "X", "Y", "Z" (Cartesian coordinates), "inverseIntrinsic" and "camRefToOpticalSystem". Note that
        it is expected that this frame is taken with extrinsicHeadToUser all set to zero.
    :param optMode: Optimization mode to be used. Supported modes are "min" (scipy.optimize.minimize in an L2 setting),
        "lsq" (scipy.optimize.least_squares) and "minabs" (scipy.optimize.minimize in an L1 setting)
    :param fixed_translation: None or the 3D world coordinates of the camera reference point. If given, this point
        will not be part of the optimization process.
    :param max_allowed_validation_error: Maximum mean validation error in [m]. Note that this validation error is
        usually affected by MPI.
    :param max_allowed_reconstruction_error: Maximum allowed reconstruction error in [px].
    :param display: Boolean whether to output a matplotlib figure.
    :param target_size: The number of inner corners of the checkerboard target.
    :return: r (rotation vector), t (translation vector) suitable for extrinsicHeadToUser calibration
    """
    A, B, C, D = pattern_corner_coordinates
    A, B, C, D = np.array(A), np.array(B), np.array(C), np.array(D)
    logger.debug("Pattern corner points are\nA:{},\nB:{},\nC:{},\nD:{}".format(A, B, C, D))

    world = world_coordinates_from_corners(A, B, C, D, target_size)

    r = None
    t = None

    # Find the chess board corners
    if image_selection == "amplitude":
        img = o3r_frame["A"]
    elif image_selection == "reflectivity":
        img = o3r_frame["R"].astype(np.float32)
        img[o3r_frame["D"] <= 0] = np.nan
    else:
        raise RuntimeError("Unknown image selection value: %s" % image_selection)
    corners, gray = findChessboardCorners(img, target_size)
    if display:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(13,9))
        plt.subplot(221)
        plt.imshow(gray, cmap="gray")

    if corners is None:
        logger.error("Could not detect corners. Make sure that the pattern is fully visible and that there are no direct reflexes in the image.")
        raise RuntimeError("Could not detect corners.")

    # If found, add object points, image points (after refining them)
    imgpoints = [corners]

    # find best-fitting world to camera transformation
    r, t, rms, rms_unit = cpc.find_transformation(
        np.tile(world, (1, len(imgpoints))),
        np.hstack(imgpoints),
        o3r_frame["inverseIntrinsic"],
        fixed_translation,
        optMode=optMode, 
        binning=False,
        camRefToOpticalSystem=o3r_frame["camRefToOpticalSystem"],
    )

    with np.printoptions(precision=3, suppress=True, sign='+'):
        logger.info('Reconstruction error after calibration %s=%.4f [px]', rms_unit, rms)

    if display:
        # plots
        # project defined chessboard corners into image in green using the transformation
        world2cam = cpc.project(world, r, t, inverse=True)
        world2cam = cpc.inverse_intrinsic_projection(world2cam, o3r_frame["inverseIntrinsic"], binning=False,
                                                     camRefToOpticalSystem=o3r_frame["camRefToOpticalSystem"])
        logger.info("world2cam.shape=%s, corners.shape=%s", world2cam.shape, corners.shape)
        plt.plot(corners[0,:], corners[1,:], 'xm')
        N = corners.shape[1]
        labels = (string.ascii_lowercase + string.digits + string.ascii_uppercase)[:N]
        for i in range(N):
            lbl = labels[i]
            if i in [0, N-1]:
                lbl += " [%.2f %.2f %.2f]" % tuple(world[:,i])
            plt.annotate(lbl, xy=corners[:,i], xytext=(20,5), textcoords='offset pixels', ha="right", va="bottom", color="m", fontsize="large")
            plt.plot([world2cam[0,i], corners[0,i]], [world2cam[1,i], corners[1,i]], 'm-')
        plt.title("Image and Corner Detections")
        
        plt.subplot(222)
        plt.scatter(world2cam[0,:] - corners[0,:], world2cam[1,:] - corners[1,:], marker='x')
        for i in range(N):
            plt.annotate(labels[i], xy=(world2cam-corners)[:,i], xytext=(20,5), textcoords="offset pixels", ha="right", va="bottom", color="b", fontsize="large")
        plt.xlabel("x error [px]")
        plt.ylabel("y error [px]")
        plt.axis("equal")
        plt.grid()
        plt.title("Reconstruction errors [px] (proj(gt) - meas); %s=%.4f [px]" % (rms_unit, rms))
    
    if rms > max_allowed_reconstruction_error:
        logger.error("Maximum reconstruction error exceeded.")
        raise RuntimeError("Maximum reconstruction error exceeded.")

    logger.info("extrinsicHeadToUser: rot=%s trans=%s" % (r, t))
    validation(world, max_allowed_validation_error, display, r, t, o3r_frame, (A,B,C,D), world2cam - corners if display else None, target_size, img)
    return t, r

def validation(world, max_allowed_error, display, R_cal, t_cal, o3r_frame, pattern_corner_coordinates, pixel_errors, target_size, img):
    '''
    Validates the 3d data with the optimized extrinsic calibration on the camera
    
    :param world: 2xN array with the expected world coordinates of the checkerboard pattern [m]
    :param max_allowed_error: maximum mean 3D error of the corner points
    :param display: Boolean whether to output a matplotlib figure.
    :param R_cal: calibrated rotation vector (suitable for extrinsicHeadToUser)
    :param t_cal: calibrated translation vector (suitable for extrinsicHeadToUser)
    :param o3r_frame: Dictionary containing an o3r frame with keys "A" (amplitude), "D" (distance), 
        "X", "Y", "Z" (Cartesian coordinates), "inverseIntrinsic" and "camRefToOpticalSystem"
    :param pattern_corner_coordinates: Must be a tuple (A,B,C,D) where the elements are the respective 
        3D world coordinates of the target corners (with the white frame removed)
    :param pixel_errors: 2xN array with the pixel error values (only needed if display=True)
    :param target_size: number of inner corners of the target
    '''
    logger.info('Validation using 3D data')
    
    # locate the chessboard in the image
    corners, gray = findChessboardCorners(img, target_size)
    if corners is None:
        logger.error("Chess board corners could not be detected.")
        raise RuntimeError("validation not possible.")
    logger.debug('Chess board corners detected')

    # setup a Cartesian array with dimensions height x width x 3
    xyz = np.zeros(o3r_frame["X"].shape + (3,))
    xyz[...,0] = o3r_frame["X"]
    xyz[...,1] = o3r_frame["Y"]
    xyz[...,2] = o3r_frame["Z"]
    # set invalid pixels to nan
    xyz[o3r_frame["D"] == 0,:] = np.nan

    # project these cartesian coordinates back into the optical system
    camRefToOpticalSystem = o3r_frame["camRefToOpticalSystem"]
    R_i = cpc.rotMat(*camRefToOpticalSystem["rot"])
    t_i = np.array(camRefToOpticalSystem["trans"])
    def rot(R, A):
        s = A.shape
        A = np.reshape(A, (-1,3)).T
        return np.reshape(R.dot(A).T, s)
    xyz_os = rot(R_i.T,xyz - t_i[np.newaxis,np.newaxis,:])
    # check that these coordinates are consistent with the original distance matrix
    assert np.all(np.logical_or(np.isclose(np.linalg.norm(xyz_os, axis=-1), o3r_frame["D"], atol=1e-4), o3r_frame["D"] == 0))

    # project into new calibrated system
    R_e = cpc.rotMat(*R_cal)
    t_e = np.array(t_cal)
    xyz_c = rot(R_e, rot(R_i, xyz_os) + t_i[np.newaxis,np.newaxis,:]) + t_e[np.newaxis,np.newaxis,:]
    t_t = t_e + R_e.dot(t_i)

    # get the 3D coordinates at the detected checkerboard features
    icorners = np.round(corners).astype(int)
    x = xyz_c[icorners[1, :], icorners[0, :], 0]
    y = xyz_c[icorners[1, :], icorners[0, :], 1]
    z = xyz_c[icorners[1, :], icorners[0, :], 2]
    N = icorners.shape[1]
    # labels for display purpose
    labels = (string.ascii_lowercase + string.digits + string.ascii_uppercase)[:N]
            
    all_errors = [] # 3D errors in world coordinates
    all_errors_o3r = [] # x error in [px], y error in [px] and distance error in [m]
    all_labels = ""
    for i in range(N):
        if np.isnan(x[i]):
            continue
        M = np.array([x[i], y[i], z[i]])
        # calculate 3D error in world coordinates
        err = world[:,i] - M
        logger.debug("%2d: xyz         =(%6.3f %6.3f %6.3f)" % ((i,) + tuple(M)))
        logger.debug( "    gt          =(%6.3f %6.3f %6.3f)" % tuple(world[:,i]))
        if display:
            all_errors.append(err)
            all_labels += labels[i]
            err_o3r = np.array([pixel_errors[0,i], 
                                pixel_errors[1,i],
                                np.linalg.norm(world[:,i] - t_t) - np.linalg.norm(M - t_t)])
            all_errors_o3r.append(err_o3r)

    # convert the 3D error into a distance for each point
    error = np.linalg.norm((np.stack([x, y, z]) - world), axis=0)
    if np.all(np.isnan(error)):
        logger.error("all 3D measurements are invalid")
        raise RuntimeError("all measurements are invalid.")

    if display:
        # rotate error into checkerboard coordinate system
        all_errors = np.array(all_errors).T # 3 x K
        import matplotlib.pyplot as plt
        A,B,C,D = pattern_corner_coordinates
        t1 = (C-A)/np.linalg.norm(C-A)
        t2 = (B-A)/np.linalg.norm(B-A)
        t3 = np.cross(t1, t2)
        Rw2c = np.array([t1, t2, t3]).T
        logger.debug("AB projected on checkerboard: %s", Rw2c.dot(B-A)) # should be appr. size of the target
        logger.debug("AC projected on checkerboard: %s", Rw2c.dot(C-A)) # should be appr. size of the target
        errproj = Rw2c.dot(all_errors)
        # and generate an error plot based on this system
        plt.subplot(223)
        plt.scatter(errproj[1,:], errproj[0,:], c=errproj[2,:])
        for i in range(all_errors.shape[1]):
            plt.annotate(all_labels[i], xy=errproj[1::-1,i], xytext=(20,5), textcoords="offset pixels", ha="right", va="bottom", color="b", fontsize="large")
        plt.title("Validation using 3D [m] (gt3d - meas); mean=%.3f m" % np.nanmean(error))
        plt.xlabel("error in AB direction [m]")
        plt.ylabel("error in AC direction [m]")
        plt.colorbar()
        plt.axis("equal")
        plt.grid()
        
        # calculate errors in O3R pixel coordinates / O3R distance measurements
        all_errors_o3r = np.array(all_errors_o3r).T
        plt.subplot(224)
        plt.scatter(all_errors_o3r[0,:], all_errors_o3r[1,:], c=all_errors_o3r[2,:])
        for i in range(all_errors.shape[1]):
            plt.annotate(all_labels[i], xy=all_errors_o3r[0:2,i], xytext=(20,5), textcoords="offset pixels", ha="right", va="bottom", color="b", fontsize="large")
        plt.title("Validation Distance errors [m] (gt - meas)")
        plt.ylabel("error x [px]")
        plt.xlabel("error y [px]")
        plt.colorbar()
        plt.axis("equal")
        plt.grid()

    logger.info('Validation error is based on %d valid and %d invalid measurements', np.sum(np.isfinite(error)), np.sum(np.isnan(error)))
    logger.info('Validation error statistics [m]: min: {:.3f} mean: {:.3f}, median: {:.3f}, max: {:.3f}, std: {:.3f}'.format(
        np.nanmin(error),
        np.nanmean(error),
        np.nanmedian(error),
        np.nanmax(error),
        np.nanstd(error),
        )
    )
    logger.info("The validation errors are often affected by MPI artifcats such that a certain bias in distance should be considered as normal.")
    logger.info("These effects might be reduced by optimizing the mode and the offset parameters.")

    if np.nanmean(error) > max_allowed_error:
        logger.error('Mean error is bigger than `max_allowed_error`: {} > {}'.format(np.nanmean(error), max_allowed_error))
        raise RuntimeError("Validation did not succeed.")
    else:
        logger.info('Error is within tolerance')
        logger.debug('Calibration done')


def world_coordinates_from_corners(A, B, C, D, target_size):
    """
    This functions creates the chessboard world coordinates from
    
    :param A: upper left corner
    :param B: upper right corner
    :param C: lower left corner
    :param D: lower right corner
    """
    world = []
    AC = []
    BD = []
    tw, th = target_size # usually 6,4
    for i in range(1, th+1):
        gamma = i / (th+1)
        AC.append((1 - gamma) * A + gamma * C)
        BD.append((1 - gamma) * B + gamma * D)

    for u, v in zip(AC, BD):
        for i in range(1, tw+1):
            gamma = i / (tw+1)
            world.append((1 - gamma) * u + gamma * v)

    world = np.array(world).T
    return world

def cc_to_coordinates(**kw):
    """
    Helper function for parsing user-supplied pattern positions. The keyword arguments can either be
    in the form of [ABCD]=(<X>,<Y>,<Z>) or [XYZ]_<set(ABCD)>=<value>.
    """
    res = dict(A = np.full(3, np.nan), B = np.full(3, np.nan), C = np.full(3, np.nan), D = np.full(3, np.nan))
    processed = set()
    for k in "ABCD":
        if k in kw:
            try:
                v = np.array(kw[k], dtype=float)
            except:
                raise RuntimeError("For point specification %s=v, v must be a float array of size 3. Given v: %s" % (k, kw[k]))
            if not len(v) == 3:
                raise RuntimeError("For point specification %s=v, v must be a float array of size 3. Given v: %s" % (k, v))
            if not np.all(np.logical_or(np.isnan(res[k]), res[k] == v)):
                raise RuntimeError("Inconsistent coordinate definition (point %s is set to %s and %s at the same time).", k, res[k], kw[k])
            res[k][:] = kw[k]
            processed.add(k)
    for k in kw:
        if "_" in k:
            splitres = k.split("_")
            if not len(splitres) == 2:
                raise RuntimeError("%s=%s: Cannot interpret statement (expecting exactly one underscore)." %(k, kw[k]))
            axis,points = splitres # assume ["[XYZ]_([ABCD]+)"]
            idx = 0 if axis == "X" else 1 if axis == "Y" else 2 if axis == "Z" else None
            if idx is None:
                raise RuntimeError("%s=%s: In common coordinate statements, expecting either X,Y or Z before the underscore." %(k, kw[k]))
            for p in points:
                if not p in "ABCD":
                    raise RuntimeError("%s=%s: specified points must be A,B,C or D. Given: %s" %(k, kw[k], p))
                if not (np.isnan(res[p][idx]) or res[p][idx] == kw[k]):
                    raise RuntimeError("Inconsistent coordinate definition (point %s is set to %s and %s at the same time).", p, res[p][idx], kw[k])
                res[p][idx] = kw[k]
            processed.add(k)
    for p in processed:
        del kw[p]
    if not len(kw) == 0:
        k = list(kw.keys())[0]
        raise RuntimeError("Don't know how to interpret %s=%s" % (k, kw[k]))
    for k in "ABCD":
        if np.any(np.isnan(res[k])):
            raise RuntimeError("Point %s was not specified completely (%s)." % (k, res[k]))
    return res["A"], res["B"], res["C"], res["D"]

def correct_frame(frameSize, A, B, C, D):
    """
    Remove the frame from the supplied 3D positions of the target corners.
    
    :param frameSize: frame size in [m]
    :param A: 3D coordinates of upper left corner of the target (including the frame)
    :param B: 3D coordinates of upper right corner of the target (including the frame)
    :param C: 3D coordinates of lower left corner of the target (including the frame)
    :param D: 3D coordinates of lower right corner of the target (including the frame)
    :return cA,cB,cC,cD corrected 3D coordinates without the frame.
    """
    # calculate side vectors
    AB = (B-A) / np.linalg.norm(B-A)
    AC = (C-A) / np.linalg.norm(C-A)
    CD = (D-C) / np.linalg.norm(D-C)
    BD = (D-B) / np.linalg.norm(D-B)
    # undo effect of frame
    cA = A + AB*frameSize + AC * frameSize
    cB = B - AB*frameSize + BD * frameSize
    cC = C - AC*frameSize + CD * frameSize
    cD = D - AC*frameSize - CD * frameSize
    return cA, cB, cC, cD

def calib(source, pattern_corner_coordinates, target_width, target_height,
          frame_size=0.0, fixed_translation=None, verbosity="INFO", graphical=True,
          max_allowed_validation_error=0.06, max_allowed_reconstruction_error=0.4, opt_mode="min",
          image_selection="amplitude", mode="standard_range4m"):
    logging.basicConfig(level=verbosity)

    cc = eval("dict(" + pattern_corner_coordinates + ")")
    A, B, C, D = cc_to_coordinates(**cc)
    logger.info("Target coordinates parsed successfully. Target size [m]: AB=%.3f CD=%.3f AC=%.3f BD=%.3f ",
                np.linalg.norm(A-B), np.linalg.norm(C-D), np.linalg.norm(A-C), np.linalg.norm(B-D))
    derr = np.linalg.norm(A + (B-A) + (C-A) - D)
    if frame_size != 0.0:
        A, B, C, D = correct_frame(frame_size, A, B, C, D)
        logger.info("Corrected coordinates for frame size: %.3f m", frame_size)
        logger.info("Target coordinates parsed successfully. Target size [m]: AB=%.3f CD=%.3f AC=%.3f BD=%.3f ",
                    np.linalg.norm(A-B), np.linalg.norm(C-D), np.linalg.norm(A-C), np.linalg.norm(B-D))
    logger.info("A=(%6.3f, %6.3f, %6.3f)", *tuple(A))
    logger.info("B=(%6.3f, %6.3f, %6.3f)", *tuple(B))
    logger.info("C=(%6.3f, %6.3f, %6.3f)", *tuple(C))
    logger.info("D=(%6.3f, %6.3f, %6.3f)", *tuple(D))
    logger.info("Distance between chessboard corners: d_AB=%.3f m d_AC=%.3f m", np.linalg.norm(B-A)/(target_width+1), np.linalg.norm(C-A)/(target_height+1), )
    logger.info("Reconstruction error of point D from A,B and C: %.3f m%s", derr, " (plausible)" if np.abs(derr) <= 0.01 else "")
    if np.abs(derr) > 0.01:
        logger.error("The target coordinates are inconsistent.")
        return 1
    
    #A, B, C, D = [np.array(coordinate, dtype=float) for coordinate in eval(args.pattern_corner_coordinates)]
    fixed_translation = np.array(eval(fixed_translation)).squeeze() if fixed_translation is not None else None
    
    frame = sources.getFrame(source, mode)

    if ((not np.all(np.abs(frame["camRefToOpticalSystem"]["trans"]) < 0.08)) or
        (not np.all(np.abs(frame["camRefToOpticalSystem"]["rot"]) < 5*np.pi/180))):
        logger.error("Cam ref to optical system seems to be non-plausible. Please make sure that you have reset the extrinsic calibration before applying the calibration.")
        raise RuntimeError("Calibration is not resetted (trans=%s rot=%s)." % (frame["camRefToOpticalSystem"]["trans"], 
                                                                               frame["camRefToOpticalSystem"]["rot"]))
    try:
        extrHeadToUserTrans, extrHeadToUserRot = calibrate([A, B, C, D], frame,
                  optMode=opt_mode,
                  fixed_translation=fixed_translation, 
                  max_allowed_validation_error=max_allowed_validation_error,
                  max_allowed_reconstruction_error=max_allowed_reconstruction_error,
                  display=graphical,
                  target_size=(target_width, target_height),
                  image_selection=image_selection)
        res = "succeeded"
        return extrHeadToUserTrans, extrHeadToUserRot
    except Exception as e:
        res = "failed (%s)" % str(e)
        raise
    finally:
        if graphical:
            import matplotlib.pyplot as plt
            plt.suptitle(r"Calibration result: " + res, fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.show(block=True)


def main():
    """
    main function for calibration.
    """
    parser = argparse.ArgumentParser(description='ifm ods calibration', epilog=help, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-cc', '--pattern_corner_coordinates', type=str, required=True,
                        help='See the section about specifying the corners for details.')
    parser.add_argument('-f', '--frame_size', type=float, default=0.0, help="The size of the (white) frame around the pattern in [m].")
    parser.add_argument('-ft', '--fixed_translation', default=None, type=str, help='use this translation vector instead of an estimation')
    parser.add_argument('-v', '--verbosity', default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"], help='The log level (DEBUG,INFO,WARNING,ERROR)')
    parser.add_argument('-g', '--graphical', action="store_true", default=False, help="Show plots.")
    parser.add_argument('-tw', '--target_width', default=6, type=int, help="number of inner corners per chessboard row (i.e. in AB direction).")
    parser.add_argument('-th', '--target_height', default=4, type=int, help="number of inner corners per chessboard column (i.e. in AC direction).")
    parser.add_argument('-mve', '--max_allowed_validation_error', default=0.06, type=float, help='Maximum allowed validation error (default: %(default).2f) [m]')
    parser.add_argument('-mre', '--max_allowed_reconstruction_error', default=0.4, type=float, help='Maximum allowed reconstruction error (default: %(default).2f) [px]')
    parser.add_argument('-om', '--opt_mode', default="min", choices=["min", "lsq", "minabs"], help='"min" uses scipy.optimize.minimize and in a least squares setting, "lsq" uses scipy.optimize.least_squares, "minabs" uses scipy.minimize in a mean absolute error setting.')
    parser.add_argument('-is', '--image_selection', default="amplitude", choices=["amplitude", "reflectivity"], help="choose whether to use amplitude or reflectivity image.")
    parser.add_argument("-m", "--mode", default="standard_range4m", choices=["standard_range4m", "standard_range2m", "extrinsic_calib"], help="choose the mode of the port.")
    parser.add_argument("source", type=str, default="ad://192.168.0.69/port2",
                        help="The source to be used. Currently supported schemes: "
                             "'adlive://<ip>/port<C>' use algo debug input with specified ip address and camera port number C=0..5 (requires imeas)."
                             "'adrec://<h5path> use algo debug input stored in a h5 file."
                             "'ifm3dpy://<ip>/port<C>' use ifm3d library input with specified ip address and camera port number C=0..5 (requires ifm3dpy)."
                        )
    # TODO: add vision assist h5 file mode
    args = parser.parse_args()
    calib(**vars(args))

if __name__ == "__main__":
    main()
