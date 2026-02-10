
import asyncio
import sys
import os

# Add root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules import web_search, ai_analyst

async def test_phase4():
    print("--- Testing Document Search ---")
    try:
        results = web_search.search_documents("project icarus osint", max_results=3)
        if results and any(r['href'].endswith(('.pdf', '.doc', '.txt', '.docx')) or 'pdf' in r['title'].lower() for r in results):
             print(f"[PASS] Document Search returned {len(results)} items.")
        else:
             print(f"[WARN] Document Search returned {len(results)} items, but maybe no obvious PDFs (could be normal).")
             if results: print(f"Sample: {results[0]['href']}")
    except Exception as e:
        print(f"[ERROR] Document Search Exception: {e}")

    print("\n--- Testing AI Analyst (Mock) ---")
    mock_config = {
        "ai_engine": {
            "enabled": True,
            "base_url": "http://mock-url",
            "model": "test-model"
        }
    }
    
    # We expect a connection error or a specific mock behavior, but we just testing import and structural call
    res = await ai_analyst.analyze_report("test_target", [{"data": "test"}], mock_config)
    
    if "AI Connection Failed" in res or "AI Error" in res:
        print(f"[PASS] AI Module called correctly (Graceful failure on missing server: {res})")
    else:
        print(f"[?] AI Response: {res}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_phase4())
