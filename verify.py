
import asyncio
import sys
import os

# Add root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core import IcarusCore

async def test_icarus():
    icarus = IcarusCore()
    
    print("--- Testing Input Detection ---")
    inputs = [
        ("test@example.com", "email"),
        ("+14155552671", "phone"),
        ("https://github.com/octocat", "url"),
        ("octocat", "handle")
    ]
    
    for inp, expected in inputs:
        detected = icarus.detect_type(inp)
        print(f"Input: {inp} | Expected: {expected} | Detected: {detected} | {'PASS' if expected == detected else 'FAIL'}")

    print("\n--- Testing Social Search (GitHub: octocat) ---")
    # This will actually hit GitHub, so it verifies network and logic
    await icarus.run_search("octocat")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_icarus())
