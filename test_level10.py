from pearl_persistent_memory import PearlPersistentMemory

def main():
    memory = PearlPersistentMemory()

    print("--- Pearl Level 10: Persistent Memory Test ---\n")

    # 1. Store Facts
    print("[Saving Memories...]")
    print(memory.remember("Pearl is my main AI assistant project.", category="project"))
    print(memory.remember("Preferred output style is concise and friendly.", category="preference"))

    # 2. Recall All Stored Facts
    print("\n[Recalling Memories...]")
    memories = memory.recall_all()
    for mem_id, cat, fact in memories:
        print(f"  • [ID: {mem_id}] ({cat.upper()}): {fact}")

    # 3. Clean up test entries (Optional)
    print("\n[Database Location]:", memory.db_path)

if __name__ == "__main__":
    main()