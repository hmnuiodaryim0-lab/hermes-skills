#!/usr/bin/env python3
"""
AMap (高德地图) Web Service API CLI
Converted from kaichen/amap-skill (TypeScript/Bun) to Python/curl for Hermes Agent.

Usage:
  python amap.py <command> [flags]

Commands:
  geocode            地理编码（地址 → 坐标）
  reverse-geocode    逆地理编码（坐标 → 地址）
  ip-location        IP 定位
  weather            天气查询
  bike-route-coords  骑行路径规划（坐标）
  bike-route-address 骑行路径规划（地址）
  walk-route-coords  步行路径规划（坐标）
  walk-route-address 步行路径规划（地址）
  drive-route-coords 驾车路径规划（坐标）
  drive-route-address 驾车路径规划（地址）
  transit-route-coords 公交路径规划（坐标）
  transit-route-address 公交路径规划（地址）
  distance           距离测量
  poi-text           POI 关键字搜索
  poi-around         POI 附近搜索
  poi-detail         POI 详情查询

Environment:
  AMAP_MAPS_API_KEY  高德地图 Web Service API Key（必填）
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error
from typing import Optional

# ── Constants ────────────────────────────────────────────────────────────────

AMAP_API_BASE_URL = "https://restapi.amap.com"
DEFAULT_TIMEOUT_SEC = 15
DEFAULT_RETRIES = 2

EXIT_OK = 0
EXIT_PARAM = 2
EXIT_NETWORK = 3
EXIT_API = 4
EXIT_INTERNAL = 5

# ── API Endpoints ─────────────────────────────────────────────────────────────

ENDPOINTS = {
    "reverse-geocode":  ("/v3/geocode/regeo",      "v3"),
    "geocode":          ("/v3/geocode/geo",         "v3"),
    "ip-location":      ("/v3/ip",                  "v3"),
    "weather":          ("/v3/weather/weatherInfo", "v3"),
    "bike-route-coords":("/v4/direction/bicycling", "v4"),
    "walk-route-coords":("/v3/direction/walking",   "v3"),
    "drive-route-coords":("/v3/direction/driving",  "v3"),
    "transit-route-coords": ("/v3/direction/transit/integrated", "v3"),
    "distance":         ("/v3/distance",            "v3"),
    "poi-text":         ("/v3/place/text",           "v3"),
    "poi-around":       ("/v3/place/around",         "v3"),
    "poi-detail":       ("/v3/place/detail",         "v3"),
}

# ── API Key ──────────────────────────────────────────────────────────────────

def get_api_key() -> str:
    key = os.environ.get("AMAP_MAPS_API_KEY", "").strip()
    if not key:
        sys.stderr.write("Error: AMAP_MAPS_API_KEY environment variable is not set.\n")
        sys.exit(EXIT_PARAM)
    return key

# ── HTTP Helpers ──────────────────────────────────────────────────────────────

def build_url(path: str, params: dict) -> str:
    qs = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    return f"{AMAP_API_BASE_URL}{path}?{qs}"

def is_success(command: str, data: dict) -> bool:
    _, strategy = ENDPOINTS[command]
    if strategy == "v3":
        return data.get("status") == "1"
    else:  # v4
        return data.get("errcode") == 0 or data.get("errcode") == "0"

def get_error_text(data: dict) -> str:
    for field in ("info", "errmsg", "infocode"):
        if isinstance(data.get(field), str) and data[field]:
            return data[field]
    errcode = data.get("errcode")
    if errcode is not None and errcode != 0:
        return str(errcode)
    return "Unknown API error"

def http_get(url: str, retries: int = DEFAULT_RETRIES) -> dict:
    last_err = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT_SEC) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if attempt < retries and e.code >= 500 or e.code == 429:
                import time; time.sleep(0.2 * (2 ** attempt))
                continue
            sys.stderr.write(f"HTTP Error {e.code}: {e.reason}\n")
            sys.exit(EXIT_NETWORK)
        except urllib.error.URLError as e:
            last_err = e
            if attempt < retries:
                import time; time.sleep(0.2 * (2 ** attempt))
                continue
            sys.stderr.write(f"Network error: {e.reason}\n")
            sys.exit(EXIT_NETWORK)
        except json.JSONDecodeError as e:
            sys.stderr.write(f"JSON parse error: {e}\n")
            sys.exit(EXIT_NETWORK)
    sys.stderr.write(f"Network request failed after {retries + 1} attempts: {last_err}\n")
    sys.exit(EXIT_NETWORK)

# ── Direct API Commands ───────────────────────────────────────────────────────

def cmd_geocode(address: str, city: Optional[str] = None) -> dict:
    url = build_url("/v3/geocode/geo", {"key": API_KEY, "address": address, "city": city})
    data = http_get(url)
    if not is_success("geocode", data):
        sys.stderr.write(f"AMap API error: {get_error_text(data)}\n")
        sys.exit(EXIT_API)
    return data

def cmd_reverse_geocode(location: str) -> dict:
    url = build_url("/v3/geocode/regeo", {"key": API_KEY, "location": location})
    data = http_get(url)
    if not is_success("reverse-geocode", data):
        sys.stderr.write(f"AMap API error: {get_error_text(data)}\n")
        sys.exit(EXIT_API)
    return data

def cmd_ip_location(ip: str) -> dict:
    url = build_url("/v3/ip", {"key": API_KEY, "ip": ip})
    data = http_get(url)
    if not is_success("ip-location", data):
        sys.stderr.write(f"AMap API error: {get_error_text(data)}\n")
        sys.exit(EXIT_API)
    return data

def cmd_weather(city: str, extensions: Optional[str] = None) -> dict:
    url = build_url("/v3/weather/weatherInfo", {"key": API_KEY, "city": city, "extensions": extensions or "base"})
    data = http_get(url)
    if not is_success("weather", data):
        sys.stderr.write(f"AMap API error: {get_error_text(data)}\n")
        sys.exit(EXIT_API)
    return data

def cmd_bike_route_coords(origin: str, destination: str) -> dict:
    url = build_url("/v4/direction/bicycling", {"key": API_KEY, "origin": origin, "destination": destination})
    data = http_get(url)
    if not is_success("bike-route-coords", data):
        sys.stderr.write(f"AMap API error: {get_error_text(data)}\n")
        sys.exit(EXIT_API)
    return data

def cmd_walk_route_coords(origin: str, destination: str) -> dict:
    url = build_url("/v3/direction/walking", {"key": API_KEY, "origin": origin, "destination": destination})
    data = http_get(url)
    if not is_success("walk-route-coords", data):
        sys.stderr.write(f"AMap API error: {get_error_text(data)}\n")
        sys.exit(EXIT_API)
    return data

def cmd_drive_route_coords(origin: str, destination: str) -> dict:
    url = build_url("/v3/direction/driving", {"key": API_KEY, "origin": origin, "destination": destination})
    data = http_get(url)
    if not is_success("drive-route-coords", data):
        sys.stderr.write(f"AMap API error: {get_error_text(data)}\n")
        sys.exit(EXIT_API)
    return data

def cmd_transit_route_coords(origin: str, destination: str, city: str, cityd: str) -> dict:
    url = build_url("/v3/direction/transit/integrated", {
        "key": API_KEY, "origin": origin, "destination": destination, "city": city, "cityd": cityd
    })
    data = http_get(url)
    if not is_success("transit-route-coords", data):
        sys.stderr.write(f"AMap API error: {get_error_text(data)}\n")
        sys.exit(EXIT_API)
    return data

def cmd_distance(origins: str, destination: str, dtype: Optional[str] = None) -> dict:
    url = build_url("/v3/distance", {"key": API_KEY, "origins": origins, "destination": destination, "type": dtype or "1"})
    data = http_get(url)
    if not is_success("distance", data):
        sys.stderr.write(f"AMap API error: {get_error_text(data)}\n")
        sys.exit(EXIT_API)
    return data

def cmd_poi_text(keywords: str, city: Optional[str] = None, citylimit: Optional[str] = None) -> dict:
    url = build_url("/v3/place/text", {
        "key": API_KEY, "keywords": keywords, "city": city, "citylimit": citylimit
    })
    data = http_get(url)
    if not is_success("poi-text", data):
        sys.stderr.write(f"AMap API error: {get_error_text(data)}\n")
        sys.exit(EXIT_API)
    return data

def cmd_poi_around(location: str, radius: Optional[str] = None, keywords: Optional[str] = None) -> dict:
    url = build_url("/v3/place/around", {
        "key": API_KEY, "location": location, "radius": radius, "keywords": keywords
    })
    data = http_get(url)
    if not is_success("poi-around", data):
        sys.stderr.write(f"AMap API error: {get_error_text(data)}\n")
        sys.exit(EXIT_API)
    return data

def cmd_poi_detail(id: str) -> dict:
    url = build_url("/v3/place/detail", {"key": API_KEY, "id": id})
    data = http_get(url)
    if not is_success("poi-detail", data):
        sys.stderr.write(f"AMap API error: {get_error_text(data)}\n")
        sys.exit(EXIT_API)
    return data

# ── Address-based Route Commands (geocode first, then route) ─────────────────

def geocode_address(address: str, city: Optional[str] = None) -> str:
    data = cmd_geocode(address, city)
    geocodes = data.get("geocodes", [])
    if not geocodes or not geocodes[0].get("location"):
        sys.stderr.write(f"Geocode returned no location for: {address}\n")
        sys.exit(EXIT_API)
    return geocodes[0]["location"]

def cmd_bike_route_address(origin_address: str, destination_address: str,
                             origin_city: Optional[str] = None, destination_city: Optional[str] = None) -> dict:
    origin = geocode_address(origin_address, origin_city)
    destination = geocode_address(destination_address, destination_city)
    return cmd_bike_route_coords(origin, destination)

def cmd_walk_route_address(origin_address: str, destination_address: str,
                             origin_city: Optional[str] = None, destination_city: Optional[str] = None) -> dict:
    origin = geocode_address(origin_address, origin_city)
    destination = geocode_address(destination_address, destination_city)
    return cmd_walk_route_coords(origin, destination)

def cmd_drive_route_address(origin_address: str, destination_address: str,
                              origin_city: Optional[str] = None, destination_city: Optional[str] = None) -> dict:
    origin = geocode_address(origin_address, origin_city)
    destination = geocode_address(destination_address, destination_city)
    return cmd_drive_route_coords(origin, destination)

def cmd_transit_route_address(origin_address: str, destination_address: str,
                                 origin_city: str, destination_city: str) -> dict:
    origin = geocode_address(origin_address, origin_city)
    destination = geocode_address(destination_address, destination_city)
    return cmd_transit_route_coords(origin, destination, origin_city, destination_city)

# ── CLI Parser ────────────────────────────────────────────────────────────────

COMMANDS = {
    "geocode":              (["--address", "--city"],                                       cmd_geocode),
    "reverse-geocode":       (["--location"],                                                cmd_reverse_geocode),
    "ip-location":          (["--ip"],                                                       cmd_ip_location),
    "weather":              (["--city", "--extensions"],                                    cmd_weather),
    "bike-route-coords":    (["--origin", "--destination"],                                 cmd_bike_route_coords),
    "bike-route-address":   (["--origin-address", "--destination-address",
                               "--origin-city", "--destination-city"],                       cmd_bike_route_address),
    "walk-route-coords":    (["--origin", "--destination"],                                  cmd_walk_route_coords),
    "walk-route-address":   (["--origin-address", "--destination-address",
                               "--origin-city", "--destination-city"],                      cmd_walk_route_address),
    "drive-route-coords":   (["--origin", "--destination"],                                  cmd_drive_route_coords),
    "drive-route-address":  (["--origin-address", "--destination-address",
                               "--origin-city", "--destination-city"],                      cmd_drive_route_address),
    "transit-route-coords": (["--origin", "--destination", "--city", "--cityd"],           cmd_transit_route_coords),
    "transit-route-address":(["--origin-address", "--destination-address",
                               "--origin-city", "--destination-city"],                     cmd_transit_route_address),
    "distance":             (["--origins", "--destination", "--type"],                     cmd_distance),
    "poi-text":             (["--keywords", "--city", "--citylimit"],                     cmd_poi_text),
    "poi-around":           (["--location", "--radius", "--keywords"],                    cmd_poi_around),
    "poi-detail":           (["--id"],                                                      cmd_poi_detail),
}

def build_parser():
    parser = argparse.ArgumentParser(description="AMap (高德地图) Web Service API CLI")
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    for cmd_name, (flags, _) in COMMANDS.items():
        p = sub.add_parser(cmd_name)
        for fl in flags:
            p.add_argument(fl)

    return parser

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    global API_KEY
    API_KEY = get_api_key()

    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(EXIT_OK)

    # Extract flags as dict (only those set)
    flags = {k.replace("-", "_"): v for k, v in vars(args).items()
             if k != "command" and v is not None}

    _, handler = COMMANDS[args.command]

    # Handle citylimit (accept string "true"/"false")
    if "citylimit" in flags:
        flags["citylimit"] = "true" if str(flags["citylimit"]).lower() in ("true", "1") else "false"

    result = handler(**flags)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
