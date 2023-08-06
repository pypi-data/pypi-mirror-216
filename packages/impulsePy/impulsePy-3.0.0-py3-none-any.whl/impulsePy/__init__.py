import zmq
import threading
import pandas as pd
import json
import logging
import os
from time import sleep

_logger = logging.getLogger(__name__)

version = "3.1.0" # Added LSS controls and data, including line control

controlEndpoint = "tcp://127.0.0.1:5557"
dataEndpoint = "tcp://127.0.0.1:5556"

profilesPath = os.path.expanduser('~\\Documents\\Impulse\\Profiles\\')
profilesPath = profilesPath.replace("\\","/")

def createControlMessage(details):
    controlString = json.dumps(details)
    controlStringB = bytes(controlString, 'utf_8')
    return controlStringB

context = zmq.Context()
controlPool = context.socket(zmq.REQ)
controlPool.connect(controlEndpoint)

status = {}

def sendControl(controlDict, showResult=1):
    global controlPool
    controlString = createControlMessage(controlDict)
    
    # Get a connection from the pool
    controlSock = controlPool
    
    # Send the message and receive the response
    controlSock.send(controlString)
    returnMessage = json.loads(controlSock.recv())
    
    # Return the response and release the connection to the pool
    if not controlSock.closed:
        controlPool = controlSock
    else:
        controlPool = context.socket(zmq.REQ)
        controlPool.connect(controlEndpoint)
    return returnMessage

def getStatus():
    controlDict = {
        '$type' : 'control.impulse.getStatus'
        }
    returnMessage = sendControl(controlDict)
    status = returnMessage["data"]["status"]
    return status

def waitForControl():
    status = getStatus()
    logging.info("[Waiting for control] current status:", status)
    while status != "control": 
        sleep(0.2)
        newStatus = getStatus()
        if newStatus != status: 
            logging.info("[Waiting for control] new status:", newStatus)
            status = newStatus
    sleep(1) # To prevent fatal errors

class profile():
    def load(self, location):
        controlDict = {
            '$type' : 'control.profileController.loadProfile',
            'path' : location  
            }
        returnMessage = sendControl(controlDict)
        return returnMessage["resultCode"]             

    def getStatus(self):
        controlDict = {
            '$type' : 'control.impulse.getStatus'
            }
        returnMessage = sendControl(controlDict)
        return returnMessage["resultCode"]  

    def control(self, action):
        controlDict = {
            '$type' : 'control.profileController.controlProfile',
            'action' : action
            }
        returnMessage = sendControl(controlDict)
        return returnMessage["resultCode"]  

class device:
    def __init__(self, stimulus):
        self.stimulus = stimulus
        self.data = pd.DataFrame()
        self.lastSentSequence = 0
        
    def setFlag(self, flagName):
        subscriber.setFlag(flagName)
    
    def getLastData(self):
        if self.stimulus.encode() in subscriber.topics:
            if len(subscriber.topics[self.stimulus.encode()].tail(1).to_dict(orient='records'))>0:
                data = subscriber.topics[self.stimulus.encode()].tail(1).to_dict(orient='records')[0]
                self.lastSentSequence = data["sequenceNumber"]
                return data
            else:
                print("No data available...")
                return None
        else:
            print("Topic not available...")
            return None
    
    def setPointChanged(self):
        data = subscriber.topics[self.stimulus.encode()].tail(1).to_dict(orient='records')[0]
        self.lastSentSequence = data["sequenceNumber"]
        
    def getNewData(self):
        if self.stimulus.encode() in subscriber.topics:
            if len(subscriber.topics[self.stimulus.encode()])>0:
                while subscriber.topics[self.stimulus.encode()].iloc[-1]["sequenceNumber"] == self.lastSentSequence:
                    sleep(0.001)
                data = subscriber.topics[self.stimulus.encode()].tail(1).to_dict(orient='records')[0]
                self.lastSentSequence = data["sequenceNumber"]
                return data
            else:
                print("No data available...")
        else:
            print("Topic not available...")
            return None
        
    def getDataFrame(self, startExpTimeOrFlag=0, endExpTimeOrFlag=None):
        if isinstance(startExpTimeOrFlag, str):
            if startExpTimeOrFlag in subscriber.flags:
                startExpTimeOrFlag = subscriber.flags[startExpTimeOrFlag]
            else:
                logging.error(f"[ERROR] Flag {startExpTimeOrFlag} does not exist!")
                return []
        if endExpTimeOrFlag==None:
            endExpTimeOrFlag = subscriber.lastExperimentTime
        elif isinstance(endExpTimeOrFlag, str):
            if endExpTimeOrFlag in subscriber.flags:
                endExpTimeOrFlag= subscriber.flags[endExpTimeOrFlag]
            else:
                logging.error(f"[ERROR] Flag {endExpTimeOrFlag} does not exist!")
                return []
        df = subscriber.topics[self.stimulus.encode()].copy()
        df = df[(df['experimentDuration']>startExpTimeOrFlag) & (df['experimentDuration']<endExpTimeOrFlag)]
        if len(df)>1:
            df["timeStamp"] = pd.to_datetime(df['timeStamp'])
        return df
    
    def subscribe(self):
        print("Subscribing to data channels is no longer necessary in this version of impulsePy")

class heat():
    def __init__(self):
        self.stimulus = 'heat'
        self.data = device(self.stimulus)
        
    def startRamp(self, setPoint, timeOrRate, rampTimeRate):
        controlDict = {
            '$type': 'control.heat.startRamp',
            'temperature': setPoint,
            timeOrRate: rampTimeRate
        }
        resultCode = sendControl(controlDict)['resultCode']
        if resultCode == 'ok':
            status[self.stimulus]="busy"
        return resultCode

    def stopRamp(self):
        controlDict = {
            '$type': 'control.heat.stopRamp'
        }
        resultCode = sendControl(controlDict)['resultCode']
        if resultCode == 'ok':
            status[self.stimulus]="ready"
        return resultCode

    def set(self, setPoint):
        self.startRamp(setPoint, 'rampTime', 0)

class bias():
    def __init__(self):
        self.stimulus = 'bias'
        self.data = device(self.stimulus)

    def getConfiguration(self):
        controlDict = {
            '$type': 'control.bias.getConfiguration'
        }
        return sendControl(controlDict)

    def set(self, setPoint, compliance):
        controlDict = {
            '$type': 'control.bias.applyConstantBias',
            'setpoint': setPoint,
            'compliance': compliance
        }
        returnMessage = sendControl(controlDict)
        return returnMessage['resultCode']

    def startSweepCycle(self, baseline, amplitude, sweep_cycle_type, rate, cycles, compliance):
        controlDict = {
            '$type': 'control.bias.startSweepCycle',
            'baseline': baseline,
            'amplitude': amplitude,
            'sweepCycleType': sweep_cycle_type,
            'rate': rate,
            'cycles': cycles,
            'compliance': compliance
        }
        resultCode = sendControl(controlDict)['resultCode']
        if resultCode == 'ok':
            status[self.stimulus]="busy"
        return resultCode

    def stopSweepCycle(self):
        controlDict = {
            '$type': 'control.bias.stopSweepCycle'
        }
        resultCode = sendControl(controlDict)['resultCode']
        if resultCode == 'ok':
            status[self.stimulus]="ready"
        return resultCode

class gas():
    def __init__(self):
        self.stimulus = 'gas'
        self.data = device(self.stimulus)
        self.msdata = device('massSpec')
        self.gasSystemType = None
        self.controlMode = None

    def getConfiguration(self):
        controlDict = {
            '$type': 'control.gas.getConfiguration'
        }
        returnMessage = sendControl(controlDict)
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(returnMessage)
        self.gasSystemType = returnMessage['data']['$type'].split('.')[-1]
        return returnMessage

    def setBypass(self, toggleState):
        controlDict = {
            '$type': 'control.gas.setBypass',
            'state': toggleState
        }
        return sendControl(controlDict)

    def setFlowCheck(self, flow, state):
        controlDict = {
            '$type': 'control.gas.setFlowCheck',
            'state': state,
            'flow': flow
        }
        return sendControl(controlDict)

    def flushReactor(self, state):
        controlDict = {
            '$type': 'control.gas.flushReactor',
            'state': state
        }
        return sendControl(controlDict)

    def stopRamp(self):
        controlDict = {
            '$type' : 'control.gas.stopRamp'
            }
        returnMessage = sendControl(controlDict)
        if returnMessage['resultCode']=='ok':
            status[self.stimulus]="ready"
        return returnMessage["resultCode"]       
    
    def evacuateHolder(self):
        controlDict = {
            '$type' : 'control.gas.evacuateHolder'
            }
        returnMessage = sendControl(controlDict)
        return returnMessage["resultCode"]       

    def startIOPRamp(self, inletPressure, outletPressure, rampTime, gas1Flow=None, gas1FlowPath=None, gas2Flow=None, gas2FlowPath=None, gas3Flow=None, gas3FlowPath=None ):
        if self.gasSystemType is None:
            self.getConfiguration()
        controlDict = {
            '$type' : 'control.gas.' + self.gasSystemType + '.inletOutletPressure.startRamp',
            'inletPressure' : inletPressure,
            'outletPressure' : outletPressure,
            'rampTime' : rampTime
            }
        if gas1Flow is not None:
            controlDict['gas1Flow']=gas1Flow
            controlDict['gas1FlowPath']=gas1FlowPath
            controlDict['gas2Flow']=gas2Flow
            controlDict['gas2FlowPath']=gas2FlowPath            
            controlDict['gas3Flow']=gas3Flow
            controlDict['gas3FlowPath']=gas3FlowPath           
        returnMessage = sendControl(controlDict)
        if returnMessage["resultCode"] =="ok":
            status[self.stimulus]="busy"
        return returnMessage["resultCode"]
    
    def setIOP(self, inletPressure, outletPressure, gas1Flow=None, gas1FlowPath=None, gas2Flow=None, gas2FlowPath=None, gas3Flow=None, gas3FlowPath=None):
        returnMessage = self.startIOPRamp(inletPressure, outletPressure, 0, gas1Flow, gas1FlowPath, gas2Flow, gas2FlowPath, gas3Flow, gas3FlowPath)
        self.data.setPointChanged()
        return returnMessage
    
    def startPFRamp(self, reactorPressure, reactorFlow, rampTime, gasConcentrationType=None, gas1Concentration=None, gas2Concentration=None ):
        if self.gasSystemType is None:
            self.getConfiguration()
        controlDict = {
            '$type' : 'control.gas.' + self.gasSystemType + '.pressureFlow.startRamp',
            'reactorPressure' : reactorPressure,
            'reactorFlow' : reactorFlow,
            'rampTime' : rampTime
            }
        if gasConcentrationType is not None:
            controlDict['gasConcentrationType']=gasConcentrationType
            controlDict['gas1Concentration']=gas1Concentration
            controlDict['gas2Concentration']=gas2Concentration        
        returnMessage = sendControl(controlDict)
        if returnMessage["resultCode"] =="ok":
            status[self.stimulus]="busy"
        return returnMessage["resultCode"]    
    
    def setPF(self, reactorPressure, reactorFlow, gasConcentrationType=None, gas1Concentration=None, gas2Concentration=None):
        returnMessage = self.startPFRamp(reactorPressure, reactorFlow, 0, gasConcentrationType, gas1Concentration, gas2Concentration)
        self.data.setPointChanged()
        return returnMessage
    
    def initiateFlow(self, reactorPressure, reactorFlow, gasConcentrationType, gas1Concentration, gas2Concentration):
        controlDict = {
            '$type' : 'control.gas.gplus.pressureFlow.initiateFlow',
            'reactorPressure' : reactorPressure,
            'reactorFlow' : reactorFlow,
            'gasConcentrationType' : gasConcentrationType,
            'gas1Concentration' : gas1Concentration,
            'gas2Concentration' : gas2Concentration
            }        
        returnMessage = sendControl(controlDict)
        return returnMessage["resultCode"]   

    def stopInitiateFlow(self):
        controlDict = {
            '$type' : 'control.gas.gplus.pressureFlow.stopInitializingFlow',
            }        
        returnMessage = sendControl(controlDict)
        return returnMessage["resultCode"]

class liquid():
    def __init__(self):
        self.stimulus = 'liquid'
        self.data = device(self.stimulus)
        
    #v0 and v1 commands (LSS)
    def setPF(self, version, outletPressure, flow):
        controlDict = {
            '$type': 'control.liquid.'+version+'.pressureFlow.apply',
            'flow': flow,
            'outletPressure': outletPressure
        }            
        resultCode = sendControl(controlDict)['resultCode']
        return resultCode

    def setIOP(self, version, inletPressure, outletPressure):
        controlDict = {
            '$type': 'control.liquid.'+version+'.inletOutletPressure.apply',
            'inletPressure1': inletPressure,
            'outletPressure': outletPressure
        }        
        resultCode = sendControl(controlDict)['resultCode']
        return resultCode

    #v2 commands (LSS advanced)
    def setHumidity(self, setPoint):
        controlDict = {
            '$type': 'control.liquid.v2.setHumidity',
            'humidity': setPoint
        }
        resultCode = sendControl(controlDict)['resultCode']
        return resultCode
   
    def setPFC(self, outletPressure, flow, concentration):
        controlDict = {
            '$type': 'control.liquid.v2.pressureFlow.apply',
            'flow': flow,
            'concentration': concentration,
            'outletPressure': outletPressure
        }       
        resultCode = sendControl(controlDict)['resultCode']
        return resultCode
 
    def setLine(self, line):
        controlDict = {
            '$type': 'control.liquid.setLine',
            'line': line # possible values: liquid, gas
        }       
        resultCode = sendControl(controlDict)['resultCode']
        return resultCode
    
    def setI2OP(self, inletPressure1, inletPressure2, outletPressure):
        controlDict = {
            '$type': 'control.liquid.v2.inletOutletPressure.apply',
            'inletPressure1': inletPressure1,
            'inletPressure2': inletPressure2,
            'outletPressure': outletPressure
        }        
        resultCode = sendControl(controlDict)['resultCode']
        return resultCode


class apiSubscriber(threading.Thread):
    def __init__(self, endpoint):
        super().__init__()
        self.endpoint = endpoint
        self.topics = {}
        self.socket = None
        self.running = True
        self.parameterInfo = pd.DataFrame()
        self.activeChannels = []
        self.controlStatusEvent = threading.Event()
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(self.endpoint)
        self.waitForControl()
        self.updateParameters()
        self.lastExperimentTime = 0
        self.flags = {}
        self.currentFlag = ""
    
    def waitForControl(self):
        print("Waiting for control.impulse...")
        while True:
            if getStatus() == "control":
                self.controlStatusEvent.set()
                break
            sleep(1)
    
    def roundDataframeValues(self, inputDf):
        # create a copy of the input dataframe with all non-timeStamp columns rounded to the correct precision
        rounded_df = inputDf.drop(columns='timeStamp')
        for _, row in self.parameterInfo.iterrows():
            prop = row["propertyName"]
            if prop in rounded_df.columns:
                if not isinstance(rounded_df[prop][0],str):
                    precision = row["precision"]
                    rounded_df[prop] = rounded_df[prop].round(precision)
        
        # convert the timeStamp column to datetime
        rounded_df['timeStamp'] = pd.to_datetime(inputDf['timeStamp'])
        
        return rounded_df   
    
    def run(self):
        while self.running:
            try:
                message = self.socket.recv_multipart(flags=zmq.NOBLOCK)
                topic = message[0]
                data = json.loads(message[1].decode('utf-8'))
                if topic in self.topics:
                    df = pd.DataFrame([data], index=[0])
                    if topic != b"events":
                        if topic == b'massSpec':
                            for channel in df.iloc[0]['channels']:
                                df[channel['name']]=channel['measuredValue']
                            df.iloc[0].drop('channels')
                        df = self.roundDataframeValues(df)
                        df["flag"]=self.currentFlag           
                        self.lastExperimentTime = df.iloc[-1]['experimentDuration']
                    self.topics[topic] = pd.concat([self.topics[topic], df], ignore_index=True)
                if topic == b"events" and data.get("newState") == "control":
                    self.updateParameters()
                    
                if topic == b"events" and data.get("$type") == "data.event.stimulusActionFinished":
                    stimulusType = data.get("stimulusType")
                    status[stimulusType]="ready"
                    
            except zmq.Again:
                pass
    
    def subscribe(self, topic):
        if isinstance(topic, bytes):
            if topic not in self.topics:
                self.topics[topic] = pd.DataFrame()
                if self.socket:
                    self.socket.setsockopt(zmq.SUBSCRIBE, topic)
                    if topic != b'events': status[topic.decode("utf-8")]="ready"
        else:
            raise TypeError("Topic must be a bytes object")
    
    def unsubscribe(self, topic):
        if isinstance(topic, bytes):
            if topic in self.topics:
                del self.topics[topic]
                if self.socket:
                    self.socket.setsockopt(zmq.UNSUBSCRIBE, topic)
                    if topic != b'events': status[topic.decode("utf-8")]="inactive"
        else:
            raise TypeError("Topic must be a bytes object")
    
    def updateParameters(self):
        print("updating parameters...")
        controlDict = {
            '$type' : 'control.impulse.getAvailableDataChannels'
            }
        returnMessage = sendControl(controlDict)
        self.activeChannels = returnMessage["data"]["activeChannels"]
        # Create a set of current topics for fast membership testing
        currentTopics = set(self.topics.keys())
       
        # Unsubscribe from inactive topics
        for topic in currentTopics - set(self.activeChannels):
            self.unsubscribe(topic)
       
        # Subscribe to new topics
        for channel in self.activeChannels:
            if channel not in currentTopics and channel != "events":
                self.subscribe(channel.encode())

        # Update parameterInfo dataframe
        self.parameterInfo = pd.DataFrame()
        for channel in self.activeChannels:
            controlDict = {
                '$type' : 'control.impulse.getAvailableProperties',
                'channelName': channel
                }
            returnMessage = sendControl(controlDict)            
            for parameter in returnMessage['data']['properties']:
                controlDict = {
                    '$type' : 'control.impulse.getPropertyInformation',
                    "channelName": channel,
                    "propertyName": parameter
                    }                
                returnMessage = sendControl(controlDict)
                parameterDataFrame = pd.DataFrame([returnMessage['data']])
                if parameter == "experimentDuration": parameterDataFrame['precision']=3
                self.parameterInfo = pd.concat([self.parameterInfo,parameterDataFrame], ignore_index=True)
        print("Parameter info:")
        print(self.parameterInfo.filter(['channelName','propertyName','unit','precision']))

    def setFlag(self, flagName):
        self.flags[flagName]=self.lastExperimentTime
        self.currentFlag = flagName
    
    def getExperimentTime(self):
        return self.lastExperimentTime      
        
    def stop(self):
        self.running = False

def disconnect():
    subscriber.stop()
    subscriber.join()

subscriber = apiSubscriber(dataEndpoint)
subscriber.start()
subscriber.subscribe(b"events")

profile = profile()
heat = heat()
bias = bias()
gas = gas()
liquid = liquid()

def getParameterInfo():
    return subscriber.parameterInfo