from typing import Any, Dict, Iterable, List, Optional, Union
from gpt4all import GPT4All

class GPT:

    def __init__(self):
        self.models: list[GPT4All] = [GPT4All("orca-mini-3b-gguf2-q4_0.gguf"),
                                      GPT4All("orca-mini-3b-gguf2-q4_0.gguf")]
        self.numModels: int = len(self.models)
        self.chatSessions = [i.chat_session() for i in self.models]
        self.startAllChatSessions()

    def startChatSession(self, modelIndex: int) -> None:
        self.chatSessions[modelIndex].__enter__()

    def endChatSession(self, modelIndex: int) -> None:
        self.chatSessions[modelIndex].__exit__(None,None,None)

    def startAllChatSessions(self) -> None:
        for i in self.chatSessions:
            i.__enter__()

    def endAllChatSessions(self) -> None:
        for i in self.chatSessions:
            i.__exit__(None,None,None)

    def getChatHistory(self, modelIndex: int) -> List[Dict[str, str]]:
        return self.models[modelIndex].current_chat_session

    def generateSimple(self, modelIndex: int, prompt: str, max_tokens: int = 200,
                       temp: float = 0.7) -> (str | Iterable[str]):
        return self.models[modelIndex].generate(prompt, max_tokens, temp)
