#!/usr/bin/env python3
"""
Test script for the agent with helpfulness evaluation.
This demonstrates the enhanced agent with quality control.
"""

import os
import requests
from langgraph_sdk import get_sync_client


def main():
    client = get_sync_client(url="http://localhost:2024")
    
    print("🤖 Testing Agent with Helpfulness Evaluation")
    print("=" * 50)

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key or api_key in {"sk-your-actual-key-here", "sk-test"}:
        print("⚠️  Skipping streaming run because OPENAI_API_KEY is missing or placeholder.")
        try:
            info = requests.get("http://localhost:2024/info", timeout=5).json()
            print("Server info:", info)
        except Exception as exc:
            print(f"❌ Could not fetch /info: {exc}")
        return
    
    try:
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
    except Exception as exc:
        print(f"❌ Streaming run failed (likely due to API key/auth): {exc}")


if __name__ == "__main__":
    main()
