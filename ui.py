# ui.py —— 统一输出入口，分离"日志层"和"回答层"
import sys

RESET = "\033[0m"
DIM   = "\033[90m"
RED   = "\033[31m"
YEL   = "\033[33m"
MAG   = "\033[35m"
CYN   = "\033[36m"
GRN   = "\033[32m"

def _p(s, color=""):
    print(color + s + (RESET if color else ""))

def info(msg):
    _p(msg, DIM)

def tool(name, args):
    preview = " ".join(str(args).split())          # 折叠换行
    if len(preview) > 160:
        preview = preview[:160] + "…"
    _p(f"▸ {name} {preview}", MAG)

def cmd(c):
    _p(f"  $ {c}", YEL)

def warn(msg):
    _p(f"⚠ {msg}", RED)

def deny(msg):
    _p(f"⛔ {msg}", RED)

def result(out):
    body = "\n".join("  │ " + ln for ln in str(out).splitlines())
    _p(body, DIM)

def answer(text):
    _p("\n" + "═" * 8 + " 回答 " + "═" * 8, CYN)
    print(text)