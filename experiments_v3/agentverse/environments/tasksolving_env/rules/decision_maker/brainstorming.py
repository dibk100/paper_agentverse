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
    """
    Brainstorming decision maker:
    - Evaluator의 조언을 먼저 broadcast
    - CriticAgent는 keyword 인자로 astep 호출
    - ConversationAgent / Solver는 positional 인자로 astep 호출
    - Solver 결과를 Summary로 모든 agent에 broadcast 후 메모리 reset
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
    ) -> List[Message]:
        # 1. Evaluator의 조언 broadcast
        if advice != "No advice yet.":
            self.broadcast_messages(
                agents, [Message(content=advice, sender="Evaluator")]
            )

        # 2. CriticAgents (agents[1:]) 호출
        for agent in agents[1:]:
            if agent.__class__.__name__ == "CriticAgent":
                # CriticAgent: keyword 인자
                review = await agent.astep(
                    preliminary_solution=previous_plan,
                    advice=advice,
                    task_description=task_description,
                    **kwargs
                )
            elif agent.__class__.__name__ == "ConversationAgent":
                # ConversationAgent: message 하나만 전달
                review = await agent.astep(
                    task_description,
                    **kwargs
                )
            else:
                # 기타 Solver 등: 기존 positional 방식
                review = await agent.astep(
                    previous_plan,
                    advice,
                    task_description,
                    **kwargs
                )
                
            # 🔍 디버깅
            if isinstance(review, str):
                print(f"[DEBUG][Brainstorming] {agent.name} returned str: {review[:100]}")
            elif hasattr(review, "content"):
                print(f"[DEBUG][Brainstorming] {agent.name} returned Message: {review.content[:100]}")
            else:
                print(f"[DEBUG][Brainstorming] {agent.name} returned type={type(review)}")
            
            # if isinstance(review, str):
            #    review = Message(content=review, sender=agent.name)

            if review and review.content.strip() != "":
                self.broadcast_messages(agents, [review])
                try:
                    logger.info(f"[{review.sender}]: {review.content}", Fore.YELLOW)
                except Exception:
                    logger.info(f"[{review.sender}]: {review.content}")

        # 3. Solver / 첫 번째 Agent 호출
        first_agent = agents[0]
        if first_agent.__class__.__name__ == "CriticAgent":
            result = await first_agent.astep(
                preliminary_solution=previous_plan,
                advice=advice,
                task_description=task_description,
                **kwargs
            )
        elif first_agent.__class__.__name__ == "ConversationAgent":
            result = await first_agent.astep(
                task_description,
                **kwargs
            )
        else:
            result = await first_agent.astep(
                previous_plan,
                advice,
                task_description,
                **kwargs
            )
            
        # 🔍 디버깅
        if isinstance(result, str):
            print(f"[DEBUG][Brainstorming] {first_agent.name} returned str: {result[:100]}")
        elif hasattr(result, "content"):
            print(f"[DEBUG][Brainstorming] {first_agent.name} returned Message: {result.content[:100]}")
        else:
            print(f"[DEBUG][Brainstorming] {first_agent.name} returned type={type(result)}")
        # if isinstance(result, str):
        #     result = Message(content=result, sender=first_agent.name)

        # 4. 모든 agent 메모리 reset
        for agent in agents:
            agent.memory.reset()

        # 5. Summary broadcast
        self.broadcast_messages(
            agents,
            [
                Message(
                    content=result.content,
                    sender="Summary From Previous Discussion",
                )
            ],
        )

        # 6. Solver 결과 반환 (List로 래핑)
        return [result]

'''
### 2025.08.28 수정
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
                    previous_plan,
                    advice,
                    task_description,
                    **kwargs
                )

            if review.content != "":
                self.broadcast_messages(agents, [review])

            logger.info(f"Reviews:")
            logger.info(f"[{review.sender}]: {review.content}", Fore.YELLOW)

        # Solver/첫 번째 에이전트 호출
        first_agent = agents[0]
        if hasattr(first_agent, "preliminary_solution"):  # CriticAgent 등
            result = await first_agent.astep(
                preliminary_solution=previous_plan,
                advice=advice,
                task_description=task_description,
                **kwargs
            )
        else:  # ConversationAgent, Solver 등
            result = await first_agent.astep(
                previous_plan,
                advice,
                task_description,
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

### 2025.08.13
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