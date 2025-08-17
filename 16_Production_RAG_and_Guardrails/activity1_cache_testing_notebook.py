# 🏗️ Activity #1: Cache Performance Testing
# 
# This code can be run in Jupyter notebook cells to test:
# 1. Embedding cache performance
# 2. LLM cache performance  
# 3. Cache hit rate measurements

import time
import statistics
from typing import Dict, Any

# ============================================================================
# CELL 1: Test Embedding Cache Performance
# ============================================================================

def test_embedding_cache_performance(num_iterations: int = 3):
    """Test embedding cache performance by embedding the same text multiple times."""
    
    print("🔍 Testing Embedding Cache Performance")
    print("=" * 50)
    
    # Initialize cache-backed embeddings
    from langgraph_agent_lib import CacheBackedEmbeddings
    cached_embeddings = CacheBackedEmbeddings(
        model="text-embedding-3-small",
        cache_dir="./cache/embeddings"
    )
    
    # Test texts
    test_texts = [
        "The Direct Loan Program provides financial assistance to eligible students.",
        "Artificial intelligence is transforming the way we approach problem solving.",
        "Machine learning algorithms require large datasets for training.",
        "Natural language processing enables computers to understand human language.",
        "Deep learning models have achieved remarkable success in various domains."
    ]
    
    embedding_times = []
    cache_hits = 0
    total_embeddings = 0
    
    for i, text in enumerate(test_texts):
        print(f"\n📝 Testing text {i+1}: {text[:50]}...")
        
        text_times = []
        
        for iteration in range(num_iterations):
            start_time = time.time()
            
            # Get embeddings
            embeddings = cached_embeddings.get_embeddings()
            result = embeddings.embed_query(text)
            
            end_time = time.time()
            duration = end_time - start_time
            text_times.append(duration)
            
            total_embeddings += 1
            
            # First iteration is always a cache miss, subsequent are hits
            if iteration > 0:
                cache_hits += 1
            
            print(f"  Iteration {iteration + 1}: {duration:.4f}s")
        
        embedding_times.extend(text_times)
    
    # Calculate metrics
    avg_time = statistics.mean(embedding_times)
    cache_hit_rate = cache_hits / (total_embeddings - len(test_texts)) if total_embeddings > len(test_texts) else 0
    
    # Separate first calls (cache misses) from subsequent calls (cache hits)
    first_call_times = embedding_times[::num_iterations]  # First call of each text
    subsequent_call_times = [t for i, t in enumerate(embedding_times) if i % num_iterations != 0]
    
    avg_first_call = statistics.mean(first_call_times) if first_call_times else 0
    avg_subsequent_call = statistics.mean(subsequent_call_times) if subsequent_call_times else 0
    
    results = {
        "total_embeddings": total_embeddings,
        "cache_hits": cache_hits,
        "cache_hit_rate": cache_hit_rate,
        "avg_time": avg_time,
        "avg_first_call": avg_first_call,
        "avg_subsequent_call": avg_subsequent_call,
        "speedup_factor": avg_first_call / avg_subsequent_call if avg_subsequent_call > 0 else 0,
        "all_times": embedding_times
    }
    
    print(f"\n📊 Embedding Cache Results:")
    print(f"  Total embeddings: {total_embeddings}")
    print(f"  Cache hits: {cache_hits}")
    print(f"  Cache hit rate: {cache_hit_rate:.2%}")
    print(f"  Average time: {avg_time:.4f}s")
    print(f"  Average first call: {avg_first_call:.4f}s")
    print(f"  Average subsequent calls: {avg_subsequent_call:.4f}s")
    print(f"  Speedup factor: {results['speedup_factor']:.2f}x")
    
    return results

# ============================================================================
# CELL 2: Test LLM Cache Performance
# ============================================================================

def test_llm_cache_performance(num_iterations: int = 3):
    """Test LLM cache performance by asking the same question multiple times."""
    
    print("🤖 Testing LLM Cache Performance")
    print("=" * 50)
    
    # Get LLM model
    from langgraph_agent_lib import get_openai_model
    llm = get_openai_model("gpt-4.1-mini")
    
    # Test queries
    test_queries = [
        "What is the main purpose of the Direct Loan Program?",
        "How does artificial intelligence work?",
        "What are the benefits of machine learning?",
        "Explain natural language processing in simple terms.",
        "What is deep learning and how is it different from traditional machine learning?"
    ]
    
    llm_times = []
    cache_hits = 0
    total_queries = 0
    
    for i, query in enumerate(test_queries):
        print(f"\n❓ Testing query {i+1}: {query[:50]}...")
        
        query_times = []
        
        for iteration in range(num_iterations):
            start_time = time.time()
            
            # Ask the same question
            response = llm.invoke(query)
            
            end_time = time.time()
            duration = end_time - start_time
            query_times.append(duration)
            
            total_queries += 1
            
            # First iteration is always a cache miss, subsequent are hits
            if iteration > 0:
                cache_hits += 1
            
            print(f"  Iteration {iteration + 1}: {duration:.4f}s")
        
        llm_times.extend(query_times)
    
    # Calculate metrics
    avg_time = statistics.mean(llm_times)
    cache_hit_rate = cache_hits / (total_queries - len(test_queries)) if total_queries > len(test_queries) else 0
    
    # Separate first calls (cache misses) from subsequent calls (cache hits)
    first_call_times = llm_times[::num_iterations]  # First call of each query
    subsequent_call_times = [t for i, t in enumerate(llm_times) if i % num_iterations != 0]
    
    avg_first_call = statistics.mean(first_call_times) if first_call_times else 0
    avg_subsequent_call = statistics.mean(subsequent_call_times) if subsequent_call_times else 0
    
    results = {
        "total_queries": total_queries,
        "cache_hits": cache_hits,
        "cache_hit_rate": cache_hit_rate,
        "avg_time": avg_time,
        "avg_first_call": avg_first_call,
        "avg_subsequent_call": avg_subsequent_call,
        "speedup_factor": avg_first_call / avg_subsequent_call if avg_subsequent_call > 0 else 0,
        "all_times": llm_times
    }
    
    print(f"\n📊 LLM Cache Results:")
    print(f"  Total queries: {total_queries}")
    print(f"  Cache hits: {cache_hits}")
    print(f"  Cache hit rate: {cache_hit_rate:.2%}")
    print(f"  Average time: {avg_time:.4f}s")
    print(f"  Average first call: {avg_first_call:.4f}s")
    print(f"  Average subsequent calls: {avg_subsequent_call:.4f}s")
    print(f"  Speedup factor: {results['speedup_factor']:.2f}x")
    
    return results

# ============================================================================
# CELL 3: Test RAG Cache Performance
# ============================================================================

def test_rag_cache_performance(file_path: str = "./data/The_Direct_Loan_Program.pdf", num_iterations: int = 3):
    """Test RAG cache performance using the ProductionRAGChain."""
    
    print("🔍 Testing RAG Cache Performance")
    print("=" * 50)
    
    # Create RAG chain
    from langgraph_agent_lib import ProductionRAGChain
    rag_chain = ProductionRAGChain(
        file_path=file_path,
        chunk_size=1000,
        chunk_overlap=100,
        embedding_model="text-embedding-3-small",
        llm_model="gpt-4.1-mini",
        cache_dir="./cache"
    )
    
    # Test queries specific to the document
    rag_queries = [
        "What is the main purpose of the Direct Loan Program?",
        "Who is eligible for the Direct Loan Program?",
        "What are the requirements for the Direct Loan Program?",
        "How does the Direct Loan Program work?",
        "What are the benefits of the Direct Loan Program?"
    ]
    
    rag_times = []
    cache_hits = 0
    total_queries = 0
    
    for i, query in enumerate(rag_queries):
        print(f"\n📄 Testing RAG query {i+1}: {query}")
        
        query_times = []
        
        for iteration in range(num_iterations):
            start_time = time.time()
            
            # Ask the RAG chain
            response = rag_chain.ask(query)
            
            end_time = time.time()
            duration = end_time - start_time
            query_times.append(duration)
            
            total_queries += 1
            
            # First iteration is always a cache miss, subsequent are hits
            if iteration > 0:
                cache_hits += 1
            
            print(f"  Iteration {iteration + 1}: {duration:.4f}s")
        
        rag_times.extend(query_times)
    
    # Calculate metrics
    avg_time = statistics.mean(rag_times)
    cache_hit_rate = cache_hits / (total_queries - len(rag_queries)) if total_queries > len(rag_queries) else 0
    
    # Separate first calls (cache misses) from subsequent calls (cache hits)
    first_call_times = rag_times[::num_iterations]  # First call of each query
    subsequent_call_times = [t for i, t in enumerate(rag_times) if i % num_iterations != 0]
    
    avg_first_call = statistics.mean(first_call_times) if first_call_times else 0
    avg_subsequent_call = statistics.mean(subsequent_call_times) if subsequent_call_times else 0
    
    results = {
        "total_queries": total_queries,
        "cache_hits": cache_hits,
        "cache_hit_rate": cache_hit_rate,
        "avg_time": avg_time,
        "avg_first_call": avg_first_call,
        "avg_subsequent_call": avg_subsequent_call,
        "speedup_factor": avg_first_call / avg_subsequent_call if avg_subsequent_call > 0 else 0,
        "all_times": rag_times
    }
    
    print(f"\n📊 RAG Cache Results:")
    print(f"  Total queries: {total_queries}")
    print(f"  Cache hits: {cache_hits}")
    print(f"  Cache hit rate: {cache_hit_rate:.2%}")
    print(f"  Average time: {avg_time:.4f}s")
    print(f"  Average first call: {avg_first_call:.4f}s")
    print(f"  Average subsequent calls: {avg_subsequent_call:.4f}s")
    print(f"  Speedup factor: {results['speedup_factor']:.2f}x")
    
    return results

# ============================================================================
# CELL 4: Run Comprehensive Cache Performance Test
# ============================================================================

def run_comprehensive_cache_test(file_path: str = "./data/The_Direct_Loan_Program.pdf"):
    """Run comprehensive cache performance testing."""
    
    print("🚀 Starting Comprehensive Cache Performance Testing")
    print("=" * 60)
    
    # Test 1: Embedding cache performance
    embedding_results = test_embedding_cache_performance(num_iterations=3)
    
    # Test 2: LLM cache performance
    llm_results = test_llm_cache_performance(num_iterations=3)
    
    # Test 3: RAG cache performance
    rag_results = test_rag_cache_performance(file_path, num_iterations=3)
    
    # Compile comprehensive results
    comprehensive_results = {
        "embedding_cache": embedding_results,
        "llm_cache": llm_results,
        "rag_cache": rag_results,
        "summary": {
            "embedding_speedup": embedding_results["speedup_factor"],
            "llm_speedup": llm_results["speedup_factor"],
            "rag_speedup": rag_results["speedup_factor"],
            "overall_cache_hit_rate": (
                embedding_results["cache_hit_rate"] + 
                llm_results["cache_hit_rate"] + 
                rag_results["cache_hit_rate"]
            ) / 3
        }
    }
    
    # Print comprehensive summary
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE CACHE PERFORMANCE SUMMARY")
    print("=" * 60)
    print(f"🔍 Embedding Cache Speedup: {embedding_results['speedup_factor']:.2f}x")
    print(f"🤖 LLM Cache Speedup: {llm_results['speedup_factor']:.2f}x")
    print(f"📄 RAG Cache Speedup: {rag_results['speedup_factor']:.2f}x")
    print(f"📈 Overall Cache Hit Rate: {comprehensive_results['summary']['overall_cache_hit_rate']:.2%}")
    print("\n✅ Cache Performance Testing Complete!")
    
    return comprehensive_results

# ============================================================================
# CELL 5: Example Usage (Copy these cells into your notebook)
# ============================================================================

# Example 1: Test just embedding cache
# embedding_results = test_embedding_cache_performance()

# Example 2: Test just LLM cache  
# llm_results = test_llm_cache_performance()

# Example 3: Test just RAG cache
# rag_results = test_rag_cache_performance()

# Example 4: Run comprehensive test
# comprehensive_results = run_comprehensive_cache_test()

# ============================================================================
# CELL 6: Analyze Cache Directory Growth
# ============================================================================

def analyze_cache_directory():
    """Analyze the cache directory to see what's being cached."""
    
    import os
    
    cache_dir = "./cache"
    
    if not os.path.exists(cache_dir):
        print("❌ Cache directory not found")
        return
    
    print("📁 Cache Directory Analysis")
    print("=" * 40)
    
    total_size = 0
    file_count = 0
    
    for root, dirs, files in os.walk(cache_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            total_size += file_size
            file_count += 1
            
            # Show relative path from cache directory
            rel_path = os.path.relpath(file_path, cache_dir)
            print(f"  📄 {rel_path}: {file_size} bytes")
    
    print(f"\n📊 Cache Summary:")
    print(f"  Total files: {file_count}")
    print(f"  Total size: {total_size} bytes ({total_size / 1024:.2f} KB)")
    
    return {
        "file_count": file_count,
        "total_size": total_size,
        "total_size_kb": total_size / 1024
    }
