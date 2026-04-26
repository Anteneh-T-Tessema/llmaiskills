import sys
from src.crew import run_agency

def main():
    if len(sys.argv) > 1:
        topic = sys.argv[1]
    else:
        topic = "The impact of Local AI on small businesses"

    print(f"🚀 Starting Viral Content Agency for topic: {topic}\n")
    result = run_agency(topic)
    
    print("\n" + "="*30)
    print("✨ FINAL CONTENT PLAN ✨")
    print("="*30)
    print(result)

if __name__ == "__main__":
    main()
