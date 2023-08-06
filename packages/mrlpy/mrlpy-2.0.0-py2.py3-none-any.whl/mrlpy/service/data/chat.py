from abc import ABC, abstractmethod
from typing import List

from mrlpy.framework.interfaces import MRLInterface
from mrlpy.framework.mrl_dataclass import mrl_dataclass


@mrl_dataclass(name="org.myrobotlab.service.data.ChatMessage")
class ChatMessage:
    speaker: str
    message: str
    conversationId: int

    def __str__(self):
        return f"{self.speaker}: {self.message}"


class TextEmbeddingGenerator(MRLInterface, ABC):
    @abstractmethod
    def generateEmbeddings(self, words: str) -> List[float]:
        pass

    @abstractmethod
    def publishEmbeddings(self, embeddings: List[float]) -> List[float]:
        pass

    @classmethod
    def java_interface_name(cls) -> str:
        return "org.myrobotlab.service.interfaces.TextEmbeddingGenerator"
