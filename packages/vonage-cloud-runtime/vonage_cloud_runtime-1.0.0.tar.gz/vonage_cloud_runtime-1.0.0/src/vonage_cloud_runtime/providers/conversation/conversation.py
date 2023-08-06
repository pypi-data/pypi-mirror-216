from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from vonage_cloud_runtime.providers.conversation.enums.conversationAction import CONVERSATION_ACTION
from vonage_cloud_runtime.session.contracts.actionPayload import ActionPayload
from vonage_cloud_runtime.providers.conversation.IConversation import IConversation
from vonage_cloud_runtime.session.ISession import ISession
from vonage_cloud_runtime.session.contracts.IFilter import IFilter
from vonage_cloud_runtime.providers.conversation.contracts.conversationPayloadWithCallback import ConversationPayloadWithCallback
from vonage_cloud_runtime.session.contracts.IPayloadWithCallback import IPayloadWithCallback
from vonage_cloud_runtime.session.contracts.command import Command
from vonage_cloud_runtime.request.contracts.requestParams import RequestParams
from vonage_cloud_runtime.request.enums.requestVerb import REQUEST_VERB

@dataclass
class Conversation(IConversation):
    session: ISession
    provider: str = field(default = "vonage-conversation")
    def __init__(self,session: ISession):
        self.session = session
    
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
