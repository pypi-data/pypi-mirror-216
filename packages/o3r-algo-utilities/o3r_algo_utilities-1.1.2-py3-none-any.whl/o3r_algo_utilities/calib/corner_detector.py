"""
This module provides a function for detecting checkerboard corners in amplitude images.
"""
import logging
import numpy as np
import cv2

logger = logging.getLogger(__name__)

def findChessboardCorners(ampl, patternSize, enhanced=True, outputAll=False):
    '''
    detects chessboard corners in an amplitude image. The chessboard will be aligned such that the first corner is
    above the last corner in the image
    
    :param ampl: amplitude image as outputted by O3R
    :param patternSize: number of inner corners in the chessboard directions
    :return: corners, gray if the chessboard corners could be detected; otherwise None, gray
    '''
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    solutions = []

    def refine(corners, gray):
        # subpixel refinement
        corners = cv2.cornerSubPix(gray, corners, (3, 3), (-1, -1), criteria)
        corners = np.array(corners).squeeze().T
        if patternSize[0] % 2 != 0 or patternSize[1] % 2 != 0 and corners[1,0] > corners[1,-1]:
            # this might happen, see here:
            # https://stackoverflow.com/questions/19190484/what-is-the-opencv-findchessboardcorners-convention
            logger.info("chessboard corners need reversal shape=%s corners[:, 0]=%s corners[:, -1]=%s",
                        corners.shape, corners[:, 0], corners[:, -1])
            corners = corners[:,::-1]
        return corners

    # rescaled amplitude image for coner detection
    gray = np.interp(ampl, (np.nanpercentile(ampl, 20), np.nanpercentile(ampl, 80)), (40, 215)).astype(np.uint8)
    fccOptions = None
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, patternSize, fccOptions)
    if ret:
        if outputAll:
            corners = refine(corners, gray)
        solutions.append((corners, gray))
    if enhanced and (outputAll or not ret):
        gray = np.interp(ampl, (np.min(ampl),np.nanpercentile(ampl, 50), np.nanpercentile(ampl, 90),np.max(ampl)),
                         (0, 40, 215, 255)).astype(np.uint8)
        ret, corners = cv2.findChessboardCorners(gray, patternSize, fccOptions)
        if ret:
            if outputAll:
                corners = refine(corners, gray)
            solutions.append((corners, gray))
        if outputAll or not ret:
            gray = np.interp(ampl, (np.min(ampl),np.nanpercentile(ampl, 10), np.nanpercentile(ampl, 50),np.max(ampl)),
                             (0, 40, 215, 255)).astype(np.uint8)
            ret, corners = cv2.findChessboardCorners(gray, patternSize, fccOptions)
            if ret:
                if outputAll:
                    corners = refine(corners, gray)
                solutions.append((corners, gray))

    if outputAll:
        return solutions

    # If found, add object points, image points (after refining them)
    if len(solutions) > 0:
        corners, gray = solutions[0]
        corners = refine(corners, gray)
        return corners, gray
    return None, gray
