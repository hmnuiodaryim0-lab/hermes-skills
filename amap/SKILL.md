---
name: amap
description: 高德地图 Web Service API 调用工具，支持地理编码、逆地理编码、IP 定位、天气查询、路径规划（骑行/步行/驾车/公交）、距离测量、POI 搜索。用户要求"查地址坐标"、"规划路线"、"天气"、"附近搜索"、"两地距离"时使用本技能。
---

# AMap 高德地图技能

## 环境要求

- Python 3 标准库（无需额外依赖）
- 环境变量 `AMAP_MAPS_API_KEY` 必须设置

## 命令速查

| 命令 | 说明 | 必填参数 |
|------|------|---------|
| `geocode` | 地理编码（地址 → 坐标） | `--address` |
| `reverse-geocode` | 逆地理编码（坐标 → 地址） | `--location` |
| `ip-location` | IP 定位 | `--ip` |
| `weather` | 天气查询 | `--city` |
| `bike-route-coords` | 骑行路线（坐标） | `--origin`, `--destination` |
| `bike-route-address` | 骑行路线（地址，自动转坐标） | `--origin-address`, `--destination-address` |
| `walk-route-coords` | 步行路线（坐标） | `--origin`, `--destination` |
| `walk-route-address` | 步行路线（地址，自动转坐标） | `--origin-address`, `--destination-address` |
| `drive-route-coords` | 驾车路线（坐标） | `--origin`, `--destination` |
| `drive-route-address` | 驾车路线（地址，自动转坐标） | `--origin-address`, `--destination-address` |
| `transit-route-coords` | 公交路线（坐标） | `--origin`, `--destination`, `--city`, `--cityd` |
| `transit-route-address` | 公交路线（地址，自动转坐标） | `--origin-address`, `--destination-address`, `--origin-city`, `--destination-city` |
| `distance` | 距离测量 | `--origins`, `--destination` |
| `poi-text` | POI 关键字搜索 | `--keywords` |
| `poi-around` | POI 附近搜索 | `--location` |
| `poi-detail` | POI 详情查询 | `--id` |

## 工作流程

1. 确认用户需求，选择合适的命令
2. 用户提供地址时，优先使用 `*-route-address` 系列命令（自动处理地理编码）
3. 用户提供坐标时，使用 `*-route-coords` 系列命令
4. 调用脚本，解析 JSON 结果
5. 将关键信息格式化返回给用户

## 调用示例

```bash
# 地理编码
AMAP_MAPS_API_KEY=$AMAP_MAPS_API_KEY python ~/.hermes/skills/amap/scripts/amap.py geocode --address "北京市朝阳区阜通东大街6号" --city 北京

# 逆地理编码
AMAP_MAPS_API_KEY=$AMAP_MAPS_API_KEY python ~/.hermes/skills/amap/scripts/amap.py reverse-geocode --location 116.481488,39.990464

# 天气查询
AMAP_MAPS_API_KEY=$AMAP_MAPS_API_KEY python ~/.hermes/skills/amap/scripts/amap.py weather --city 北京 --extensions all

# 骑行路线（地址）
AMAP_MAPS_API_KEY=$AMAP_MAPS_API_KEY python ~/.hermes/skills/amap/scripts/amap.py bike-route-address --origin-address "北京市朝阳区阜通东大街6号" --destination-address "北京市海淀区上地十街10号" --origin-city 北京 --destination-city 北京

# POI 搜索
AMAP_MAPS_API_KEY=$AMAP_MAPS_API_KEY python ~/.hermes/skills/amap/scripts/amap.py poi-text --keywords "咖啡" --city 110108 --citylimit true

# 距离测量
AMAP_MAPS_API_KEY=$AMAP_MAPS_API_KEY python ~/.hermes/skills/amap/scripts/amap.py distance --origins "116.481488,39.990464|116.434307,39.90909" --destination "116.315613,39.998935" --type 1
```

## API Key 配置

将以下内容加入 `~/.hermes/.env`：

```
AMAP_MAPS_API_KEY=你的高德地图API密钥
```

免费申请地址：https://lbs.amap.com/dev/key/app

## 注意事项

- 坐标格式：`经度,纬度`（注意是经度在前，如 `116.481488,39.990464`）
- 城市编码可使用城市名或 ADCode（如 `110000` 代表北京）
- 骑行路线使用 v4 接口，与其他路线接口版本不同
- `citylimit` 参数接受 `true`/`false` 字符串
- AMap API 有日配额限制，免费版每日 5000 次调用
