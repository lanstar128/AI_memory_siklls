---
name: conversation-archive
description: |
  对话归档技能。在用户完成工作或明确要求保存时，引导用户导出对话并归档。
  触发条件：用户说"保存对话"/"归档"/"记录一下"，或检测到离开意图（"今天就到这"/"提交代码吧"）。
  用于指导 AI 如何正确地归档对话记录，包括时间戳提取和索引管理。
compatibility: Claude Code, Gemini CLI, OpenAI Codex, iFlow CLI
metadata:
  author: lanstar128
  version: "1.0"
---

# 对话归档技能

本技能指导 AI 在用户完成工作时，引导用户导出对话并进行归档处理。

---

## 一、触发条件

### 1.1 主动触发（用户明确要求）
- 用户说"保存对话"、"归档一下"、"记录这次对话"
- 用户说"帮我保存"、"存一下"

### 1.2 被动触发（检测到离开意图）
- 用户说"今天就到这"、"我先忙了"、"下次继续"
- 用户说"提交代码吧"、"commit 一下"
- 明显的任务完成迹象

---

## 二、执行流程

### 2.1 模式选择

根据上下文自动选择模式：

- **模式 A：标准归档 (AI Self-Archive)**
  - 适用：Gemini CLI, Claude Code, Codex, iFlow
  - 触发：默认模式。当用户没有提供导出文件，仅要求"保存"或"归档"时。
  
- **模式 B：文件导入 (File Import)**
  - 适用：Antigravity IDE (或手动导出文件的用户)
  - 触发：用户说"我导出了文件"、"文件在这里"或提供了文件路径。

---

### 2.2 模式 A：标准归档 (默认)

**步骤 1：生成归档内容**
AI 总结当前上下文，生成 Markdown 内容（直接写入目标文件）：

- **路径**：`~/.gemini/memory/conversations/<YYYY-MM>/<YYYY-MM-DD>_<标题>.md`
  *(标题：使用连字符命名，如 `fix-react-hook-error`)*
- **内容格式**：
  ```markdown
  ---
  archived_at: <当前时间 YYYY-MM-DD HH:MM>
  title: <对话标题>
  ---
  
  # <对话标题>
  
  ## 📌 摘要
  <100字以内的对话总结，包含核心解决的问题>
  
  ## 📝 关键交互记录
  
  ### User Input
  <复述用户的关键提问或报错信息>
  
  ### AI Response
  <复述 AI 的关键对策或代码方案>
  
  (仅保留关键轮次，去除闲聊)
  ```

**步骤 2：生成元数据索引**
创建临时索引文件 `/tmp/archive_meta.json`：
```json
{
  "conversation_title": "<对话标题>",
  "archive_time": "<当前时间 YYYY-MM-DD HH:MM>",
  "turns": [
    {"index": 1, "time": "", "first_line": "<摘要第一句>"}
  ]
}
```

**步骤 3：入库与同步**
```bash
# 添加到索引
python3 ~/.gemini/skills/conversation-archive/scripts/db_manager.py \
  --action add \
  --metadata /tmp/archive_meta.json \
  --file ~/.gemini/memory/conversations/<YYYY-MM>/<YYYY-MM-DD>_<标题>.md

# 清理临时文件
rm /tmp/archive_meta.json

# Git 同步
git -C ~/.gemini add . && git -C ~/.gemini commit -m "auto: archive <标题>" && git -C ~/.gemini push
```

---

### 2.3 模式 B：文件导入 (IDE 增强)

**步骤 1：引导/扫描**
```
检测到导出文件。正在处理...
```
扫描 `~/Downloads/` 下最新的 `.md` 文件。

**步骤 2：提取元数据**
从文件内容或 `ADDITIONAL_METADATA` 提取时间戳和标题，生成 `/tmp/archive_metadata.json`。
*(参考 `scripts/inject_timestamps.py` 的逻辑)*

**步骤 3：注入与归档**
```bash
# 注入时间戳并移动到全局目录
python3 ~/.gemini/skills/conversation-archive/scripts/inject_timestamps.py \
  --source <源文件> \
  --metadata /tmp/archive_metadata.json \
  --output ~/.gemini/memory/conversations/

# 更新索引
python3 ~/.gemini/skills/conversation-archive/scripts/db_manager.py \
  --action add \
  --metadata /tmp/archive_metadata.json \
  --file <输出的归档文件路径>

# 去重检查 (仅在此模式下执行，防止多次导出)
python3 ~/.gemini/skills/conversation-archive/scripts/dedup_archives.py \
  --dir ~/.gemini/memory/conversations/<YYYY-MM>/

# 清理
rm /tmp/archive_metadata.json

# Git 同步
git -C ~/.gemini add . && git -C ~/.gemini commit -m "auto: import <标题>" && git -C ~/.gemini push
```

---

## 三、存储结构

```
~/.gemini/memory/
├── conversations/          # 对话原文
│   ├── 2026-01/
│   │   └── 2026-01-18_对话归档技能讨论.md
│   └── 2026-02/
│       └── ...
├── conversations.db        # SQLite 索引
└── index_backup.json       # JSON 备份
```

> [!NOTE]
> 所有对话保存在全局目录，便于统一备份和跨设备同步。

---

## 四、检索历史对话

当用户需要查找历史对话时：
```bash
python3 ~/.gemini/skills/conversation-archive/scripts/db_manager.py \
  --action search \
  --keyword "关键词" \
  --date-range "2026-01-01,2026-01-31"
```

---

## 五、相关脚本

| 脚本 | 功能 |
|------|------|
| `scripts/inject_timestamps.py` | 将时间戳注入 Markdown 文件 |
| `scripts/db_manager.py` | SQLite 索引管理（增删查） |

---

*Created: 2026-01-18*
