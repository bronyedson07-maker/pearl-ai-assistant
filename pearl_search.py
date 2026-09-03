from ddgs import DDGS

class PearlSearchEngine:
    """
    Performs real-time web searches using DDGS (No API key required).
    """
    
    @staticmethod
    def search_web(query, max_results=3):
        """Searches the live web and returns formatted snippets."""
        try:
            results = []
            ddgs = DDGS()
            search_results = ddgs.text(query, max_results=max_results)
            
            for r in search_results:
                results.append(f"• Title: {r.get('title')}\n  Snippet: {r.get('body')}\n  URL: {r.get('href')}")
            
            if not results:
                return "No relevant search results found."
                
            return "\n\n".join(results)
        except Exception as e:
            return f"Search error: {e}"