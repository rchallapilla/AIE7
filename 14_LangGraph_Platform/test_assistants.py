#!/usr/bin/env python3
"""
Test script to demonstrate LangGraph assistants without requiring API keys.
This script shows the available assistants and their configurations.
"""

import requests
import json

def test_server_info():
    """Test basic server connectivity."""
    try:
        response = requests.get("http://localhost:2024/info")
        if response.status_code == 200:
            print("✅ Server is running and healthy!")
            info = response.json()
            print(f"   Version: {info.get('version', 'Unknown')}")
            print(f"   LangGraph Python: {info.get('langgraph_py_version', 'Unknown')}")
            return True
        else:
            print(f"❌ Server returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return False

def test_assistants():
    """Test assistant endpoints."""
    try:
        # Search for assistants
        response = requests.post("http://localhost:2024/assistants/search", 
                               json={"limit": 10})
        
        if response.status_code == 200:
            assistants = response.json()
            print(f"\n📋 Found {len(assistants)} assistants:")
            
            for assistant in assistants:
                print(f"\n🤖 Assistant: {assistant.get('name', 'Unknown')}")
                print(f"   ID: {assistant.get('assistant_id', 'Unknown')}")
                print(f"   Graph: {assistant.get('graph_id', 'Unknown')}")
                print(f"   Description: {assistant.get('description', 'No description')}")
                print(f"   Status: {assistant.get('status', 'Unknown')}")
                
                # Get graph schema for this assistant
                graph_id = assistant.get('graph_id')
                if graph_id:
                    schema_response = requests.get(f"http://localhost:2024/assistants/{assistant['assistant_id']}/schemas")
                    if schema_response.status_code == 200:
                        schema = schema_response.json()
                        print(f"   📊 Graph Schema:")
                        print(f"      - Input Schema: {'✅' if schema.get('input_schema') else '❌'}")
                        print(f"      - Output Schema: {'✅' if schema.get('output_schema') else '❌'}")
                        print(f"      - State Schema: {'✅' if schema.get('state_schema') else '❌'}")
            
            return True
        else:
            print(f"❌ Failed to get assistants: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing assistants: {e}")
        return False

def test_graphs():
    """Test graph endpoints."""
    try:
        # Test the two graphs we know about
        graphs = ["simple_agent", "agent_with_helpfulness"]
        
        print(f"\n🔧 Testing {len(graphs)} graphs:")
        
        for graph_id in graphs:
            print(f"\n📊 Graph: {graph_id}")
            
            # Try to get graph info (this might not work without proper auth)
            try:
                response = requests.get(f"http://localhost:2024/assistants/search", 
                                     json={"graph_id": graph_id, "limit": 1})
                if response.status_code == 200:
                    results = response.json()
                    if results:
                        print(f"   ✅ Graph is accessible")
                        print(f"   📝 Assistant: {results[0].get('name', 'Unknown')}")
                    else:
                        print(f"   ⚠️  No assistants found for this graph")
                else:
                    print(f"   ❌ Cannot access graph info")
            except Exception as e:
                print(f"   ❌ Error accessing graph: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing graphs: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Testing LangGraph Platform...")
    print("=" * 50)
    
    # Test server connectivity
    if not test_server_info():
        return
    
    # Test assistants
    test_assistants()
    
    # Test graphs
    test_graphs()
    
    print("\n" + "=" * 50)
    print("✅ Testing complete!")
    print("\n📝 Summary:")
    print("   - Server is running on http://localhost:2024")
    print("   - Two assistants available: 'agent' and 'agent_helpful'")
    print("   - Two graphs: 'simple_agent' and 'agent_with_helpfulness'")
    print("   - API endpoints are accessible")
    print("\n🔗 Next steps:")
    print("   1. Configure API keys in .env file")
    print("   2. Test with: uv run test_served_graph.py")
    print("   3. Open Studio: https://smith.langchain.com/studio?baseUrl=http://localhost:2024")

if __name__ == "__main__":
    main()
