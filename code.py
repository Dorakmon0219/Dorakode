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
    while True:
        response = client.messages.create(
            model=MODEL,
            system=SYSTEM,
            tools=TOOLS,
            max_tokens=8000,
            messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})

        # 正常结束：返回本轮 assistant 内容
        if response.stop_reason == "end_turn":
            return response.content

        # 被截断：不要执行可能不完整的 tool_use
        if response.stop_reason == "max_tokens":
            print("\033[31m[警告] 回复被 max_tokens 截断，本轮中止\033[0m")
            return response.content

        # 其他非工具原因（refusal / stop_sequence 等）：直接返回
        if response.stop_reason != "tool_use":
            return response.content

        # 执行工具
        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            try:
                # 按工具名分发，避免硬编码 command
                if block.name == "bash":
                    print(f"\033[33m$ {block.input['command']}\033[0m")
                    output = run_bash(block.input["command"])
                else:
                    output = f"未知工具: {block.name}"
            except Exception as e:
                output = f"工具执行出错: {e}"
            print(output[:250])
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": output,
            })

        # 没有工具结果就不要 append 空 content，避免 API 400
        if not results:
            return response.content

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
        final_content = agent_loop(history)
        if final_content:
            for block in final_content:
                if getattr(block, "type", None) == "text":
                    print(block.text)
        print()



