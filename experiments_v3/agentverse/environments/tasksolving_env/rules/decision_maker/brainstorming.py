from __future__ import annotations
import asyncio
from colorama import Fore

from typing import TYPE_CHECKING, List

from . import decision_maker_registry
from .base import BaseDecisionMaker
from agentverse.logging import logger

from agentverse.message import Message

if TYPE_CHECKING:
    from agentverse.agents.base import BaseAgent
    from agentverse.message import CriticMessage

@decision_maker_registry.register("brainstorming")
class BrainstormingDecisionMaker(BaseDecisionMaker):
    name: str = "brainstorming"

    async def astep(
        self,
        agents: List[BaseAgent],
        task_description: str,
        previous_plan: str = "No solution yet.",
        advice: str = "No advice yet.",
        *args,
        **kwargs,
    ) -> List[str]:
        # 조언이 있으면 먼저 브로드캐스트
        if advice != "No advice yet.":
            self.broadcast_messages(
                agents, [Message(content=advice, sender="Evaluator")]
            )

        # 모든 CriticAgent/Agent 호출
        for agent in agents[1:]:
            if hasattr(agent, "preliminary_solution"):  # CriticAgent 등
                review = await agent.astep(
                    preliminary_solution=previous_plan,
                    advice=advice,
                    task_description=task_description,
                    **kwargs
                )
            else :
                review = await agent.astep(
                    previous_plan,  # positional
                    advice,
                    task_description,
                    **kwargs
                )

            if review.content != "":
                self.broadcast_messages(agents, [review])

            logger.info(f"Reviews:")
            logger.info(f"[{review.sender}]: {review.content}", Fore.YELLOW)

        # Solver/첫 번째 에이전트 호출
        result = await agents[0].astep(
            preliminary_solution=previous_plan,
            advice=advice,
            task_description=task_description,
            **kwargs
        )

        # 메모리 초기화 후 summary 브로드캐스트
        for agent in agents:
            agent.memory.reset()

        self.broadcast_messages(
            agents,
            [
                Message(
                    content=result.content,
                    sender="Summary From Previous Discussion"
                )
            ],
        )

        return [result]

'''
@decision_maker_registry.register("brainstorming")
class BrainstormingDecisionMaker(BaseDecisionMaker):
    """
    Much like the horizontal decision maker, but with some twists:
    (1) Solver acts as a summarizer, summarizing the discussion of this turn
    (2) After summarizing, all the agents' memory are cleared, and replaced with
    the summary (to avoid exceeding maximum context length of the model too fast)
    """

    name: str = "brainstorming"

    async def astep(
        self,
        agents: List[BaseAgent],
        task_description: str,
        previous_plan: str = "No solution yet.",
        advice: str = "No advice yet.",
        *args,
        **kwargs,
    ) -> List[str]:
        if advice != "No advice yet.":
            self.broadcast_messages(
                agents, [Message(content=advice, sender="Evaluator")]
            )
        for agent in agents[1:]:
            review: CriticMessage = await agent.astep(previous_plan, advice, task_description)
            # 2025.08.13, 수정했긴 했는데 이 부분 위험한 것 같긴함 previous_plan, advice, task_description/ env_description=previous_plan
            if review.content != "":
                self.broadcast_messages(agents, [review])

            logger.info("", "Reviews:", Fore.YELLOW)
            logger.info(
                "",
                f"[{review.sender}]: {review.content}",
                Fore.YELLOW,
            )

        result = await agents[0].astep(previous_plan, advice, task_description)
        for agent in agents:
            agent.memory.reset()
        self.broadcast_messages(
            agents,
            [
                Message(
                    content=result.content, sender="Summary From Previous Discussion"
                )
            ],
        )
        return [result]
'''