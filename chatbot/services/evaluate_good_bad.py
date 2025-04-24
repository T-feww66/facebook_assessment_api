from chatbot.utils.evaluate_generator import EvaluateGenerator
from chatbot.utils.graph_state import GraphState
from chatbot.utils.llm import LLM  # noqa: I001
from langgraph.graph import END, StateGraph, START
from typing import Dict, Any

from app.ai_config import settings


class EvaluateGoodBad:
    def __init__(self) -> None:
        """
        Khởi tạo ChatBotSimple với các thành phần chính.
        """
        self.llm = LLM().get_llm(settings.AI)
        self.answer_generator = EvaluateGenerator(self.llm)

    def generate(self, state: GraphState) -> Dict[str, Any]:
        """
        Tạo câu trả lời từ câu hỏi.
        """
        question = state["question"]

        generation = self.answer_generator.get_chain().invoke(
            {"question": question}
        )
        return {"generation": generation}

    def get_workflow(self):
        """
        Thiết lập luồng xử lý của chatbot.
        """
        workflow = StateGraph(GraphState)
        workflow.add_node("generate", self.generate)

        workflow.add_edge(START, "generate")
        workflow.add_edge("generate", END)
        return workflow
