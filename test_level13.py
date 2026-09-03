from pearl_search import PearlSearchEngine

def main():
    searcher = PearlSearchEngine()

    print("--- Pearl Level 13: Live Web Search Test ---\n")

    query = "latest artificial intelligence developments"
    print(f"Searching for: '{query}'...\n")

    results = searcher.search_web(query, max_results=3)

    print("Search Results:")
    print("-" * 50)
    print(results)
    print("-" * 50)

if __name__ == "__main__":
    main()