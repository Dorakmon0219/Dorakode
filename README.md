# Dorakode

**一个用 Python 实现的终端 AI 编码代理，实践 `learn-claude-code` 的 harness 工程思想并做自定义加强。**

Dorakode 基于 [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) 的核心论断——**Agency 来自模型训练，Harness 才是工程师该建的东西**——把课程里的 harness 机制落地成一个真实可用的 CLI。

## 它是什么

用自然语言描述任务，Dorakode 在终端里读代码、改文件、跑命令、看结果，出错就自己调整，直到验证通过。

```bash
dorakode "修复 pytest 失败的用例"
dorakode "把 src/utils 里的回调改成 async/await"
dorakode # 进入交互式 REPL
```

"Humans steer. Agents execute."

## 设计原则

1. **循环恒定，机制可插拔。** Agent loop 永远只有一条：调模型 → 调工具 → 回填结果 → 调工具。新能力以 handler 或 hook 注册，不重写循环。
2. **模型决定，harness 执行。** 代码不替模型做决策，只提供动作空间、上下文和边界。
3. **按需加载。** 技能、项目知识、记忆都在需要时加载，避免上下文被无效信息占满。
4. **权限先于自由。** 每个有副作用的工具调用都经过权限规则，破坏性操作必须显式批准。

## 开发计划

| 阶段 | 机制 | Dorakode 模块 | 状态 |
|---|---|---|---|
| s01 Agent Loop | `messages[]` + `while True` | `dorakode/agent/loop.py` | 规划中 |
| s02 Tool Use | `TOOL_HANDLERS` 分发表 | `dorakode/tools/registry.py` | 规划中 |
| s03 Permission | 审批流水线 | `dorakode/permissions/` | 规划中 |
| s04 Hooks | `PreToolUse` / `PostToolUse` | `dorakode/hooks/` | 后续 |
| s05 TodoWrite | plan-then-execute | `dorakode/planning/` | 后续 |
| s06 Subagent | 独立 `messages[]` 上下文隔离 | `dorakode/agent/subagent.py` | 后续 |
| s07 Skill Loading | 按需注入技能目录 | `dorakode/skills/` | 后续 |
| s08 Context Compact | 四级压缩策略 | `dorakode/context/compact.py` | 后续 |
| s09 Memory | 选择 / 提取 / 固化 | `dorakode/memory/` | 后续 |
| s10 Task System | 磁盘持久化任务图 | `dorakode/tasks/` | 后续 |
| s11 Background Tasks | 线程执行 + 通知队列 | `dorakode/tasks/background.py` | 后续 |
| s12 Cron Scheduler | 定时触发 | `dorakode/scheduler/` | 后续 |
| s13 Agent Teams | 队友 + 原子任务认领 + worktree | `dorakode/teams/` | 后续 |
| s14 MCP Plugin | 外部工具并入同一工具池 | `dorakode/mcp/` | 后续 |
| s15 Integrated Harness | 多机制共用一条 loop | `dorakode/runtime/` | 后续 |
| s16 Workflow Runtime | 脚本编排 + 日志恢复 | `dorakode/workflow/` | 后续 |
| s17 Goal Loop | 独立评估器决定是否停止 | `dorakode/goal/` | 后续 |

## 项目状态

Dorakode 目前状态：**未开始**

## 快速开始

> 仓库刚起步，以下命令待 CLI 入口落地后生效。

环境要求：Python 3.11+

```bash
git clone https://github.com/Dorakmon0219/Dorakode.git
cd Dorakode
uv sync
```

配置模型（兼容 Anthropic / OpenAI 接口）：

```bash
cp .env.example .env
# 编辑 .env，填入 ANTHROPIC_API_KEY 或 DORAKODE_API_KEY
```

运行：

```bash
uv run python -m dorakode # 交互式 REPL
uv run python -m dorakode "修复 pytest 失败的用例"  # 单次任务
```

安装为全局命令（可选）：

```bash
uv pip install -e .
dorakode "解释 src/parser.py 的逻辑"
```
## 技术栈

- **语言**：Python 3.11+
- **CLI**：`argparse` / `click`
- **模型接口**：Anthropic SDK，兼容 OpenAI 接口
- **依赖管理**：`pyproject.toml` + `uv`（`uv.lock` 锁定版本）

## 致谢

设计思想与机制拆解来自 [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code)。

## License

MIT