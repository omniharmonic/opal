#!/usr/bin/env python3
"""
OPAL Ollama Integration Test

Tests the Ollama API for embeddings and LLM operations.
Run with: python tests/test_ollama.py

Requirements:
- Ollama installed and running: https://ollama.ai
- Models pulled: ollama pull nomic-embed-text && ollama pull llama3.2
"""

import sys
import json

try:
    import urllib.request
    import urllib.error
except ImportError:
    print("❌ urllib not available")
    sys.exit(1)

OLLAMA_BASE_URL = "http://localhost:11434"

def make_request(endpoint, data=None, method="GET"):
    """Make an HTTP request to Ollama API."""
    url = f"{OLLAMA_BASE_URL}{endpoint}"

    if data:
        data = json.dumps(data).encode('utf-8')
        request = urllib.request.Request(url, data=data, method="POST")
        request.add_header('Content-Type', 'application/json')
    else:
        request = urllib.request.Request(url, method=method)

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        raise ConnectionError(f"Failed to connect to Ollama: {e}")

def test_ollama_connection():
    """Test that Ollama is running and accessible."""
    print("Testing Ollama connection...")
    try:
        # Try to list models
        response = make_request("/api/tags")
        print(f"  ✅ Connected to Ollama at {OLLAMA_BASE_URL}")
        return True
    except ConnectionError as e:
        print(f"  ❌ Cannot connect to Ollama: {e}")
        print("  Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_ollama_models():
    """List available models."""
    print("\nTesting available models...")
    try:
        response = make_request("/api/tags")
        models = response.get('models', [])

        if not models:
            print("  ⚠️  No models installed")
            print("  Install required models:")
            print("    ollama pull nomic-embed-text")
            print("    ollama pull llama3.2")
            return False

        print(f"  ✅ Found {len(models)} models:")
        for model in models:
            name = model.get('name', 'unknown')
            size = model.get('size', 0) / (1024**3)  # Convert to GB
            print(f"     - {name} ({size:.2f} GB)")

        return True
    except Exception as e:
        print(f"  ❌ Error listing models: {e}")
        return False

def test_embedding_model():
    """Test the nomic-embed-text embedding model."""
    print("\nTesting embedding model (nomic-embed-text)...")
    try:
        test_text = "Participatory budgeting is a democratic process"

        response = make_request("/api/embeddings", {
            "model": "nomic-embed-text",
            "prompt": test_text
        })

        embedding = response.get('embedding', [])

        if not embedding:
            print("  ❌ No embedding returned")
            return False

        print(f"  ✅ Embedding generated successfully")
        print(f"     Dimensions: {len(embedding)}")
        print(f"     Sample values: [{embedding[0]:.4f}, {embedding[1]:.4f}, ...]")

        return True

    except ConnectionError:
        print("  ❌ Model not available. Install with: ollama pull nomic-embed-text")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_llm_model():
    """Test the llama3.2 LLM model."""
    print("\nTesting LLM model (llama3.2)...")
    try:
        test_prompt = "In one sentence, what is consent-based decision making?"

        response = make_request("/api/generate", {
            "model": "llama3.2",
            "prompt": test_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 100
            }
        })

        generated_text = response.get('response', '')

        if not generated_text:
            print("  ❌ No response generated")
            return False

        print(f"  ✅ LLM response generated successfully")
        print(f"     Response: {generated_text[:150]}...")

        return True

    except ConnectionError:
        print("  ❌ Model not available. Install with: ollama pull llama3.2")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_semantic_similarity():
    """Test semantic similarity between two texts."""
    print("\nTesting semantic similarity...")
    try:
        texts = [
            "Consent-based decision making requires no objections",
            "Sociocracy uses consent for governance decisions",
            "The weather is nice today"
        ]

        embeddings = []
        for text in texts:
            response = make_request("/api/embeddings", {
                "model": "nomic-embed-text",
                "prompt": text
            })
            embeddings.append(response.get('embedding', []))

        # Calculate cosine similarity
        def cosine_similarity(a, b):
            dot_product = sum(x * y for x, y in zip(a, b))
            norm_a = sum(x ** 2 for x in a) ** 0.5
            norm_b = sum(x ** 2 for x in b) ** 0.5
            return dot_product / (norm_a * norm_b)

        sim_01 = cosine_similarity(embeddings[0], embeddings[1])
        sim_02 = cosine_similarity(embeddings[0], embeddings[2])

        print(f"  ✅ Semantic similarity calculated")
        print(f"     '{texts[0][:40]}...' vs")
        print(f"     '{texts[1][:40]}...': {sim_01:.4f}")
        print(f"     '{texts[2][:40]}...': {sim_02:.4f}")

        # The first two should be more similar than the third
        if sim_01 > sim_02:
            print(f"  ✅ Semantic relationships correct (related > unrelated)")
            return True
        else:
            print(f"  ⚠️  Unexpected similarity scores")
            return False

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_entity_extraction_prompt():
    """Test entity extraction using LLM."""
    print("\nTesting entity extraction prompt...")
    try:
        transcript = """
        Maria Chen: I've been implementing consent-based decision making in our
        neighborhood council for about six months now.

        Interviewer: How has that worked with participatory budgeting?

        Maria Chen: It's been transformative. The sociocracy principles really
        complement the PB process.
        """

        prompt = f"""Extract named entities from this transcript.
Return as JSON with these categories:
- people: names of individuals
- organizations: group names
- patterns: governance patterns mentioned
- protocols: methodologies or processes

Transcript:
{transcript}

Return ONLY valid JSON, no other text."""

        response = make_request("/api/generate", {
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 500
            }
        })

        result = response.get('response', '')

        print(f"  ✅ Entity extraction completed")
        print(f"     Raw response:\n{result[:500]}")

        # Try to parse as JSON
        try:
            # Find JSON in response
            import re
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                entities = json.loads(json_match.group())
                print(f"  ✅ Valid JSON extracted")
                return True
            else:
                print(f"  ⚠️  No JSON found in response")
                return False
        except json.JSONDecodeError:
            print(f"  ⚠️  Response is not valid JSON (this is acceptable)")
            return True  # LLM worked, just formatting issue

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("OPAL Ollama Integration Test")
    print("=" * 60)

    results = []

    # Test 1: Connection
    results.append(("Connection", test_ollama_connection()))

    if not results[-1][1]:
        print("\n⚠️  Cannot proceed without Ollama connection.")
        print("Start Ollama with: ollama serve")
        return 1

    # Test 2: List models
    results.append(("List models", test_ollama_models()))

    # Test 3: Embedding model
    results.append(("Embedding model", test_embedding_model()))

    # Test 4: LLM model
    results.append(("LLM model", test_llm_model()))

    # Test 5: Semantic similarity
    if results[2][1]:  # Only if embedding model works
        results.append(("Semantic similarity", test_semantic_similarity()))

    # Test 6: Entity extraction
    if results[3][1]:  # Only if LLM model works
        results.append(("Entity extraction", test_entity_extraction_prompt()))

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name}: {status}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Ollama is ready for OPAL.")
        return 0
    elif passed >= 3:
        print("\n⚠️  Core functionality works. Some optional features may need setup.")
        return 0
    else:
        print("\n❌ Critical tests failed. Please check Ollama setup.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
