class PearlRouter:
    """
    Routes user queries to system actions, live web search, or specific LLM parameters.
    """
    
    @staticmethod
    def route_query(query):
        query_clean = query.lower().strip()

        # Keywords for live web search
        search_keywords = [
            "search", "google", "weather", "latest", "news", 
            "who is", "what is the price", "today", "current", "score"
        ]

        # Keywords for system actions
        system_keywords = [
            "volume", "mute", "brightness", "screenshot", 
            "open", "launch", "close app"
        ]

        if any(k in query_clean for k in search_keywords):
            return {
                "route": "WEB_SEARCH",
                "model": "llama-3.3-70b-versatile",
                "max_tokens": 400
            }

        if any(k in query_clean for k in system_keywords):
            return {
                "route": "SYSTEM_ACTION",
                "model": None,
                "max_tokens": None
            }

        # Default fast route for general conversation
        return {
            "route": "LLM_FAST",
            "model": "llama-3.3-70b-versatile",
            "max_tokens": 300
        }