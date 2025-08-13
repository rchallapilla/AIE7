#!/usr/bin/env python3
"""
Complete setup test for the A2A LangGraph implementation.
This script tests all components are working properly.
"""

import asyncio
import os
import httpx
import json
from pathlib import Path

async def test_environment():
    """Test that environment variables are set."""
    print("🔧 Testing Environment Setup...")
    
    required_vars = ["OPENAI_API_KEY", "TAVILY_API_KEY"]
    optional_vars = ["LANGCHAIN_API_KEY", "LANGCHAIN_PROJECT"]
    
    all_good = True
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith("your_"):
            print(f"❌ {var}: Not set or still placeholder")
            all_good = False
        else:
            print(f"✅ {var}: Set (***{value[-4:]})")
    
    for var in optional_vars:
        value = os.getenv(var)
        if value and not value.startswith("your_"):
            print(f"✅ {var}: Set (***{value[-4:]})")
        else:
            print(f"⚠️  {var}: Not set (optional)")
    
    return all_good

async def test_agent_server():
    """Test that the A2A agent server is running."""
    print("\n🌐 Testing Agent Server...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:10000/.well-known/agent-card.json")
            
            if response.status_code == 200:
                agent_card = response.json()
                print(f"✅ Agent server is running")
                print(f"   Name: {agent_card.get('name')}")
                print(f"   Skills: {len(agent_card.get('skills', []))}")
                return True
            else:
                print(f"❌ Agent server returned status {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Cannot connect to agent server: {e}")
        print("   Make sure to run: uv run python -m app")
        return False

async def test_data_directory():
    """Test that data directory exists."""
    print("\n📁 Testing Data Directory...")
    
    data_dir = Path("data")
    if data_dir.exists():
        pdf_files = list(data_dir.glob("*.pdf"))
        print(f"✅ Data directory exists")
        print(f"   PDF files: {len(pdf_files)}")
        
        if pdf_files:
            for pdf in pdf_files[:3]:  # Show first 3
                print(f"   - {pdf.name}")
        else:
            print("   ℹ️  No PDF files found (RAG functionality won't work)")
        
        return True
    else:
        print(f"❌ Data directory doesn't exist")
        return False

async def test_dependencies():
    """Test that key dependencies are available."""
    print("\n📦 Testing Dependencies...")
    
    try:
        import langchain
        import langgraph
        import a2a
        import tavily
        
        print("✅ All key dependencies are installed")
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Run: uv sync")
        return False

def print_next_steps():
    """Print the next steps for the user."""
    print("\n🚀 Next Steps:")
    print("=" * 50)
    
    print("\n1. Set your API keys (if not already done):")
    print("   export OPENAI_API_KEY='sk-proj-your_actual_key'")
    print("   export TAVILY_API_KEY='tvly-your_actual_key'")
    print("   export LANGCHAIN_API_KEY='ls__your_actual_key'  # Optional")
    print("   export LANGCHAIN_PROJECT='your_project_name'    # Optional")
    
    print("\n2. Start the A2A agent server:")
    print("   uv run python -m app")
    
    print("\n3. In another terminal, test the setup:")
    print("   uv run python test_complete_setup.py")
    
    print("\n4. Run the client agent demo:")
    print("   uv run python client_agent.py")
    
    print("\n5. Test the original test client:")
    print("   uv run python app/test_client.py")
    
    print("\n🎯 For homework submission:")
    print("- Create a git branch: git checkout -b s15-assignment")
    print("- Commit your changes")
    print("- Record a Loom video demonstrating the working system")

async def main():
    """Run all tests."""
    print("🧪 A2A LangGraph Setup Test")
    print("=" * 40)
    
    tests = [
        ("Environment", test_environment()),
        ("Agent Server", test_agent_server()),
        ("Data Directory", test_data_directory()),
        ("Dependencies", test_dependencies()),
    ]
    
    results = []
    for name, test_coro in tests:
        result = await test_coro
        results.append((name, result))
    
    print("\n📊 Test Summary:")
    print("=" * 20)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! Your A2A setup is ready.")
        print("\nYou can now run:")
        print("   uv run python client_agent.py")
    else:
        print("⚠️  Some tests failed. See instructions above.")
        print_next_steps()

if __name__ == "__main__":
    asyncio.run(main())
