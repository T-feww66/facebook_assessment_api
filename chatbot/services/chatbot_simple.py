from chatbot.utils.answer_generator import AnswerGenerator
from chatbot.utils.retriever import Retriever
from chatbot.utils.graph_state import GraphState
from chatbot.utils.llm import LLM  # noqa: I001
from langgraph.graph import END, StateGraph, START
from typing import Dict, Any

from app.config import settings


class ChatBotSimple:
    def __init__(self, path_vector_store) -> None:
        """
        Khởi tạo ChatBotSimple với các thành phần chính.
        """

        self.retriever = Retriever(settings.LLM_NAME).set_retriever(
            path_vector_store)  # Khởi tạo trình tìm kiếm tài liệu
        self.llm = LLM().get_llm(settings.GOOGLE_LLM)
        self.answer_generator = AnswerGenerator(self.llm)

    def retrieve(self, state: GraphState) -> Dict[str, Any]:
        """
        Tìm kiếm các tài liệu liên quan đến câu hỏi.

        Args:
            state (GraphState): Trạng thái hiện tại chứa câu hỏi.

        Returns:
            dict: Chứa danh sách tài liệu và câu hỏi.
        """
        question = state["question"]
        documents = self.retriever.get_documents(
            question, int(settings.NUM_DOC))
        return {"documents": documents, "question": question}

    def generate(self, state: GraphState) -> Dict[str, Any]:
        """
        Tạo câu trả lời từ câu hỏi.
        """
        question = state["question"]
        documents = state["documents"]
        context = "\n\n".join(doc.page_content for doc in documents)

        
        generation = self.answer_generator.get_chain().invoke(
            {"question": question, "context": context}
        )
        return {"generation": generation}

    def get_workflow(self):
        """
        Thiết lập luồng xử lý của chatbot.
        """
        workflow = StateGraph(GraphState)
        workflow.add_node("retrieve", self.retrieve)  # Bước tìm kiếm tài liệu
        workflow.add_node("generate", self.generate)

        workflow.add_edge(START, "retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)

        return workflow
