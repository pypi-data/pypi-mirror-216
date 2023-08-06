from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.IBridge import IBridge
from vonage_cloud_runtime.session.ISession import ISession
from vonage_cloud_runtime.providers.state.IState import IState
from vonage_cloud_runtime.providers.state.contracts.IStateCommand import IStateCommand
from vonage_cloud_runtime.providers.state.contracts.stateCommand import StateCommand
from vonage_cloud_runtime.providers.state.enums.stateOperations import StateOperations
from vonage_cloud_runtime.request.enums.requestVerb import REQUEST_VERB
from vonage_cloud_runtime.providers.state.enums.expireOption import EXPIRE_OPTION
from vonage_cloud_runtime.request.contracts.requestParams import RequestParams
T = TypeVar('T')
@dataclass
class State(IState):
    session: ISession
    bridge: IBridge
    url: str
    namespace: str
    provider: str = field(default = "client-persistence-api")
    def __init__(self,session: ISession,namespace: str = None):
        self.bridge = session.bridge
        self.url = session.config.getExecutionUrl(self.provider)
        if namespace is None:
            self.namespace = f'state:{session.id}'
        
        else: 
            self.namespace = namespace
        
        self.session = session
    
    def createCommand(self,op: str,key: str,args: List[str]):
        return StateCommand(op,self.namespace,key,args)
    
    async def executeCommand(self,command: IStateCommand):
        requestParams = RequestParams()
        requestParams.method = REQUEST_VERB.POST
        requestParams.url = self.url
        requestParams.headers = self.session.constructRequestHeaders()
        requestParams.data = command
        return await self.session.request(requestParams)
    
    async def set(self,key: str,value: T):
        payload = []
        payload.append(self.bridge.jsonStringify(value))
        command = self.createCommand(StateOperations.SET,key,payload)
        return await self.executeCommand(command)
    
    async def get(self,key: str):
        payload = []
        command = self.createCommand(StateOperations.GET,key,payload)
        result = await self.executeCommand(command)
        if result is not None and result != "":
            return self.bridge.jsonParse(result)
        
        return None
    
    async def delete(self,key: str):
        payload = []
        command = self.createCommand(StateOperations.DEL,key,payload)
        return await self.executeCommand(command)
    
    async def increment(self,key: str,value: int):
        args = [self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.INCRBY,key,args)
        response = await self.executeCommand(command)
        return self.bridge.jsonParse(response)
    
    async def decrement(self,key: str,value: int):
        args = [self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.DECRBY,key,args)
        response = await self.executeCommand(command)
        return self.bridge.jsonParse(response)
    
    async def expire(self,key: str,seconds: int,option: EXPIRE_OPTION = None):
        args = [self.bridge.jsonStringify(seconds)]
        if option is not None:
            args.append(option)
        
        command = self.createCommand(StateOperations.EXPIRE,key,args)
        return await self.executeCommand(command)
    
    async def mapDelete(self,htable: str,keys: List[str]):
        command = self.createCommand(StateOperations.HDEL,htable,keys)
        return await self.executeCommand(command)
    
    async def mapExists(self,htable: str,key: str):
        payload = [key]
        command = self.createCommand(StateOperations.HEXISTS,htable,payload)
        return await self.executeCommand(command)
    
    async def mapGetAll(self,htable: str):
        payload = []
        command = self.createCommand(StateOperations.HGETALL,htable,payload)
        response = await self.executeCommand(command)
        result = {}
        for i in range(0,response.__len__(),2):
            result[response[i]] = response[i + 1]
        
        return result
    
    async def mapGetMultiple(self,htable: str,keys: List[str]):
        command = self.createCommand(StateOperations.HMGET,htable,keys)
        response = await self.executeCommand(command)
        result = []
        for i in range(0,response.__len__()):
            result.append(response[i])
        
        return result
    
    async def mapGetValues(self,htable: str):
        payload = []
        command = self.createCommand(StateOperations.HVALS,htable,payload)
        response = await self.executeCommand(command)
        result = []
        for i in range(0,response.__len__()):
            result.append(response[i])
        
        return result
    
    async def mapGetValue(self,htable: str,key: str):
        payload = [key]
        command = self.createCommand(StateOperations.HGET,htable,payload)
        return await self.executeCommand(command)
    
    async def mapSet(self,htable: str,keyValuePairs: Dict[str,str]):
        payload = []
        keys = self.bridge.getObjectKeys(keyValuePairs)
        for i in range(0,keys.__len__()):
            payload.append(keys[i])
            payload.append(keyValuePairs[keys[i]])
        
        command = self.createCommand(StateOperations.HSET,htable,payload)
        return await self.executeCommand(command)
    
    async def mapIncrement(self,htable: str,key: str,value: int):
        payload = [key,self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.HINCRBY,htable,payload)
        return await self.executeCommand(command)
    
    async def mapLength(self,htable: str):
        payload = []
        command = self.createCommand(StateOperations.HLEN,htable,payload)
        return await self.executeCommand(command)
    
    async def mapScan(self,htable: str,cursor: str,pattern: str,count: int):
        payload = [cursor,"MATCH",pattern,"COUNT",self.bridge.jsonStringify(count)]
        command = self.createCommand(StateOperations.HSCAN,htable,payload)
        return await self.executeCommand(command)
    
    async def listAppend(self,list: str,value: T):
        payload = [self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.RPUSH,list,payload)
        return await self.executeCommand(command)
    
    async def listEndPop(self,list: str,count: int = 1):
        args = [self.bridge.jsonStringify(count)]
        command = self.createCommand(StateOperations.RPOP,list,args)
        response = await self.executeCommand(command)
        return self.parseResponse(response)
    
    async def listPrepend(self,list: str,value: T):
        payload = [self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.LPUSH,list,payload)
        return await self.executeCommand(command)
    
    async def listStartPop(self,list: str,count: int = 1):
        args = [self.bridge.jsonStringify(count)]
        command = self.createCommand(StateOperations.LPOP,list,args)
        response = await self.executeCommand(command)
        return self.parseResponse(response)
    
    async def listRemove(self,list: str,value: T,count: int = 0):
        args = [self.bridge.jsonStringify(count),self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.LREM,list,args)
        return await self.executeCommand(command)
    
    async def listLength(self,list: str):
        payload = []
        command = self.createCommand(StateOperations.LLEN,list,payload)
        return await self.executeCommand(command)
    
    async def listRange(self,list: str,startPos: int = 0,endPos: int = -1):
        args = [self.bridge.jsonStringify(startPos),self.bridge.jsonStringify(endPos)]
        command = self.createCommand(StateOperations.LRANGE,list,args)
        response = await self.executeCommand(command)
        return self.parseResponse(response)
    
    async def listTrim(self,list: str,startPos: int,endPos: int):
        args = [self.bridge.jsonStringify(startPos),self.bridge.jsonStringify(endPos)]
        command = self.createCommand(StateOperations.LTRIM,list,args)
        return await self.executeCommand(command)
    
    async def listInsert(self,list: str,before: bool,pivot: T,value: T):
        direction = "AFTER"
        if before is True:
            direction = "BEFORE"
        
        args = [direction,self.bridge.jsonStringify(pivot),self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.LINSERT,list,args)
        return await self.executeCommand(command)
    
    async def listIndex(self,list: str,position: int):
        args = [self.bridge.jsonStringify(position)]
        command = self.createCommand(StateOperations.LINDEX,list,args)
        response = await self.executeCommand(command)
        return self.bridge.jsonParse(response)
    
    async def listSet(self,list: str,position: int,value: T):
        args = [self.bridge.jsonStringify(position),self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.LSET,list,args)
        return await self.executeCommand(command)
    
    def parseResponse(self,response: List[str]):
        result = []
        if response is not None:
            for i in range(0,response.__len__()):
                result.append(self.bridge.jsonParse(response[i]))
            
        
        return result
    
    def reprJSON(self):
        result = {}
        dict = asdict(self)
        keywordsMap = {"from_":"from","del_":"del","import_":"import","type_":"type"}
        for key in dict:
            val = getattr(self, key)

            if val is not None:
                if type(val) is list:
                    parsedList = []
                    for i in val:
                        if hasattr(i,'reprJSON'):
                            parsedList.append(i.reprJSON())
                        else:
                            parsedList.append(i)
                    val = parsedList

                if hasattr(val,'reprJSON'):
                    val = val.reprJSON()
                if key in keywordsMap:
                    key = keywordsMap[key]
                result.__setitem__(key.replace('_hyphen_', '-'), val)
        return result
