# hermes-skills

Hermes Agent 个性化技能集合 —— 仅保存自建、自定义、自更新的技能，不含内置bundled技能。

## 当前个性化技能

| 技能 | 说明 |
|------|------|
| bazi-mingli | 八字/命理分析，基于中国古典典籍（渊海子平、三命通会、滴天髓、穷通宝鉴、子平真诠、千里命稿、神峰通考、果老星宗、协纪辨方等） |
| cyber-cultivation | 赛博修仙：AI知识引擎与实修向导，以现代神经科学与认知心理学解析道家内丹、佛家禅定等实修体系 |
| travel-research | 旅行目的地深度研究工作流，输入城市名，输出完整旅行研究报告（历史分层/博物馆/古建/考古/美食/路线）+ 信息图 |

## 内置技能（不保存在此仓库）

以下为 Hermes Agent 内置bundled技能，请通过官方渠道更新，不在此仓库管理：

apple, autonomous-ai-agents, creative, data-science, devops, diagramming, dogfood, domain, email, feeds, gaming, gifs, github, inference-sh, leisure, mcp, media, mlops, note-taking, productivity, red-teaming, research, smart-home, social-media, software-development

## 同步方式

本地更新技能后，若需同步到此仓库：

```bash
cd ~/.hermes/skills

# 只提交个性化技能
git add bazi-mingli cyber-cultivation travel-research
git commit -m "update: ..."
git push origin main
```

## 安装个性化技能

```bash
hermes skills install hmnuiodaryim0-lab/hermes-skills bazi-mingli
hermes skills install hmnuiodaryim0-lab/hermes-skills cyber-cultivation
hermes skills install hmnuiodaryim0-lab/hermes-skills travel-research
```
