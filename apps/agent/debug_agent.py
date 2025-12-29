from langgraph.prebuilt import create_react_agent
import inspect

print("\n=== AGENT SIGNATURE DIAGNOSIS ===")
print(inspect.signature(create_react_agent))
print("=================================\n")