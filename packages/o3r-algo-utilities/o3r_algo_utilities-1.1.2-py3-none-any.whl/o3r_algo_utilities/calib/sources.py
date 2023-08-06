"""
This module encapsulates the different sources which might be used by the calibration.
"""
import logging
import struct
import numpy as np
import scipy.ndimage as ndi
import h5py
from o3r_algo_utilities import o3r_uncompress_di
try:
    import ifm3dpy
except ImportError:
    ifm3dpy = None

try:
    from ifm_imeas.imeas_tools import unpack_imeas
except ImportError:
    # Optional algo debug h5 files / algo debug live input are not supported.
    unpack_imeas = None

try:
    from ifm_o3r_algodebug.Receiver import ADReceiver
except ImportError:
    # Optional algo debug live input is not supported.
    ADReceiver = None

logger = logging.getLogger(__name__)
if ifm3dpy is None:
    logger.warning("ifm3dpy is not installed. Consider to depend your project to 'o3r_algo_utilities[ifm3dpy]'")

def getFrame(source, mode):
    """
    :param source: Specifies the source the following formats are supported:
        'adrec://<pathToFile>' use an algo debug hdf5 recording stored in <pathToFile> 
            (requires the ifm proprietary library imeas)
        'adlive://<ip>/port<camPort>' use a live connection to the camera specified 
            by <ip> and <camPort> (0..5)
        'ifm3dpy://<ip>/port<camPort>' use a live connection to the camera specified 
            by <ip> and <camPort> (0..5)    """
    if source.startswith("adrec://"):
        if unpack_imeas is None:
            raise RuntimeError("The ifm-internal tool imeas is required for reading algo debug recordings.")
        h5_algo_debug = source[len("adrec://"):]
        frame = load_algo_debug_recording(h5_algo_debug)
    elif source.startswith("adlive://"):
        if unpack_imeas is None:
            raise RuntimeError("The ifm-internal tool imeas is required for algo debug input.")
        if ADReceiver is None:
            raise RuntimeError("The tool ifm_o3r_algodebug is required for algo debug live input.")
        ip_port = source[len("adlive://"):]
        ip, port = ip_port.split("/")
        if port.startswith("port"):
            port = port[len("port"):]
        port = int(port)
        frame = grab_algo_debug(ip, port, mode)
    elif source.startswith("ifm3dpy://"):
        ip_port = source[len("ifm3dpy://"):]
        ip, port = ip_port.split("/")
        if port.startswith("port"):
            port = port[len("port"):]
        port = int(port)

        frame = grab_ifm3d_frame(ip, port, mode)
        
    else:
        raise RuntimeError("cannot interpret source.")

    conf = frame["C"]
    img = frame["A"]
    # replace suspect pixel and invalid amplitudes with a median-ed version
    M = np.logical_or((conf & 128) == 128, img < 0)
    if np.sum(M) > 0:
        img[M] = (ndi.median_filter(img, (3, 3)))[M]
    img[img < 0] = 0

    return frame
    
def load_algo_debug_recording(h5file):
    """
    Parses the last frame of an algo debug measurement while ignoring the referenced calibration.
    
    :param h5file: The path of the h5 file to be read.
    :return: a dictionary with Cartesian coordinates, distance and amplitude matrix and calibration information.
    """
    f = h5py.File(h5file, "r")
    calib = None
    for i in range(len(f["streams"]["o3r_di_0"])):
        d, _ = unpack_imeas(f["streams"]["o3r_di_0"][i][0].tobytes(), add_toplevel_wrapper=False)
        if "irs2381/calib" in d:
            calib = d["irs2381/calib"]
            break

    d,_ = unpack_imeas(f["streams"]["o3r_di_0"][-1][0].tobytes(), add_toplevel_wrapper=False)
    f.close()
    
    ifout_compr = d["irs2381/ifout_compr"]

    return proc_algo_debug(calib, ifout_compr)

def grab_algo_debug(ip, port, mode):
    calib = None
    ifout_compr = None
    o3r = ifm3dpy.O3R(ip=ip)
    oldConfig=o3r.get([f"/ports/port{port}"])
    try:
        # setting extrinsic to zero is not strictly necessary for the algo debug frames, but we do it nevertheless to
        # be similar to ifm3d grabbing
        o3r=set_extrinsic_zero(o3r, port, mode)
        with ADReceiver(ip, "port%d"%port, autoInterpret=True, xmlrpcTimeout=3, autostart=True) as rcv:
            logger.debug("receiving frame ...")
            cnt = 0
            ifout_compr = None
            while cnt < 10:
                data = rcv.get(timeout=3)
                cnt += 1
                if "irs2381/calib" in data:
                    calib = data["irs2381/calib"]
                if "irs2381/ifout_compr" in data:
                    # use 2m mode if available
                    if ifout_compr is None or data["irs2381/ifout_compr"].measurementRangeMax < ifout_compr.measurementRangeMax:
                        ifout_compr = data["irs2381/ifout_compr"]
            if calib is None or ifout_compr is None:
                raise RuntimeError("Could not grab algo debug frame from specified address.")
            frame = proc_algo_debug(calib, ifout_compr)
        
        # need to grab another frame with "normal" mode for validation purpose
        o3r=set_extrinsic_zero(o3r, port, "standard_range4m")
        with ADReceiver(ip, "port%d"%port, autoInterpret=True, xmlrpcTimeout=3, autostart=True) as rcv:
            logger.debug("receiving frame ...")
            cnt = 0
            ifout_compr = None
            while cnt < 10:
                data = rcv.get(timeout=3)
                cnt += 1
                if "irs2381/calib" in data:
                    calib = data["irs2381/calib"]
                if "irs2381/ifout_compr" in data:
                    # use 2m mode if available
                    if ifout_compr is None or data["irs2381/ifout_compr"].measurementRangeMax < ifout_compr.measurementRangeMax:
                        ifout_compr = data["irs2381/ifout_compr"]
            if calib is None or ifout_compr is None:
                raise RuntimeError("Could not grab algo debug frame from specified address.")
            f2 = proc_algo_debug(calib, ifout_compr)
            frame.update({
                'D': f2["D"],
                'X': f2["X"],
                'Y': f2["Y"],
                'Z': f2["Z"],
            })
        
    finally:
        o3r.set(oldConfig)
    return frame 

def proc_algo_debug(calib, ifout_compr):
    # ignore the currently parametrized calibration
    opticToUserTrans = np.array([getattr(calib.intrinsicCalibration.camRefToOpticalSystem, "trans"+a) for a in "XYZ"])
    opticToUserRot = np.array([getattr(calib.intrinsicCalibration.camRefToOpticalSystem, "rot"+a) for a in "XYZ"])
    X,Y,Z,D = o3r_uncompress_di.xyzdFromDistance(np.array(ifout_compr.distance), ifout_compr.distanceResolution, 
                                                 opticToUserTrans, opticToUserRot,
                                                 ifout_compr.intrinsicCalib.modelID,
                                                 ifout_compr.intrinsicCalib.modelParameters,
                                                 ifout_compr.width, ifout_compr.height)
    A = o3r_uncompress_di.convertAmplitude(np.array(ifout_compr.amplitude), ifout_compr.amplitudeResolution, ifout_compr.width, ifout_compr.height)
    R = np.reshape(ifout_compr.reflectivity, (ifout_compr.height, ifout_compr.width))
    res = dict(X=X,Y=Y,Z=Z,D=D,A=A,R=R,C=np.reshape(ifout_compr.confidence[:A.size], A.shape),
               camRefToOpticalSystem=dict(trans=opticToUserTrans,rot=opticToUserRot),
               intrinsic=dict(modelID=ifout_compr.intrinsicCalib.modelID,modelParameters=np.array(ifout_compr.intrinsicCalib.modelParameters)),
               inverseIntrinsic=dict(modelID=ifout_compr.inverseIntrinsicCalib.modelID,modelParameters=np.array(ifout_compr.inverseIntrinsicCalib.modelParameters)),
               )
    return res

def set_extrinsic_zero(o3r_object, port, mode):
    port=f"port{port}"
    logger.info("Resetting /ports/%s", port)
    o3r_object.reset("/ports/%s" % port)
    o3r_object.set({'ports':{port:{'state':'CONF', 'mode': mode}}})
    o3r_object.set({'ports':{port:{'processing':{'extrinsicHeadToUser': {'rotX': 0.0,'rotY': 0.0, 'rotZ': 0.0, 'transX': 0.0, 'transY': 0.0, 'transZ': 0.0}}}}})
    o3r_object.set({'ports':{port:{'state':'RUN'}}})

    return o3r_object

def grab_ifm3d_frame(ip, port, mode):
    ifm3dpy_version = tuple(int(x.split("+")[0]) for x in ifm3dpy.__version__.split(".")[:3])
    if ifm3dpy_version <= (1,0,0):
        raise RuntimeError("Need a later version due to issues in ifm3dpy 1.0.0")
    if mode == "extrinsic_calib" and ifm3dpy_version <= (1,2,2):
        raise RuntimeError("Need a later version of ifm3dpy for using extrinsic_calib mode")
    # updated API
    o3r = ifm3dpy.O3R(ip=ip)
    final_port = o3r.get([f"/ports/port{port}/data/pcicTCPPort"])["ports"][f"port{port}"]["data"]["pcicTCPPort"]
    oldConfig=o3r.get([f"/ports/port{port}"])
    try:
        o3r=set_extrinsic_zero(o3r, port, mode)
        frame_grabber=ifm3dpy.FrameGrabber(o3r,pcic_port=final_port)
        frame_grabber.start()
        ok, frame = frame_grabber.wait_for_frame().wait_for(timeout_ms=10000)
        if not ok:
            raise ValueError #Exception('fg-timeout on ' + port + ' reached')
        xyz=frame.get_buffer(ifm3dpy.buffer_id.XYZ)
        ampl=frame.get_buffer(ifm3dpy.buffer_id.NORM_AMPLITUDE_IMAGE)
        conf=frame.get_buffer(ifm3dpy.buffer_id.CONFIDENCE_IMAGE)
        dist=frame.get_buffer(ifm3dpy.buffer_id.RADIAL_DISTANCE_IMAGE)
        refl=frame.get_buffer(ifm3dpy.buffer_id.REFLECTIVITY)
        invIntrinsic = frame.get_buffer(ifm3dpy.buffer_id.INVERSE_INTRINSIC_CALIBRATION).tobytes()
        invIntrinsicModelID, *invIntrinsicModelParams = struct.unpack("<I32f", invIntrinsic)
        extrinsics = frame.get_buffer(ifm3dpy.buffer_id.EXTRINSIC_CALIB).flatten()
        result = {
            'A': ampl,
            'C': conf,
            'D': dist,
            'X': xyz[:,:,0],
            'Y': xyz[:,:,1],
            'Z': xyz[:,:,2],
            'R': refl,
            'inverseIntrinsic': dict(modelID=invIntrinsicModelID,modelParameters=invIntrinsicModelParams),
            'camRefToOpticalSystem': dict(trans=extrinsics[0:3], rot=extrinsics[3:6])
        }
        if mode == "extrinsic_calib":
            # need to grab another frame with "normal" mode for validation purpose
            frame_grabber.stop()
            frame_grabber=ifm3dpy.FrameGrabber(o3r,pcic_port=final_port)
            o3r = set_extrinsic_zero(o3r, port, "standard_range4m")
            frame_grabber.start()
            ok, frame = frame_grabber.wait_for_frame().wait_for(timeout_ms=10000)
            if not ok:
                raise ValueError #Exception('fg-timeout on ' + port + ' reached')
            xyz=frame.get_buffer(ifm3dpy.buffer_id.XYZ)
            dist=frame.get_buffer(ifm3dpy.buffer_id.RADIAL_DISTANCE_IMAGE)
            invIntrinsic = frame.get_buffer(ifm3dpy.buffer_id.INVERSE_INTRINSIC_CALIBRATION).tobytes()
            invIntrinsicModelID, *invIntrinsicModelParams = struct.unpack("<I32f", invIntrinsic)
            extrinsics = frame.get_buffer(ifm3dpy.buffer_id.EXTRINSIC_CALIB).flatten()
            result.update({
                'D': dist,
                'X': xyz[:,:,0],
                'Y': xyz[:,:,1],
                'Z': xyz[:,:,2],
                'inverseIntrinsic': dict(modelID=invIntrinsicModelID,modelParameters=invIntrinsicModelParams),
                'camRefToOpticalSystem': dict(trans=extrinsics[0:3], rot=extrinsics[3:6])
            })
    finally:
        o3r.set(oldConfig)
    return result
