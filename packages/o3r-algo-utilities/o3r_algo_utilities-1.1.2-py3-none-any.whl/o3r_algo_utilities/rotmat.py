# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2020 ifm electronic gmbh
#
# THE PROGRAM IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.
#

"""
This module exports functions for handling the euler calibration angles used in O3R.
"""

import numpy as np

def rotMat(*rot_xyz):
    """
    Creates a rotation matrix from the given euler angles.

    :param rot_xyz: 3 element vector containing rotX, rotY and rotZ in [rad]
    :return: 3x3 rotation matrix R
    """
    res = np.eye(3)
    for i, alpha in enumerate(rot_xyz):
        lr = np.eye(3)
        lr[(i+1)%3, (i+1)%3] = np.cos(alpha)
        lr[(i+2)%3, (i+2)%3] = np.cos(alpha)
        lr[(i+1)%3, (i+2)%3] = -np.sin(alpha)
        lr[(i+2)%3, (i+1)%3] = np.sin(alpha)
        res = res.dot(lr)
    return res

def rotMatReverse(matR):
    """
    Calculates euler angles from a rotation matrix. This is the inverse of the rotMat() function.

    :param matR: 3x3 rotation matrix
    :return: rotX, rotY, rotZ in [rad]
    """
    alpha = np.arctan2(matR[1,2], matR[2,2])
    c2 = np.sqrt(matR[0,0]**2 + matR[0,1]**2)
    beta = np.arctan2(-matR[0,2], c2)
    s1 = np.sin(alpha)
    c1 = np.cos(alpha)
    gamma = np.arctan2(s1*matR[2,0] - c1*matR[1,0], c1*matR[1,1] - s1*matR[2,1])
    rotX, rotY, rotZ = -alpha, -beta, -gamma
    if rotX < -np.pi/2 or rotX > np.pi/2:
        if rotX < 0:
            rotX += np.pi
        else:
            rotX -= np.pi
        rotY = np.pi - rotY
        if rotY < -np.pi:
            rotY += 2*np.pi
        if rotY > np.pi:
            rotY -= 2*np.pi
        rotZ = rotZ + np.pi
        if rotZ > np.pi:
            rotZ -= 2*np.pi
    return rotX, rotY, rotZ

def o3rCalibAnglesToHumanReadable(*rot_xyz):
    """
    Converts the O3R euler angles into a human readable format.

    The resulting 3 angles are yaw, pitch and roll.

    The yaw angle describes the viewing direction of the camera in a standard robotics coordinte system (x pointing
    forward, y pointing left and z pointing upwards). yaw=0 is a forward looking camera, yaw=90 is a left looking
    camera, etc.

    The pitch angle describes the tilt angle of the camerea. pitch=0 is a horizontally mounted camera, pitch>0 is a
    camera pointing downwards and pitch<0 is a camera pointing upwards.

    The roll angle describes the roll angle of the camera. roll=0 is the canonical form (a non-rotated panorama view).
    roll=180 is the panorama view rotated by 180°, etc.

    :param rot_xyz: 3 element vector containing rotX, rotY and rotZ in [rad]
    :return: yaw, pitch and roll angle in [degree]
    """
    matR = rotMat(*rot_xyz)

    # the pitch and roll angles are defined readily by the transformation result of [0,0,1]

    # R transforms vectors in the head coordinate system to vectors in the vehicle coordinate system
    # for better readability, we want to split this rotation into multiple parts:
    #   R = R_yaw @ R_pitch @ R_roll @ R_swap
    # with R_swap is the matrix which swaps head coordinate system vectors into canonical front looking cameras
    #            | 0  0  1 |
    #   R_swap = |-1  0  0 |
    #            | 0 -1  0 |
    #
    # R_yaw turns the coordinate system to forward, left, backward, right looking cameras
    #           | cy -sy  0 |
    #   R_yaw = | sy cy   0 | (where sy,cy is sin(yaw), cos(yaw) respectively, yaw in [0,...360[ )
    #           | 0   0   1 |
    # R_pitch tilts the coordinate system
    #             | cp 0  sp|
    #   R_pitch = | 0  1  0 |
    #             |-sp 0  cp|
    # R_roll rolls the coordinate system
    #             | 1  0  0 |
    #   R_roll =  | 0 cr -sr|
    #             | 0 sr cr |

    spitch = -matR[2,2]
    pitch = np.arcsin(spitch)
    yaw = np.arctan2(matR[1,2], matR[0,2])

    matRyaw = rotMat(0.0,0.0,yaw)
    matRpitch = rotMat(0.0,pitch,0.0)
    matRswap = np.array([
        [0,0,1],
        [-1,0,0],
        [0,-1,0]
    ], dtype=float)
    # R = R_yaw @ R_pitch @ R_roll @ R_swap
    # -> R_roll = (R_yaw @ R_pitch).T @ R @ R_swap.T
    matRroll = (matRyaw @ matRpitch).T @ matR @ matRswap.T
    roll = np.arctan2(matRroll[2,1], matRroll[2,2])
    return yaw*180/np.pi, pitch*180/np.pi, roll*180/np.pi

def humanReadableToO3RCalibAngles(yaw, pitch, roll):
    """
    This function converts human readable orientation angles into O3R calibration angles. It is the inverse of
    o3rCalibAnglesToHumanReadable.

    :param yaw: yaw angle in degree
    :param pitch: pitch angle in degree
    :param roll: roll angle in degree
    :return: rotX, rotY, rotZ O3R euler rotation angles in [rad]
    """
    yaw *= np.pi/180
    pitch *= np.pi/180
    roll *= np.pi/180

    matRyaw = rotMat(0.0,0.0,yaw)
    matRpitch = rotMat(0.0,pitch,0.0)
    matRroll = rotMat(roll,0.0,0.0)
    matRswap = np.array([
        [0,0,1],
        [-1,0,0],
        [0,-1,0]
    ], dtype=float)
    return rotMatReverse( matRyaw @ matRpitch @ matRroll @ matRswap)
