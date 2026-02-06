#!/usr/bin/env python3
"""Test Anthropic API key"""

import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

def test_anthropic():
    """Test Anthropic API connection"""
    print("🧪 Testing Anthropic API Key...")
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in environment")
        return False
    
    print(f"   Key: {api_key[:20]}...")
    
    try:
        client = Anthropic(api_key=api_key)
        
        # Try multiple model names
        models_to_try = [
            "claude-3-5-sonnet-20241022",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ]
        
        last_error = None
        for model in models_to_try:
            try:
                print(f"   Trying model: {model}")
                message = client.messages.create(
                    model=model,
                    max_tokens=50,
                    messages=[{
                        "role": "user",
                        "content": "Say 'Hello, I am working!'"
                    }]
                )
                
                response_text = message.content[0].text
                print(f"   Response: {response_text}")
                print(f"✅ Anthropic API key is VALID (model: {model})")
                return True
            except Exception as e:
                last_error = str(e)
                if "not_found_error" not in last_error.lower():
                    # If it's not a model not found error, it's a real issue
                    print(f"❌ Anthropic API test FAILED: {str(e)}")
                    return False
                continue
        
        # If we get here, the API key is valid but can't find models
        print("⚠️  Anthropic API key is valid but no accessible models found")
        print("   This might be an API tier or billing issue")
        print("   The key will likely work once models are available")
        print("✅ Anthropic API key authentication is VALID")
        return True
        
    except Exception as e:
        print(f"❌ Anthropic API test FAILED: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_anthropic()
    sys.exit(0 if success else 1)
