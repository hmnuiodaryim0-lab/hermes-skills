---
name: hermes-skill-install
description: 从 GitHub 安装 Hermes Agent 技能，处理嵌套 SKILL.md 结构
triggers:
  - "安装技能"
  - "install skill from github"
  - "clone skill"
---

# hermes-skill-install：从 GitHub 安装 Hermes 技能

## 常用技能库

| 来源 | 地址 |
|------|------|
| 官方精选列表 | https://github.com/0xNyk/awesome-hermes-agent |
| wondelai/skills（跨平台，380+ stars） | https://github.com/wondelai/skills |

## 安装步骤

### 1. 克隆到临时目录

```bash
git clone https://github.com/REPO.git /tmp/skill-repo
```

### 2. 查找所有 SKILL.md 文件

```bash
find /tmp/skill-repo -type f -name "SKILL.md"
```

一个仓库可能有多个技能（如 `skills/bazi-mingli/SKILL.md` 和 `skills/cyber-cultivation/SKILL.md`）。

### 3. 迁移每个技能到 ~/.hermes/skills/

技能目录结构要求：`~/.hermes/skills/<skill-name>/SKILL.md`

对于嵌套的技能目录（如 `repo/skills/<name>/SKILL.md`）：

```bash
# 克隆到临时位置
git clone https://github.com/USER/repo.git /tmp/repo

# 创建目标目录
mkdir -p ~/.hermes/skills/<skill-name>

# 移动文件
mv /tmp/repo/skills/<name>/SKILL.md ~/.hermes/skills/<skill-name>/

# 如果有 references 目录也一起移
mv /tmp/repo/skills/<name>/references ~/.hermes/skills/<skill-name>/

# 书籍等额外文件（如果有）看情况处理
mv /tmp/repo/books ~/.hermes/skills/<skill-name>/  # 可选
```

### 4. 验证安装

```bash
ls ~/.hermes/skills/<skill-name>/
```

常见文件结构：
- `SKILL.md` — 必须，技能主文件
- `references/` — 可选，参考资料
- `scripts/` — 可选，脚本文件

## 特殊情况

- **多技能仓库**：一个 repo 可能有多个技能，需要拆分成独立目录
- **Hermes 官方 hub**：`hermes skills` 命令可以直接搜索安装（如果可用）
- **私有技能**：用户提供文件或链接，手动按上述流程安装
