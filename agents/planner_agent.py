from langchain.agents import Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import json

class PlannerAgent:
    def __init__(self, llm_model="gpt-4"):
        self.llm = ChatOpenAI(model=llm_model, temperature=0.7)
        self.memory = ConversationBufferMemory()
        
    def generate_test_cases(self, game_url: str, count: int = 20) -> List[TestCase]:
        """Generate test cases for the game"""
        
        prompt = PromptTemplate(
            template="""
            Analyze the number/math puzzle game at {game_url}.
            Generate {count} comprehensive test cases covering:
            1. Basic functionality (number input, calculations)
            2. Edge cases (boundary values, invalid inputs)
            3. UI interactions (buttons, controls)
            4. Game flow (start, progress, completion)
            5. Error handling scenarios
            
            For each test case, provide:
            - Unique ID and descriptive name
            - Clear steps to execute
            - Expected outcomes
            - Priority (1-5)
            - Tags for categorization
            
            Output as JSON array.
            """,
            input_variables=["game_url", "count"]
        )
        
        response = self.llm.predict(
            prompt.format(game_url=game_url, count=count)
        )
        
        test_cases = self._parse_test_cases(response)
        return test_cases
    
    def _parse_test_cases(self, response: str) -> List[TestCase]:
        """Parse LLM response into TestCase objects"""
        try:
            data = json.loads(response)
            return [TestCase(**tc) for tc in data]
        except Exception as e:
            print(f"Error parsing test cases: {e}")
            return []