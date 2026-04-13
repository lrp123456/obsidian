# OpenCode AGENTS 配置

本文件定义了项目可用的 agents 和 skills。

## Skills

### python-tutor

**描述**：Python 进阶导师 - 互动教学与文档生成

**用途**：
- 针对具备 Java/Spring Cloud 背景的学习者进行 Python 进阶教学
- 生成标准化的 Markdown 格式学习文档
- 覆盖 asyncio、装饰器、LangChain、LlamaIndex 等进阶主题

**触发方式**：
```
/python-tutor
```

**文件位置**：`skills/python-tutor.md`

---

## 架构说明

```
Obsidian Vault/
├── skills/
│   └── python-tutor.md    # Python 教学技能定义
├── AGENTS.md              # 本文件 - agents/skills 注册表
├── CLAUDE.md              # Claude Code 配置（原始）
└── Python学习/             # 生成的学习文档存放目录
```

## 添加新 Skill

1. 在 `skills/` 目录创建 `*.md` 文件
2. 使用 `## Skill: skill-name` 格式开头
3. 包含 `**Base directory**:` 字段
4. 在本文件的 Skills 部分注册
