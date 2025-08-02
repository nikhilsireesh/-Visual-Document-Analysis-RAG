"""
Simple test script to verify Gemini API connection
"""
import os
import google.generativeai as genai

def test_gemini_api():
    """Test direct Gemini API connection."""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ No GEMINI_API_KEY found in environment")
        return False
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Test with simple query
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content("Explain how AI works in a few words")
        
        print("✅ Gemini API Connection Successful!")
        print(f"📝 Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Gemini API Test Failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Gemini API Connection...")
    success = test_gemini_api()
    
    if success:
        print("\n🎉 Gemini is ready for your RAG system!")
        print("💡 Try running: streamlit run app.py")
    else:
        print("\n⚠️  Please check your API key and try again")
