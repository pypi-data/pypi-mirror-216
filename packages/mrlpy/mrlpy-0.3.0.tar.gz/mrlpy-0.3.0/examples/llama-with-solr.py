import logging
import re
from threading import Thread
from typing import List, Any

from sentence_transformers import SentenceTransformer

from mrlpy import mcommand
from mrlpy.framework.runtime import Runtime
from mrlpy.framework.service import Service
from mrlpy.service.data.chat import ChatMessage, TextEmbeddingGenerator
from llama_cpp import Llama

Runtime.init_runtime()
logging.basicConfig(level=logging.INFO, force=True)

template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. 
If the AI does not know the answer to a question, it truthfully says it does not know. The AI ONLY uses information contained in the "Relevant Information" section and does not hallucinate.

Relevant Information:
{context}



Conversation:
{input}
ASSISTANT:"""


# .replace("{context}", "").replace("{input}", "Write a python program to generate the fibonacci sequence")


class ChatPromptManager(Service):
    def __init__(self, name):
        super(ChatPromptManager, self).__init__(name)

    def publishPrompt(self, prompt: str) -> str:
        return prompt

    def fillPrompt(self, prompt_vars: dict[str, Any]) -> str:
        temp_dict = {key: "\n".join([str(element) for element in value]) if type(value) == list else str(value) for
                     key, value in prompt_vars.items()}
        filled_prompt = template.format(**temp_dict)
        self.invoke("publishPrompt", filled_prompt)
        return filled_prompt

    # def fillPrompt(self, prompt_template: str, prompt_vars: dict[str, str]) -> str:
    #     filled_prompt = prompt_template.format(**prompt_vars)
    #     self.invoke("publishPrompt", filled_prompt)
    #     return filled_prompt


class CompletionsListener(Service):
    def __init__(self, name):
        super(CompletionsListener, self).__init__(name)

    def onPartialCompletion(self, partial):
        print(partial, end="", flush=True)

    def onCompletion(self, completion):
        print(completion, flush=True)


class LlamaCppChat(Service):
    def __init__(self, name: str):
        super().__init__(name)
        self.llama = Llama(model_path="/media/branden/DATA/git/llama.cpp/models/Manticore-13B-Chat-Pyg.ggmlv3.q5_1.bin",
                           n_threads=6,
                           n_ctx=2000, verbose=False)

    def publishPartialCompletion(self, partial: str) -> str:
        return partial

    def publishCompletion(self, completion) -> str:
        return completion

    def onPrompt(self, prompt: str) -> str:
        completion = ""
        print(f"Prompt: {prompt}")
        for partial in self.llama(prompt, stream=True, max_tokens=768):
            completion += partial["choices"][0]["text"]
            self.invoke("publishPartialCompletion", partial["choices"][0]["text"])
        self.invoke("publishCompletion", completion)
        return completion


class MiniLMEmbeddings(Service, TextEmbeddingGenerator):
    def __init__(self, name):
        super().__init__(name)
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def generateEmbeddings(self, words: str) -> List[float]:
        embeddings = self.embedding_model.encode(words).tolist()
        self.invoke("publishEmbeddings", embeddings)
        return embeddings

    def publishEmbeddings(self, embeddings: List[float]) -> List[float]:
        return embeddings

    def onRecallMemories(self, memories: List[ChatMessage]):
        # chr(92) is newline, Python just doesn't let you do '\n' inside f-string curly braces
        print(f"Memories:\n{chr(92).join([memory.speaker + ': ' + memory.message for memory in memories])}")

    def onText(self, text):
        self.generateEmbeddings(text)


class CommandLineInputPublisher(Service):
    def __init__(self, name):
        super(CommandLineInputPublisher, self).__init__(name)
        self.thread: Thread
        self.prompt = "USER: "

    def publishText(self, words: str) -> str:
        return words

    def inputLoop(self):
        while True:
            self.invoke("publishText", input(self.prompt))


class PairAssembler(Service):
    def __init__(self, name):
        super(PairAssembler, self).__init__(name)
        self.have_first = False
        self.have_second = False
        self.first = None
        self.second = None
        self.reset_first = True
        self.reset_second = True

    def publishPair(self, first, second) -> (Any, Any):
        return first, second

    def setFirst(self, first):
        self.first = first
        self.have_first = True
        if self.have_second:
            self.have_first = False if self.reset_first else self.have_first
            self.have_second = False if self.reset_second else self.have_second
            self.invoke("publishPair", self.first, self.second)

    def setSecond(self, second):
        self.second = second
        self.have_second = True
        if self.have_first:
            self.have_first = False if self.reset_first else self.have_first
            self.have_second = False if self.reset_second else self.have_second
            self.invoke("publishPair", self.first, self.second)


class ChatMessageAssembler(Service):
    def __init__(self, name):
        super(ChatMessageAssembler, self).__init__(name)
        self.conversation_id = 1234
        self.speaker = "USER"

    def publishChatMessage(self, message: ChatMessage) -> ChatMessage:
        return message

    def onText(self, text):
        self.invoke("publishChatMessage",
                    ChatMessage(speaker=self.speaker, message=text, conversationId=self.conversation_id))

    # class Mapper(Service):
    #     """
    #     Setup mappings on "slots"
    #     self.setSlot1Key()
    #     self.setSlot1Value()
    #     """
    #
    #     def __init__(self, name):
    #         super(Mapper, self).__init__(name)
    #         self.required_slots = []
    #         self.slot_setter_regex = re.compile(r"^setSlot([0-9]+)(Key|Value)$")
    #         self.internal_slot_keys_mapping: dict = dict()
    #
    #     def __getattr__(self, item: str):
    #         m = self.slot_setter_regex.match(item)
    #         if not m:
    #             raise AttributeError(f"No such attribute {item} exists on object {self}")
    #
    #         slot_num = int(m.groups()[0])
    #         slot_set_type = m.groups()[1]
    #
    #         def set_slot_key(self, key):
    #             self.internal_slot_keys_mapping[slot_num] = key


class Mapper(Service):

    def __init__(self, name):
        super(Mapper, self).__init__(name)
        self.required_keys = set()
        self.internal_mapping: dict = dict()

    def addRequiredKeys(self, key: str):
        self.required_keys.add(key)

    def addMapping(self, key, value):
        self.internal_mapping[key] = value
        for required_key in self.required_keys:
            if required_key not in self.internal_mapping.keys():
                return
        self.invoke("publishMapping", self.internal_mapping)

    def publishMapping(self, mapping: dict) -> dict:
        temp_mapping = mapping.copy()
        self.internal_mapping.clear()
        return temp_mapping


def connection_done():
    print("Connection done")
    llama = LlamaCppChat("llama")
    compl = CompletionsListener("compl")
    memorize_embeddings = MiniLMEmbeddings("memorize")
    recall_embeddings = MiniLMEmbeddings("recall")
    memorize_assembler = PairAssembler("memorize_assembler")
    input_mapping_pair = PairAssembler("input_mapping_pair")
    recall_mapping_pair = PairAssembler("recall_mapping_pair")
    prompt_input_mapper = Mapper("prompt_input_mapper")
    prompt_manager = ChatPromptManager("prompt_manager")
    in_loop = CommandLineInputPublisher("in_loop")
    msg_assembler = ChatMessageAssembler("msg_assembler")
    solr = mcommand.callService("runtime", "start", ["solr", "Solr"])

    #       +-> memorize_embeddings--+
    #       |                        +--> memorize_assembler -> solr.memorize()
    # input +-> msg_assembler ----+--+
    #       |                     |
    #       |                     +-----> input_mapping_pair -------------------------+
    #       |                                                                         +--> prompt_input_mapper ----+
    #       +-> recall_embeddings --> solr.recallMemories()---> recall_mapping_pair --+                            |
    #                                                                                                              |
    #                                                                        compl <-- llama <-- prompt_manager <--+

    # solr.startEmbedded()
    msg_assembler.subscribe(in_loop.getFullName(), "publishText")
    recall_embeddings.subscribe(in_loop.getFullName(), "publishText")
    memorize_embeddings.subscribe(in_loop.name, "publishText")

    memorize_assembler.subscribe(msg_assembler.getFullName(), "publishChatMessage", memorize_assembler.getFullName(),
                                 "setFirst")

    memorize_assembler.subscribe(memorize_embeddings.getFullName(), "publishEmbeddings",
                                 memorize_assembler.getFullName(),
                                 "setSecond")

    input_mapping_pair.reset_first = False
    input_mapping_pair.setFirst("input")
    input_mapping_pair.subscribe(msg_assembler.getFullName(), "publishChatMessage",
                                 input_mapping_pair.getFullName(),
                                 "setSecond")

    solr.subscribe(memorize_assembler.getFullName(), "publishPair", solr.getFullName(), "memorize")

    solr.subscribe(recall_embeddings.getFullName(), "publishEmbeddings", solr.getFullName(), "recallMemories")
    # solr.deleteEmbeddedIndex()

    recall_mapping_pair.reset_first = False
    recall_mapping_pair.setFirst("context")
    recall_mapping_pair.subscribe(solr.getFullName(), "recallMemories", recall_mapping_pair.getFullName(), "setSecond")

    prompt_input_mapper.addRequiredKeys("context")
    prompt_input_mapper.addRequiredKeys("input")
    prompt_input_mapper.subscribe(input_mapping_pair.getFullName(), "publishPair",
                                  prompt_input_mapper.getFullName(),
                                  "addMapping")
    prompt_input_mapper.subscribe(recall_mapping_pair.getFullName(), "publishPair",
                                  prompt_input_mapper.getFullName(),
                                  "addMapping")

    prompt_manager.subscribe(prompt_input_mapper.getFullName(), "publishMapping",
                             prompt_manager.getFullName(),
                             "fillPrompt")

    llama.subscribe(prompt_manager.getFullName(), "publishPrompt")

    compl.subscribe(llama.getFullName(), "publishPartialCompletion")
    in_loop.inputLoop()

    # llama.generateCompletion(template)


Runtime.getRuntime().post_connect_hooks.append(connection_done)

mcommand.setPort("8888")
mcommand.connect(id="obsidian", daemon=False)

# for completion in llama(template, stream=True, max_tokens=768):
#     print(completion["choices"][0]["text"], end="", flush=True)
# print(mcommand.callService("solr", "recallMemories", [embedding_model.encode(turn.message).tolist()]))
# mcommand.connect(daemon=False, bypassRegisters=True)
# mcommand.sendCommand("runtime", "describe", [])
# p = mcommand.callService("runtime", "start", ["python", "Python"])
# print(p)
# print(p.__dict__)
