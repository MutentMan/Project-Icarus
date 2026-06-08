
from duckduckgo_search import DDGS
from rich.console import Console

console = Console()

def search_web(query: str, config: dict = None, max_results=5, site_filter=None):
    results = []
    
    full_query = query
    if site_filter:
        full_query = f'"{query}" site:{site_filter}'
        
    try:
        with DDGS() as ddgs:
            # text search
            ddg_results = list(ddgs.text(full_query, max_results=max_results))
            for r in ddg_results:
                title = r.get('title', '')
                body = r.get('body', '')
                href = r.get('href', '')
                
                # RELEVANCE FILTER: Ensure the query exists in title or snippet
                # We normalize to lowercase for matching
                search_term = query.lower().replace('"', '') # Clean up quotes for matching
                if search_term in title.lower() or search_term in body.lower() or search_term in href.lower():
                    results.append({
                        "title": title,
                        "href": href,
                        "body": body
                    })
    except Exception as e:
        # Fallback or error logging
        pass
        
    return results

def search_documents(query: str, config: dict = None, max_results=5):
    # Dorks for documents
    dork = f'"{query}" (filetype:pdf OR filetype:docx OR filetype:xlsx OR filetype:csv OR filetype:txt)'
    return search_web(dork, config, max_results)

if __name__ == "__main__":
    # Test
    res = search_web("test@example.com")
    print(res)
