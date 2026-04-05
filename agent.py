# agent.py

from langchain.agents import Tool, initialize_agent, AgentType
from langchain_community.llms import Ollama
from agent_tools import pricing_tool


# -------------------------------
# 1. Load Local LLM (Ollama)
# -------------------------------
llm = Ollama(model="mistral")


# -------------------------------
# 2. Define Tools
# -------------------------------
tools = [
    Tool(
        name="Pricing Tool",
        func=pricing_tool,
        description="""
        You MUST use this tool for ALL pricing calculations.

        ⚠️ STRICT FORMAT:
        - Use EXACTLY this tool name: Pricing Tool
        - DO NOT use brackets like [Pricing Tool]
        - DO NOT change the name

        Correct format:
        Action: Pricing Tool
        Action Input: price bond 1000 0.05 5

        Supported inputs:
        - price bond <face_value> <rate> <time>
        - price option <S> <K> <T> <r> <sigma>
        - price eln <S> <r> <sigma>
        """
    )
]
# -------------------------------
# 3. Initialize Agent
# -------------------------------
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# -------------------------------
# 4. Run Interactive Loop
# -------------------------------
def main():
    print("💡 Financial Pricing Agent Ready (type 'exit' to quit)\n")

    while True:
        try:
            query = input("Ask: ")

            if query.lower() in ["exit", "quit"]:
                print("👋 Exiting agent.")
                break

            # Run agent
            result = agent.run(query)

            print("\n✅ Result:", result)
            print("-" * 50)

        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


# -------------------------------
# 5. Entry Point
# -------------------------------
if __name__ == "__main__":
    main()