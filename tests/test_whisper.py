#!/usr/bin/env python3
"""
OPAL Whisper Integration Test

Tests the openai-whisper library for audio transcription.
Run with: python tests/test_whisper.py
"""

import os
import sys
import tempfile
import wave
import struct
import math

def generate_test_audio(filename, duration=3, sample_rate=16000):
    """Generate a simple test audio file with a sine wave."""
    n_samples = int(duration * sample_rate)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)

        # Generate a 440Hz sine wave
        for i in range(n_samples):
            sample = int(32767 * 0.3 * math.sin(2 * math.pi * 440 * i / sample_rate))
            wav_file.writeframes(struct.pack('<h', sample))

    return filename

def test_whisper_import():
    """Test that whisper can be imported."""
    print("Testing whisper import...")
    try:
        import whisper
        print(f"  ✅ Whisper imported successfully (version: {whisper.__version__})")
        return True
    except ImportError as e:
        print(f"  ❌ Failed to import whisper: {e}")
        print("  Install with: pip install openai-whisper")
        return False

def test_whisper_models():
    """Test available models."""
    print("\nTesting available models...")
    try:
        import whisper
        models = whisper.available_models()
        print(f"  ✅ Available models: {', '.join(models)}")
        return True
    except Exception as e:
        print(f"  ❌ Failed to list models: {e}")
        return False

def test_whisper_load_model(model_name="tiny"):
    """Test loading a model."""
    print(f"\nTesting model loading ({model_name})...")
    try:
        import whisper
        print(f"  Loading {model_name} model (this may take a moment)...")
        model = whisper.load_model(model_name)
        print(f"  ✅ Model '{model_name}' loaded successfully")
        return model
    except Exception as e:
        print(f"  ❌ Failed to load model: {e}")
        return None

def test_whisper_transcribe(model):
    """Test transcription with a generated audio file."""
    print("\nTesting transcription...")

    if model is None:
        print("  ⏭️  Skipping (no model loaded)")
        return False

    try:
        # Generate a test audio file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            test_file = f.name

        print("  Generating test audio file...")
        generate_test_audio(test_file, duration=2)

        print("  Transcribing...")
        result = model.transcribe(test_file, fp16=False)

        print(f"  ✅ Transcription successful")
        print(f"  Detected language: {result.get('language', 'unknown')}")
        print(f"  Text: '{result.get('text', '').strip()}'")

        # Cleanup
        os.unlink(test_file)
        return True

    except Exception as e:
        print(f"  ❌ Transcription failed: {e}")
        if 'test_file' in locals():
            try:
                os.unlink(test_file)
            except:
                pass
        return False

def test_whisper_with_real_audio(model, audio_path):
    """Test transcription with a real audio file."""
    print(f"\nTesting with real audio: {audio_path}")

    if model is None:
        print("  ⏭️  Skipping (no model loaded)")
        return False

    if not os.path.exists(audio_path):
        print(f"  ⏭️  Skipping (file not found)")
        return False

    try:
        print("  Transcribing...")
        result = model.transcribe(audio_path, fp16=False)

        print(f"  ✅ Transcription successful")
        print(f"  Detected language: {result.get('language', 'unknown')}")
        print(f"  Text preview: '{result.get('text', '').strip()[:200]}...'")

        return True

    except Exception as e:
        print(f"  ❌ Transcription failed: {e}")
        return False

def main():
    print("=" * 60)
    print("OPAL Whisper Integration Test")
    print("=" * 60)

    results = []

    # Test 1: Import
    results.append(("Import", test_whisper_import()))

    # Test 2: List models
    results.append(("List models", test_whisper_models()))

    # Test 3: Load model
    model = test_whisper_load_model("tiny")
    results.append(("Load model", model is not None))

    # Test 4: Transcribe generated audio
    results.append(("Transcribe (synthetic)", test_whisper_transcribe(model)))

    # Test 5: Transcribe real audio if provided
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
        results.append(("Transcribe (real)", test_whisper_with_real_audio(model, audio_path)))

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
        print("\n🎉 All tests passed! Whisper is ready for OPAL.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
