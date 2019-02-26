from sys import platform
import ctypes
import os
import logging

'''Code for creating a directory ND_HOME/log in which log files will be written'''

if platform == "linux" or platform == "linux2":
    path = "ND_HOME/log"
    try:
        if os.path.exists(path):
            print("Path already exists")
        else:
            os.makedirs(path)
    except OSError:
        print("Creation of directory failed %s " % path)

elif platform == "win32":
    path = "ND_HOME\log"
    try:
        if os.path.exists(path):
            print("Path already exists")
        else:
            os.makedirs(path)
    except OSError:
        print("Creation of directory failed")


elif platform == "darwin":
    path = "/ND_HOME/log"
    try:
        if os.path.exists(path):
            print("Path already exists")
        else:
            os.makedirs(path)
    except OSError:
        print("Creation of directory failed")

'''code for logging into the path by reading contents from ndsettings to /models/config.py'''


class MyFileHandler(object):
    def __init__(self, dir, logger, handlerFactory, format, **kw):
        kw['filename'] = os.path.join(dir, logger.name)
        self._handler = handlerFactory(**kw)

    def __getattr__(self, n):
        if hasattr(self._handler, n):
            return getattr(self._handler, n)
        # raise AttributeError


logger = logging.getLogger(__name__)
f_handler = logging.FileHandler('agentlogs')
f_handler.setLevel(logging.WARNING)
f_format = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s')
f_handler.setFormatter(f_format)
f_handler = MyFileHandler(path, logger, logging.FileHandler, f_format)
logger.addHandler(f_handler)
for i in range(10):
    logger.warn('Hello this is testing for logger file')

f = open('/home/cavisson/work/nsecom/ndsettings.conf', 'r')
contents = f.read()
f1 = open('/home/cavisson/work/pythonagent/agent/models/config.py', 'w+')
try:
    f1.write(contents)
except OSError:
    print("Not able to write")
else:
    print("Successfully written")

'''Using ctypes in python to Call C APIs for proxy server'''


class Threshold(ctypes.Structure):
    _fields_ = [('slow', ctypes.c_int),
                ('very_slow', ctypes.c_int)]


# th = Threshold(1,2)


class BTObject(ctypes.Structure):
    _fields_ = [('bt_name', ctypes.c_char * 512),
                ('bt_category', ctypes.c_char_p),
                ('is_meta_data_dumped', ctypes.c_int),
                ('bt_id', ctypes.c_int),
                ('bt_startTime', ctypes.c_longlong),
                ('bt_endTime', ctypes.c_longlong),
                ('dd_IntervalTime', ctypes.c_longlong),
                ('AIFlag', ctypes.c_char_p),
                ('bt_threshold', Threshold),
                ('enableBodyCapture', ctypes.c_int),
                ('maxBodySize', ctypes.c_int)]


# btO = BTObject(b'aaaa', b"123", 1,2,3,4,5, b"333", th, 6,7)
# print(btO.bt_name, btO.bt_category, btO.is_meta_data_dumped, btO.bt_threshold.slow, btO.bt_threshold.very_slow)


class sqlProp(ctypes.Structure):
    _fields_ = [('DBCallDepth', ctypes.c_int),
                ('sqlId', ctypes.c_longlong),
                ('startTime', ctypes.c_longlong),
                ('backendId', ctypes.c_longlong)]


# sqlP = sqlProp(1,2,3,4)
# print(sqlP.DBCallDepth, sqlP.sqlId, sqlP.startTime)


class NDBTMonitorDataCounters(ctypes.Structure):
    _fields_ = [('count', ctypes.c_int),
                ('duration', ctypes.c_longlong),
                ('minDuration', ctypes.c_longlong),
                ('maxDuration', ctypes.c_longlong),
                ('cpuTime', ctypes.c_longlong),
                ('minCpuTime', ctypes.c_longlong),
                ('maxCpuTime', ctypes.c_longlong),
                ('normalCount', ctypes.c_int),
                ('normalDuration', ctypes.c_longlong),
                ('minNormalDuration', ctypes.c_longlong),
                ('maxNormalDuration', ctypes.c_longlong),
                ('slowCount', ctypes.c_int),
                ('slowDuration', ctypes.c_longlong),
                ('minSlowDuration', ctypes.c_longlong),
                ('maxSlowDuration', ctypes.c_longlong),
                ('verySlowCount', ctypes.c_int),
                ('verySlowDuration', ctypes.c_longlong),
                ('minVerySlowDuration', ctypes.c_longlong),
                ('maxVerySlowDuration', ctypes.c_longlong),
                ('errorCount', ctypes.c_int),
                ('errorDuration', ctypes.c_longlong),
                ('minErrorDuration', ctypes.c_longlong),
                ('maxErrorDuration', ctypes.c_longlong),
                ('waitCount', ctypes.c_int),
                ('cumWaitTime', ctypes.c_longlong),
                ('minWaitTime', ctypes.c_longlong),
                ('maxWaitTime', ctypes.c_longlong),
                ('syncCount', ctypes.c_int),
                ('cumSyncTime', ctypes.c_longlong),
                ('minSyncTime', ctypes.c_longlong),
                ('maxSyncTime', ctypes.c_longlong),
                ('queueCount', ctypes.c_int),
                ('minQueueTime', ctypes.c_longlong),
                ('maxQueueTime', ctypes.c_longlong),
                ('cumQueueTime', ctypes.c_longlong),
                ('tlBTObj', BTObject),
                ('dataExist', ctypes.c_char_p)]


# ndbt = NDBTMonitorDataCounters(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,btO,"a")
# print(ndbt.tlBTObj.bt_name, ndbt.dataExist)


class methodArgList_t(ctypes.Structure):
    _fields_ = [('argName', ctypes.c_char_p),
                ('type', ctypes.c_char_p)]


# md = methodArgList_t("1","2")
# print(md.argName, md.type)


class methodPropProperties(ctypes.Structure):
    _fields_ = [('type', ctypes.c_char_p),
                ('callOutValue', ctypes.c_char_p),
                ('moduleName', ctypes.c_char_p * 128),
                ('methodName', ctypes.c_char_p),
                ('customCalloutName', ctypes.c_char_p),
                ('aliasMethodName', ctypes.c_char_p),
                ('methodRetType', ctypes.c_char_p),
                ('methodId', ctypes.c_int),
                ('isEntryPoint', ctypes.c_int),
                ('usedFlag', ctypes.c_int),
                ('instrumentationProp', ctypes.c_int),
                ('instrumentationStatus', ctypes.c_int),
                ('isAsyncCall', ctypes.c_int),
                ('methodArgsListCount', ctypes.c_uint),
                ('methodArgList', methodArgList_t),
                ('customCalloutptr', ctypes.c_voidp)]


# # mp = methodPropProperties("1", "2","3","4","5","6","7",8,9,10,11,12,13,14, md, None)
# # print(mp.type, mp.customCalloutptr, mp.aliasMethodName)


class NDBackendMonitorDataCounters(ctypes.Structure):
    _fields_ = [('cumCount', ctypes.c_longlong),
                ('count', ctypes.c_longlong),
                ('errorCount', ctypes.c_longlong),
                ('duration', ctypes.c_longlong),
                ('minDuration', ctypes.c_longlong),
                ('maxDuration', ctypes.c_longlong),
                ('mpp', methodPropProperties),
                ('dataExist', ctypes.c_char_p)]


# # ndB = NDBackendMonitorDataCounters(1,2,3,4,5,6,mp, "yes")
# # print(ndB.count, ndB.mpp.aliasMethodName)


class NDMethodMonitorDataCounters(ctypes.Structure):
    _fields_ = [('count', ctypes.c_int),
                ('cumCount', ctypes.c_int),
                ('duration', ctypes.c_longlong),
                ('minDuration', ctypes.c_longlong),
                ('maxDuration', ctypes.c_longlong),
                ('mpp', methodPropProperties),
                ('dataExist', ctypes.c_char_p)]


# # ndMM = NDMethodMonitorDataCounters(1,2,3,4,5,mp, "n")
# # print(ndMM.minDuration, ndMM.dataExist)


class NDMonitorDataModel(ctypes.Structure):
    _fields_ = [('currentSizeOfBTArray', ctypes.c_int),
                ('currentSizeOfBackendArray', ctypes.c_int),
                ('currentSizeOfMethodArray', ctypes.c_int),
                ('lastUpdateTimeStamp', ctypes.c_longlong),
                ('lockForBT', ctypes.c_void_p),
                ('lockForMM', ctypes.c_void_p),
                ('lockForIP', ctypes.c_void_p),
                ('btmDataArray', NDBTMonitorDataCounters),
                ('mmDataArray', NDMethodMonitorDataCounters),
                ('ipmDataArray', NDBackendMonitorDataCounters)]


# # ndMD = NDMonitorDataModel(1,2,3,4,None,None,None,ndbt,ndMM,ndB)
# # print(ndMD.lockForBT, ndMD.lastUpdateTimeStamp)


class NDPerThreadData_t(ctypes.Structure):
    _fields_ = [('tlTierBackendName', ctypes.c_char_p),
                ('tlIsFPCaptured', ctypes.c_char_p),
                ('tlIsBTExcluded', ctypes.c_char_p),
                ('tlIsForceDump', ctypes.c_char_p),
                ('prevTierSeq', ctypes.c_char_p),
                ('seqPfx', ctypes.c_char_p),
                ('tlFPInstanceForFPHdr', ctypes.c_char_p),
                ('reqURI', ctypes.c_char_p),
                ('backendMetaRecord', ctypes.c_char_p),
                ('trxId', ctypes.c_char_p),
                ('methodRecord', ctypes.c_char_p),
                ('tlCorrelationIdHeader', ctypes.c_char_p * 128),
                ('tlLogHttpConditionFlowpath', ctypes.c_char_p),
                ('tlFirstTierFPID', ctypes.c_char_p),
                ('tlLogCompleteFlowPath', ctypes.c_char_p),
                ('currThreadSeq', ctypes.c_char_p),
                ('tlThreadFromPool', ctypes.c_char_p),
                ('sequenceBlob', ctypes.c_char_p * 512),
                ('tlIsFPHeaderDumped', ctypes.c_char_p),
                ('tlCategory', ctypes.c_char_p),
                ('isHttpCallOut', ctypes.c_char_p),
                ('tlCassandraSQL', ctypes.c_char_p),
                ('tlCassandraAdd', ctypes.c_char_p),
                ('tlFPSeqBlockRecordBuffer', ctypes.c_char_p),
                ('tlURL', ctypes.c_char_p * 512),
                ('tlURLParameters', ctypes.c_char_p * 512),
                ('tlUnCaughtExceptionCount', ctypes.c_short),
                ('tlExceptionCount', ctypes.c_short),
                ('tlTierBackendType', ctypes.c_int),
                ('tlStatusCode', ctypes.c_int),
                ('byteArray', ctypes.c_int),
                ('tlServiceMethodDepth', ctypes.c_int),
                ('tlServiceMethodId', ctypes.c_int),
                ('tlServiceMethodCount', ctypes.c_int),
                ('sequenceBlobLen', ctypes.c_int),
                ('tlNonServiceMethodCount', ctypes.c_int),
                ('tlSyntheticMonitor', ctypes.c_int),
                ('tlTargetDepth', ctypes.c_int),
                ('httpCallOutDepth', ctypes.c_int),
                ('flowpathInstanceStr', ctypes.c_char_p),
                ('flowpathInstance', ctypes.c_longlong),
                ('tlsIdx', ctypes.c_longlong),
                ('seqNum', ctypes.c_longlong),
                ('tlTestRunNumber', ctypes.c_longlong),
                ('tlSeqNumberForTierCallOut', ctypes.c_longlong),
                ('tlFlowPathTimeStampInMS', ctypes.c_longlong),
                ('tlThreadId', ctypes.c_longlong),
                ('tlFpCPUTime', ctypes.c_longlong),
                ('tlDuration', ctypes.c_longlong),
                ('firstFlowpathInstance', ctypes.c_longlong),
                ('prevFlowpathInstance', ctypes.c_longlong),
                ('tlBackendSubType', ctypes.c_longlong),
                ('tlTierStartTime', ctypes.c_longlong),
                ('tierCallOutHeader', ctypes.c_char_p),
                ('tierCallOutHeaderLen', ctypes.c_int),
                ('tierCallOutSeqNum', ctypes.c_longlong),
                ('tlBTObj', BTObject),
                ('tlSQLObj', sqlProp),
                ('tlMonitorDataModel', NDMonitorDataModel),
                ('hasMapNodePtr', ctypes.c_voidp),
                ('free_next', ctypes.c_voidp),
                ('free_prev', ctypes.c_voidp),
                ('busy_next', ctypes.c_voidp),
                ('busy_prev', ctypes.c_voidp),
                ('setEndFPFlag', ctypes.c_char_p),
                ('ndSessionId', ctypes.c_longlong),
                ('prev_fp_start_time', ctypes.c_longlong),
                ('instrumented', ctypes.c_int),
                ('btCategory', ctypes.c_int),
                ('exceptionCount', ctypes.c_int),
                ('totalFpcount', ctypes.c_int),
                ('tierID', ctypes.c_int),
                ('ndAppServerID', ctypes.c_int),
                ('appID', ctypes.c_int),
                ('tlFlowpathType', ctypes.c_int),
                ('cavSID', ctypes.c_longlong),
                ('NDPageID', ctypes.c_longlong),
                ('last_fptimestamp_from_cookie', ctypes.c_longlong),
                ('agentThreadID', ctypes.c_longlong),
                ('syncTime', ctypes.c_longlong),
                ('waitTime', ctypes.c_longlong),
                ('qTimeInMS', ctypes.c_longlong),
                ('debugModeLen', ctypes.c_int),
                ('debugModeBuf', ctypes.c_char_p * 128),
                ('bitFlags', ctypes.c_int),
                ('sequenceBlobLock', ctypes.c_voidp),
                ('updateBTLock', ctypes.c_voidp),
                ('excepMessage', ctypes.c_char_p),
                ('dumpERecordFlag', ctypes.c_int),
                ('unwindfID', ctypes.c_ulonglong),
                ('exceptionFlagForEventType', ctypes.c_int),
                ('excepClassName', ctypes.c_char_p),
                ('throwingCName', ctypes.c_char_p),
                ('throwingMName', ctypes.c_char_p)]


# '''Importing and using the C APIs from .so'''

def wrapper_func(lib, funcname, restype, argtypes):
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func


libc = ctypes.CDLL('./libcontrol.so')
print(libc)


agent_init = wrapper_func(libc, 'agent_init', None,
                          [ctypes.POINTER(ctypes.c_char), ctypes.c_int, ctypes.POINTER(ctypes.c_char),
                           ctypes.POINTER(ctypes.c_char)])


startFP = wrapper_func(libc, 'startFP', ctypes.POINTER(NDPerThreadData_t),
                       [ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char),
                        ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char),
                        ctypes.POINTER(ctypes.c_char)
                           , ctypes.c_longlong, ctypes.c_longlong])


ndMethodEntry = wrapper_func(libc, 'ndMethodEntry', None,
                             [ctypes.POINTER(ctypes.c_char), ctypes.POINTER(NDPerThreadData_t),
                              ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char),
                              ctypes.POINTER(ctypes.c_char), ctypes.c_longlong, ctypes.POINTER(ctypes.c_char),
                              ctypes.POINTER(ctypes.c_char), ctypes.c_longlong])


ndMethodExit = wrapper_func(libc, 'ndMethodExit', None,
                            [ctypes.POINTER(ctypes.c_char), ctypes.POINTER(NDPerThreadData_t),
                             ctypes.POINTER(ctypes.c_char), ctypes.c_longlong, ctypes.c_int,
                             ctypes.POINTER(ctypes.c_char), ctypes.c_longlong, ctypes.c_longlong, ctypes.c_longlong,
                             ctypes.POINTER(ctypes.c_char), ctypes.c_longlong])


endFP = wrapper_func(libc, 'endFP', None, [ctypes.POINTER(NDPerThreadData_t), ctypes.c_int, ctypes.c_char_p])

agent_init("Python", 1, "Python", "Python")

import time

time.sleep(60)
for i in range(1001):
    ndTD = startFP(None, "'\'", None, None, None, None, None, 0, 0)
    for j in range(101):
        ndMethodEntry(None, ndTD, 'ABC', None, "'\'", 0, None, None, 0)
        ndMethodExit(None, ndTD, 'ABC', 0, 200, None, 1, 0, 0, None, 1)
        print(j, )

    endFP(ndTD, 200, None)










