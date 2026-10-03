from agent.agent import run_agent


def main():

    print("=" * 60)
    print("🇮🇳 India Weather & News Agent")
    print("=" * 60)

    print("Ask about:")
    print("- Weather of Indian cities")
    print("- Current news")
    print("- Recent events")
    print()
    print("Type 'exit' to quit.")
    print()

    while True:

        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        try:

            answer = run_agent(user_input)

            print()
            print("Agent:")
            print(answer)
            print()

        except Exception as e:

            print()
            print("Error:", e)
            print()


if __name__ == "__main__":
    main()