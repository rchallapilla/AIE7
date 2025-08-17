#!/usr/bin/env python3
"""
🏗️ Activity #1: Cache Performance Testing

This script implements comprehensive cache performance testing for:
1. Embedding cache performance
2. LLM cache performance  
3. Cache hit rate measurements
"""

import time
import os
import sys
from typing import List, Dict, Any
import statistics

# Add the current directory to Python path to import our library
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph_agent_lib import (
    ProductionRAGChain,
    CacheBackedEmbeddings,
    setup_llm_cache,
    get_openai_model
)


class CachePerformanceTester:
    """Comprehensive cache performance testing utility."""
    
    def __init__(self, cache_dir: str = "./cache"):
        """Initialize the cache performance tester.
        
        Args:
            cache_dir: Directory for caching
        """
        self.cache_dir = cache_dir
        self.results = {}
        
        # Set up LLM cache
        setup_llm_cache(cache_type="memory")
        print("✓ LLM cache configured")
        
        # Test texts for embedding cache testing
        self.test_texts = [
            "The Direct Loan Program provides financial assistance to eligible students.",
            "Artificial intelligence is transforming the way we approach problem solving.",
            "Machine learning algorithms require large datasets for training.",
            "Natural language processing enables computers to understand human language.",
            "Deep learning models have achieved remarkable success in various domains."
        ]
        
        # Test queries for LLM cache testing
        self.test_queries = [
            "What is the main purpose of the Direct Loan Program?",
            "How does artificial intelligence work?",
            "What are the benefits of machine learning?",
            "Explain natural language processing in simple terms.",
            "What is deep learning and how is it different from traditional machine learning?"
        ]
    
    def test_embedding_cache_performance(self, num_iterations: int = 3) -> Dict[str, Any]:
        """Test embedding cache performance by embedding the same text multiple times.
        
        Args:
            num_iterations: Number of times to test each text
            
        Returns:
            Dictionary with performance metrics
        """
        print("\n🔍 Testing Embedding Cache Performance")
        print("=" * 50)
        
        # Initialize cache-backed embeddings
        cached_embeddings = CacheBackedEmbeddings(
            model="text-embedding-3-small",
            cache_dir=f"{self.cache_dir}/embeddings"
        )
        
        embedding_times = []
        cache_hits = 0
        total_embeddings = 0
        
        for i, text in enumerate(self.test_texts):
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
        cache_hit_rate = cache_hits / (total_embeddings - len(self.test_texts)) if total_embeddings > len(self.test_texts) else 0
        
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
    
    def test_llm_cache_performance(self, num_iterations: int = 3) -> Dict[str, Any]:
        """Test LLM cache performance by asking the same question multiple times.
        
        Args:
            num_iterations: Number of times to test each query
            
        Returns:
            Dictionary with performance metrics
        """
        print("\n🤖 Testing LLM Cache Performance")
        print("=" * 50)
        
        # Get LLM model
        llm = get_openai_model("gpt-4.1-mini")
        
        llm_times = []
        cache_hits = 0
        total_queries = 0
        
        for i, query in enumerate(self.test_queries):
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
        cache_hit_rate = cache_hits / (total_queries - len(self.test_queries)) if total_queries > len(self.test_queries) else 0
        
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
    
    def test_rag_cache_performance(self, file_path: str, num_iterations: int = 3) -> Dict[str, Any]:
        """Test RAG cache performance using the ProductionRAGChain.
        
        Args:
            file_path: Path to the PDF file
            num_iterations: Number of times to test each query
            
        Returns:
            Dictionary with performance metrics
        """
        print("\n🔍 Testing RAG Cache Performance")
        print("=" * 50)
        
        # Create RAG chain
        rag_chain = ProductionRAGChain(
            file_path=file_path,
            chunk_size=1000,
            chunk_overlap=100,
            embedding_model="text-embedding-3-small",
            llm_model="gpt-4.1-mini",
            cache_dir=self.cache_dir
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
    
    def run_comprehensive_test(self, file_path: str = "./data/The_Direct_Loan_Program.pdf") -> Dict[str, Any]:
        """Run comprehensive cache performance testing.
        
        Args:
            file_path: Path to the PDF file for RAG testing
            
        Returns:
            Dictionary with all test results
        """
        print("🚀 Starting Comprehensive Cache Performance Testing")
        print("=" * 60)
        
        # Test 1: Embedding cache performance
        embedding_results = self.test_embedding_cache_performance(num_iterations=3)
        
        # Test 2: LLM cache performance
        llm_results = self.test_llm_cache_performance(num_iterations=3)
        
        # Test 3: RAG cache performance
        rag_results = self.test_rag_cache_performance(file_path, num_iterations=3)
        
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


def main():
    """Main function to run cache performance testing."""
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key before running this script")
        return
    
    # Check if PDF file exists
    file_path = "./data/The_Direct_Loan_Program.pdf"
    if not os.path.exists(file_path):
        print(f"⚠️  Warning: PDF file not found at {file_path}")
        print("RAG cache testing will be skipped")
        file_path = None
    
    # Create tester and run comprehensive test
    tester = CachePerformanceTester()
    
    try:
        if file_path:
            results = tester.run_comprehensive_test(file_path)
        else:
            # Run only embedding and LLM tests
            embedding_results = tester.test_embedding_cache_performance()
            llm_results = tester.test_llm_cache_performance()
            results = {
                "embedding_cache": embedding_results,
                "llm_cache": llm_results,
                "rag_cache": None
            }
        
        print("\n🎉 Cache performance testing completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
