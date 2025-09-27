from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from typing import List, Dict, Any
import asyncio
from backend.core.architecture import TestCase
import json

class PlannerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, model="gpt-4-1106-preview")
        self.template = """
        Generate a detailed test case for testing a web-based number/math puzzle game at {url}.
        Consider: User interactions, Game mechanics, Edge cases, Performance aspects, Security concerns.
        Format the response as a structured test case with clear steps, expected outcomes, and validation criteria.
        """
        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    async def generate_test_case(self, url: str) -> TestCase:
        response = await self.chain.arun(url=url)
        parsed_response = self._parse_response(response)
        return TestCase(**parsed_response)

    async def generate_test_cases(self, url: str, count: int = 20) -> List[TestCase]:
        tasks = [self.generate_test_case(url) for _ in range(count)]
        test_cases = await asyncio.gather(*tasks)
        return test_cases

    def _parse_response(self, response: str) -> Dict[str, Any]:
        try:
            parsed = json.loads(response)
            return {
                "name": parsed["name"],
                "steps": parsed["steps"],
                "priority": parsed.get("priority", 1),
                "complexity": parsed.get("complexity", 0.5),
                "estimated_duration": parsed.get("estimated_duration", 300),
                "tags": parsed.get("tags", [])
            }
        except json.JSONDecodeError:
            raise ValueError("Failed to parse LLM response")