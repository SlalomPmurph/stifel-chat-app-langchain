from langchain_community.llms import Ollama
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class LangChainService:
    """Service for LangChain agent interactions with Ollama"""

    def __init__(self):
        self.llm = None
        self.agent_executor = None
        self.memory = None
        self._initialize_llm()

    def _initialize_llm(self):
        """Initialize Ollama LLM"""
        try:
            self.llm = Ollama(
                base_url=settings.OLLAMA_BASE_URL,
                model=settings.OLLAMA_MODEL,
                temperature=settings.OLLAMA_TEMPERATURE,
            )
            logger.info(f"Initialized Ollama with model: {settings.OLLAMA_MODEL}")
        except Exception as e:
            logger.error(f"Failed to initialize Ollama: {e}")
            raise

    def _create_tools(self, advisor_id: str) -> list:
        """Create LangChain tools for the agent"""

        def get_customer_info(customer_name: str) -> str:
            """Get customer information by name"""
            # TODO: Implement actual database query
            return f"Customer information for {customer_name}: Active account with balance $125,000"

        def get_account_balance(customer_name: str) -> str:
            """Get account balance for a customer"""
            # TODO: Implement actual database query
            return f"Total account balance for {customer_name}: $125,000"

        def get_portfolio_summary(customer_name: str) -> str:
            """Get portfolio summary for a customer"""
            # TODO: Implement actual calculation
            return f"Portfolio for {customer_name}: 60% stocks, 30% bonds, 10% cash"

        tools = [
            Tool(
                name="CustomerInfo",
                func=get_customer_info,
                description="Get basic information about a customer by their name. Input should be the customer's full name."
            ),
            Tool(
                name="AccountBalance",
                func=get_account_balance,
                description="Get the total account balance for a customer. Input should be the customer's name."
            ),
            Tool(
                name="PortfolioSummary",
                func=get_portfolio_summary,
                description="Get portfolio allocation summary for a customer. Input should be the customer's name."
            ),
        ]

        return tools

    def create_agent(self, advisor_id: str) -> AgentExecutor:
        """Create a LangChain agent with tools and memory"""

        # Initialize memory for conversation context
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # Get tools
        tools = self._create_tools(advisor_id)

        # Create prompt template
        template = """You are a helpful AI assistant for financial advisors at Stifel Financial Group.
You help advisors get information about their customers and provide insights.

You have access to the following tools:
{tools}

Tool names: {tool_names}

When answering questions:
1. Be professional and concise
2. Only provide information about customers the advisor has access to
3. If you need to use a tool, format your response as:
   Thought: [your reasoning]
   Action: [tool name]
   Action Input: [input to the tool]
   
4. After getting the tool result, provide a clear answer to the advisor

Chat History:
{chat_history}

Question: {input}
{agent_scratchpad}"""

        prompt = PromptTemplate(
            template=template,
            input_variables=["input", "chat_history", "agent_scratchpad", "tools", "tool_names"]
        )

        # Create the agent
        agent = create_react_agent(
            llm=self.llm,
            tools=tools,
            prompt=prompt
        )

        # Create agent executor
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=self.memory,
            verbose=settings.DEBUG,
            max_iterations=3,
            handle_parsing_errors=True
        )

        return self.agent_executor

    async def chat(self, message: str, advisor_id: str, session_id: str = None) -> dict:
        """
        Process a chat message and return response

        Args:
            message: User's message
            advisor_id: Advisor's ID
            session_id: Optional session ID for context

        Returns:
            dict with response and optional chart_data
        """
        try:
            # Create or get agent
            if not self.agent_executor:
                self.create_agent(advisor_id)

            # Invoke the agent
            result = await self.agent_executor.ainvoke({"input": message})

            response = {
                "response": result.get("output", "I'm sorry, I couldn't process that request."),
                "chart_data": None,  # TODO: Implement chart generation logic
            }

            return response

        except Exception as e:
            logger.error(f"Error in chat processing: {e}")
            return {
                "response": "I apologize, but I encountered an error processing your request. Please try again.",
                "chart_data": None
            }

    def reset_memory(self):
        """Reset conversation memory"""
        if self.memory:
            self.memory.clear()


# Global instance
langchain_service = LangChainService()

