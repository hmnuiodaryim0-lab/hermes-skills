---
name: travel-research
description: 旅行目的地深度研究工作流——输入城市名，输出完整旅行研究报告（历史分层/博物馆/古建/考古/美食/路线），并生成信息图。支持大陆/海外路线规划：境内调用高德地图（amap skill），境外调用 Google Maps。
category: productivity
---

# 旅行目的地深度研究技能

输入：城市名（或地区名）
输出：完整 .org 格式旅行研究报告 + 路线规划 + 信息图

---

## 工作流

### 第一步：城市画像 + 六维度并行研究

用 Brave Search 并行搜索以下六个维度：

```
1. {城市} 历史沿革 古代文明
2. {城市} 博物馆 推荐 必去
3. {城市} 古建筑 文物保护单位
4. {城市} 考古发现 遗址
5. {城市} 人文 民族文化 民俗
6. {城市} 美食 特产 必吃
```

同时搜索：景点门票/开放时间/交通方式/最佳季节

---

### 第二步：判断境内/境外（关键步骤）

**必须执行此步骤来决定后续路线工具。**

用 AMap 地理编码探测目的地：

```bash
# 在 ~/.hermes/skills/amap/scripts/ 目录下执行
AMAP_MAPS_API_KEY=$AMAP_MAPS_API_KEY python amap.py geocode --address "{目的城市}" --city "{目的城市}"
```

检查返回结果：

- **province 字段非空**（包含"省"、"市"、"自治区"等中文行政区划）→ **大陆境内**，路线用高德地图（amap skill）
- **province 字段为空**或 geocode 失败 → **境外**，路线用 Google Maps（通过 web 搜索获取驾车/公交路线）

---

### 第三步：整理报告结构

按以下大纲组织内容（.org 格式）：

```org
#+title: {城市}旅行研究
#+date: {日期}
#+filetags: :travel:

* 城市概览
地理位置、文明坐标（3-5句话）

* 历史分层
** 古代时期（旧石器—明清）
** 近代动荡期（晚清—民国）
** 红色记忆期/现代（20世纪后）

* 博物馆指南
** {博物馆名}（★★★★★ 必去）
- 地位/开放时间/预约方式
*** 镇馆之宝
*** 重点展厅
*** 容易错过

* 古建遗存
** {遗迹名}（年代/文保级别）
- 看点

* 考古发现
** {遗址/沉舰等}
- 发现意义

* 参观路线
（路线内容根据境内/境外判断，见第四步）

* 美食体系
** 必吃清单
| 美食 | 特点 | 推荐理由 |

** 美食地点推荐
...

* 实用信息
** 最佳季节
** 交通
** 注意事项
```

---

### 第四步：路线规划（境内/境外分支）

#### 境内路线（大陆城市，使用高德地图）

调用 amap skill（`~/.hermes/skills/amap/scripts/amap.py`）：

```bash
# 地理编码获取坐标（注意：必须从 amap/scripts/ 目录运行，或用全路径）
AMAP_MAPS_API_KEY=$AMAP_MAPS_API_KEY python ~/.hermes/skills/amap/scripts/amap.py geocode --address "{景点A}" --city {城市}

# 驾车路线（坐标模式，坐标格式为 经度,纬度）
AMAP_MAPS_API_KEY=$AMAP_MAPS_API_KEY python ~/.hermes/skills/amap/scripts/amap.py drive-route-coords --origin {坐标A} --destination {坐标B}

# 步行路线
AMAP_MAPS_API_KEY=$AMAP_MAPS_API_KEY python ~/.hermes/skills/amap/scripts/amap.py walk-route-coords --origin {坐标A} --destination {坐标B}

# 骑行路线
AMAP_MAPS_API_KEY=$AMAP_MAPS_API_KEY python ~/.hermes/skills/amap/scripts/amap.py bike-route-coords --origin {坐标A} --destination {坐标B}

# 公交路线
AMAP_MAPS_API_KEY=$AMAP_MAPS_API_KEY python ~/.hermes/skills/amap/scripts/amap.py transit-route-coords --origin {坐标A} --destination {坐标B} --city {出发城市} --cityd {目的城市}

# 距离测量（多起点，用 | 分隔）
AMAP_MAPS_API_KEY=$AMAP_MAPS_API_KEY python ~/.hermes/skills/amap/scripts/amap.py distance --origins "{坐标1}|{坐标2}" --destination {坐标B} --type 1
```

> 注意：参数 `--type` 在 distance 命令中控制距离计算方式（0=直线距离，1=驾车距离，3=公交距离）。

将路线结果（距离、耗时、途经道路）填入报告的"参观路线"章节。

#### 境外路线（海外/港澳台，使用 Google Maps）

通过 Brave Search 搜索路线：

```
{出发地} to {目的地} driving directions Google Maps
{出发地} to {目的地} public transit directions
```

或者直接用浏览器工具访问 `https://www.google.com/maps/dir/{出发地}/{目的地}` 获取路线摘要。

将搜索结果中的关键信息（路线距离、预计车程/时长、途经高速公路）填入报告。

---

### 第五步：保存文档

```bash
mkdir -p ~/Documents/notes
path="~/Documents/notes/$(date '+%Y%m%dT%H%M%S')==z--{城市}旅行研究.org"
# 写入整理好的 org 内容
```

---

### 第六步：生成信息图

用 `nano-banana-2-beta` 生成城市信息图（异步模式）：

```bash
# 1. 提交任务
curl -X POST https://api.evolink.ai/v1/images/generations \
  -H "Authorization: Bearer $EVOLINK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nano-banana-2-beta",
    "prompt": "旅行信息图，{城市}旅行指南，包含：最佳季节、必去景点、美食推荐、交通方式。中文设计，清晰易读，信息丰富",
    "size": "1024x1024",
    "num_images": 1
  }'

# 2. 轮询任务状态（等待约30-60秒）
curl -X GET "https://api.evolink.ai/v1/tasks/{task_id}" \
  -H "Authorization: Bearer $EVOLINK_API_KEY"

# 3. 成功后从 data[0].url 下载图片
```

---

## 工具依赖

| 工具 | 用途 | 技能 |
|------|------|------|
| Brave Search | 城市研究、境外路线搜索 | 内置 web 工具 |
| amap.py | 大陆境内地理编码、路线规划 | amap skill |
| Google Maps | 境外路线获取 | Brave Search / 浏览器 |
| evolink (nano-banana-2-beta) | 信息图生成 | 内置 image_gen |

---

## 注意事项

- **第二步（境内/境外判断）不可跳过**，路线工具选择取决于此结果
- 历史分层至少覆盖：古代（旧石器—明清）、近代（晚清—民国）、现代（20世纪后）三个时期
- 博物馆标注星级（★★★★★ 必去 / ★★★★ 推荐）
- 路线按主题分类：红色记忆/边境风情/自然风光/深度人文
- 出图 API 为异步，需轮询；图片保存后路径加入报告末尾
- 依赖工具：Brave Search（搜索）、curl（出图 API）
