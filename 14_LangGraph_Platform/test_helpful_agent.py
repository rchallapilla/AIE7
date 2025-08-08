#!/usr/bin/env python3
"""
Test script for the agent with helpfulness evaluation.
This demonstrates the enhanced agent with quality control.
"""

from langgraph_sdk import get_sync_client

def main():
    client = get_sync_client(url="http://localhost:2024")
    
    print("🤖 Testing Agent with Helpfulness Evaluation")
    print("=" * 50)
    
    for chunk in client.runs.stream(
        None,  # Threadless run
        "agent_with_helpfulness",  # Assistant id from langgraph.json
        input={
            "messages": [
                {
                    "role": "human",
                    "content": "What are the key differences between transformers and RNNs?",
                }
            ]
        },
        stream_mode="updates",
    ):
        print(f"📡 Event: {chunk.event}")
        if chunk.data:
            print(f"📊 Data: {chunk.data}")
        print()

if __name__ == "__main__":
    main()
