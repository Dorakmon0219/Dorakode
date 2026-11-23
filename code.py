import os
try:
    import readline
    # 修复 macOS 的 libedit 处理中文输入时的退格问题
    readline.parse_and_bind('set bind-tty-special-chars off')
    readline.parse_and_bind('set input-meta on')
    readline.parse_and_bind('set output-meta on')
    readline.parse_and_bind('set convert-meta off')
except ImportError:
    pass
from anthropic import Anthropic
from dotenv import load_dotenv
from tools import *

load_dotenv(override = True)

base_url = os.getenv("DORAKODE_BASE_URL")
api_key = os.getenv("DORAKODE_API_KEY")
MODEL = os.environ["MODEL_ID"]

if base_url:
    os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)
client = Anthropic(base_url = base_url, api_key = api_key)
SYSTEM = f"You are a coding agent at {os.getcwd()}. Use the given tools to act, don't explain."

def agent_loop(messages: list):
    # Agent loop
    while True:
        response = client.messages.create(
            model = MODEL,
            system = SYSTEM,
            tools = TOOLS,
            max_tokens = 8000,
            messages = messages,
        )

        # Append the assistant's response to the messages list
        messages.append({"role": "assistant", "content": response.content})

        # TODO: Handle stop_reason properly, currently just return if end_turn
        if response.stop_reason == "end_turn":
            return

        # Execute each tool call, collect results
        results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"\033[33m$ {block.input['command']}\033[0m")
                output = run_bash(block.input["command"])
                print(output[:200])
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })
        # Feed tool results back, loop continues
        messages.append({"role": "user", "content": results})


# main
if __name__ == "__main__":
    print("\n----------------Dorakode is all you need----------------\n")
    print("输入问题，回车发送。输入 q / exit 退出。\n")
    history = []
    while True:
        try:
            query = input("\033[36mdorakode >> \033[0m")
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() in ("q", "exit", ""):
            break
        history.append({"role": "user", "content": query})
        agent_loop(history)
        # Print the model's final text response
        response_content = history[-1]["content"]
        if isinstance(response_content, list):
            for block in response_content:
                if getattr(block, "type", None) == "text":
                    print(block.text)
        print()



