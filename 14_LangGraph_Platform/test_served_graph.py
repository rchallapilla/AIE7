import os
import requests
from langgraph_sdk import get_sync_client


def main():
    # If no usable OpenAI credentials, run a lightweight server check and exit gracefully.
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key or api_key in {"sk-your-actual-key-here", "sk-test"}:
        print("⚠️  Skipping streaming run because OPENAI_API_KEY is missing or placeholder.")
        # Basic sanity check that the server is up instead
        try:
            info = requests.get("http://localhost:2024/info", timeout=5).json()
            print("Server info:", info)
        except Exception as exc:
            print(f"❌ Could not fetch /info: {exc}")
        return

    client = get_sync_client(url="http://localhost:2024")
    try:
        for chunk in client.runs.stream(
            None,  # Threadless run
            "simple_agent",  # Assistant id from langgraph.json (assistants)
            input={
                "messages": [
                    {
                        "role": "human",
                        "content": "What is the MuonClip optimizer, and what paper did it first appear in?",
                    }
                ]
            },
            stream_mode="updates",
        ):
            print(f"Receiving new event of type: {chunk.event}...")
            print(chunk.data)
            print("\n\n")
    except Exception as exc:
        print(f"❌ Streaming run failed (likely due to API key/auth): {exc}")


if __name__ == "__main__":
    main()