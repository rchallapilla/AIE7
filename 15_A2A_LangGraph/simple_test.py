#!/usr/bin/env python3
"""Simple test to see the A2A response format."""

import asyncio
import logging
from uuid import uuid4
import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import MessageSendParams, SendMessageRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def simple_test():
    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as httpx_client:
        # Initialize resolver and client
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url="http://localhost:10000"
        )
        
        agent_card = await resolver.get_agent_card()
        logger.info(f"Connected to: {agent_card.name}")
        
        client = A2AClient(
            httpx_client=httpx_client,
            agent_card=agent_card
        )
        
        # Send a simple message
        send_message_payload = {
            'message': {
                'role': 'user',
                'parts': [
                    {'kind': 'text', 'text': 'Hello, what can you do?'}
                ],
                'message_id': uuid4().hex,
            },
        }
        request = SendMessageRequest(
            id=str(uuid4()), 
            params=MessageSendParams(**send_message_payload)
        )

        response = await client.send_message(request)
        print(f"Response type: {type(response)}")
        print(f"Response: {response}")
        
        if hasattr(response, 'model_dump'):
            print(f"Response dump: {response.model_dump()}")

if __name__ == "__main__":
    asyncio.run(simple_test())
