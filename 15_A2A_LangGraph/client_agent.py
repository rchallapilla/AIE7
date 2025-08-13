#!/usr/bin/env python3
"""
Activity #1: LangGraph Agent that uses our A2A Agent

This creates a simple LangGraph agent that can make API calls to our A2A agent
through the A2A protocol, demonstrating agent-to-agent communication.
"""

import asyncio
import logging
from typing import Dict, Any, List
from typing_extensions import TypedDict
from uuid import uuid4

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import MessageSendParams, SendMessageRequest
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClientAgentState(TypedDict):
    """State for our client agent that communicates with the A2A agent."""
    messages: List[HumanMessage | AIMessage]
    a2a_response: str
    current_query: str

class A2AClientAgent:
    """A LangGraph agent that uses our A2A agent as a tool."""
    
    def __init__(self, a2a_agent_url: str = "http://localhost:10000"):
        self.a2a_agent_url = a2a_agent_url
        self.client = None
        self.httpx_client = None
        self.graph = self._build_graph()
    
    async def _initialize_a2a_client(self):
        """Initialize the A2A client connection."""
        try:
            self.httpx_client = httpx.AsyncClient(timeout=httpx.Timeout(60.0))
            resolver = A2ACardResolver(
                httpx_client=self.httpx_client,
                base_url=self.a2a_agent_url
            )
            
            # Get the agent card
            agent_card = await resolver.get_agent_card()
            logger.info(f"Connected to A2A agent: {agent_card.name}")
            logger.info(f"Available skills: {[skill.name for skill in agent_card.skills]}")
            
            # Initialize client
            self.client = A2AClient(
                httpx_client=self.httpx_client,
                agent_card=agent_card
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize A2A client: {e}")
            return False
    
    async def _query_a2a_agent(self, state: ClientAgentState) -> Dict[str, Any]:
        """Query the A2A agent with the current user message."""
        logger.info(f"Querying A2A agent: {state['current_query']}")
        
        # Initialize client if not done
        if not self.client:
            success = await self._initialize_a2a_client()
            if not success:
                return {
                    "a2a_response": "Failed to connect to A2A agent",
                    "messages": state["messages"] + [AIMessage(content="Failed to connect to A2A agent")]
                }
        
        try:
            # Send message using the same pattern as test_client.py
            send_message_payload = {
                'message': {
                    'role': 'user',
                    'parts': [
                        {'kind': 'text', 'text': state['current_query']}
                    ],
                    'message_id': uuid4().hex,
                },
            }
            request = SendMessageRequest(
                id=str(uuid4()), 
                params=MessageSendParams(**send_message_payload)
            )

            response = await self.client.send_message(request)
            logger.info(f"Response received: {response}")
            
            # Extract the response text
            if hasattr(response, 'result') and response.result:
                if hasattr(response.result, 'message') and response.result.message:
                    if hasattr(response.result.message, 'parts') and response.result.message.parts:
                        # Get the text from the first part
                        for part in response.result.message.parts:
                            if hasattr(part, 'text') and part.text:
                                agent_response = part.text
                                return {
                                    "a2a_response": agent_response,
                                    "messages": state["messages"] + [AIMessage(content=f"A2A Agent Response: {agent_response}")]
                                }
            
            return {
                "a2a_response": "No valid response from A2A agent",
                "messages": state["messages"] + [AIMessage(content="No valid response from A2A agent")]
            }
            
        except Exception as e:
            error_msg = f"Error querying A2A agent: {str(e)}"
            logger.error(error_msg)
            return {
                "a2a_response": error_msg,
                "messages": state["messages"] + [AIMessage(content=error_msg)]
            }
    
    def _extract_query(self, state: ClientAgentState) -> Dict[str, Any]:
        """Extract the user query from the messages."""
        if state["messages"]:
            last_message = state["messages"][-1]
            if isinstance(last_message, HumanMessage):
                return {"current_query": last_message.content}
        
        return {"current_query": "No query found"}
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(ClientAgentState)
        
        # Add nodes
        workflow.add_node("extract_query", self._extract_query)
        workflow.add_node("query_a2a_agent", self._query_a2a_agent)
        
        # Add edges
        workflow.set_entry_point("extract_query")
        workflow.add_edge("extract_query", "query_a2a_agent")
        workflow.add_edge("query_a2a_agent", END)
        
        return workflow.compile()
    
    async def run(self, user_input: str) -> str:
        """Run the client agent with user input."""
        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "a2a_response": "",
            "current_query": ""
        }
        
        result = await self.graph.ainvoke(initial_state)
        return result["a2a_response"]

async def main():
    """Demonstrate the A2A client agent."""
    print("🤖 A2A Client Agent Demo")
    print("=" * 40)
    
    # Create the client agent
    client_agent = A2AClientAgent()
    
    # Test queries that demonstrate different skills
    test_queries = [
        "What are the latest developments in artificial intelligence?",  # Web search
        "Find recent papers on transformer architectures",  # ArXiv search
        "What information is available in the loaded documents?",  # RAG search
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {query}")
        print("-" * 50)
        
        try:
            response = await client_agent.run(query)
            print(f"📝 Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()

if __name__ == "__main__":
    # Instructions for running
    print("🚀 A2A Client Agent")
    print("=" * 40)
    print("This agent demonstrates how to use LangGraph to communicate")
    print("with our A2A agent through the A2A protocol.")
    print()
    print("Prerequisites:")
    print("1. Make sure your A2A agent server is running:")
    print("   uv run python -m app")
    print()
    print("2. Make sure your API keys are set properly")
    print()
    print("Running the demo...")
    print()
    
    asyncio.run(main())
