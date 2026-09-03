from pearl_router import PearlRouter

def main():
    router = PearlRouter()
    
    test_queries = [
        "Open Chrome",
        "Hi Pearl",
        "Set volume to 50",
        "Can you explain how quantum computing works in detail?",
        "What is the capital of France?",
        "Take a screenshot"
    ]

    print("--- Pearl Level 6/7: Intelligent Router Test ---\n")

    for q in test_queries:
        decision = router.route_query(q)
        print(f"Query:    '{q}'")
        print(f"Route:    {decision['route']}")
        print(f"Model:    {decision['model']}")
        print(f"Tokens:   {decision['max_tokens']}")
        print("-" * 45)

if __name__ == "__main__":
    main()