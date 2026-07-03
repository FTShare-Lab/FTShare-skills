---
name: etf-pcf-download
description: 下载指定 PCF 文件（market.ft.tech）。用户问下载 PCF、PCF 文件内容、某只 ETF 申购赎回清单 XML 时使用。
---

# 下载指定 PCF 文件 - 下载指定 PCF 文件

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 下载指定 PCF 文件 |
| 外部接口 | `GET /api/v1/market/data/etf-pcf/etf-pcfs/{filename}` |
| 请求方式 | GET |
| 适用场景 | 根据 PCF 文件名下载对应 XML 文件内容，用于 ETF 申购赎回清单的详细数据 |

## 2. 请求参数

说明：`filename` 为路径参数（必填），通常由 PCF 列表接口 `etf-pcfs` 的 `items[].filename` 获得。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| filename | string | 是 | PCF 文件名（路径参数） | pcf_159003_20260309.xml | 由 PCF 列表接口的 items[].filename 获得 |

## 3. 响应说明

- **成功**：返回文件二进制流，`Content-Type: application/octet-stream`，`Content-Disposition: attachment; filename="{filename}"`。响应体为 PCF 的 XML 内容。
- **失败**：HTTP 非 2xx，响应体为错误信息。

## 4. 用法

通过主目录 `run.py` 调用（必填 `--filename`，可选 `--output` 保存到文件）：

```bash
# 输出到 stdout，可重定向到文件
python <RUN_PY> etf-pcf-download --filename pcf_159003_20260309.xml > pcf_159003_20260309.xml

# 保存到指定文件（仅允许当前工作目录下路径，防止路径穿越）
python <RUN_PY> etf-pcf-download --filename pcf_159003_20260309.xml --output pcf_159003_20260309.xml
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。未传 `--output` 时 XML 输出到 stdout；传 `--output` 时写入该文件。本接口无需额外请求头。

## 5. 请求示例

```
GET /api/v1/market/data/etf-pcf/etf-pcfs/pcf_159003_20260309.xml
```

## 6. 注意事项

- `filename` 须与列表接口返回的 `filename` 一致，且不得包含路径分隔符（如 `/`、`\`）
- 使用 `--output` 时仅可写入当前工作目录及其子目录，不可使用绝对路径或 `..` 穿越目录
- **自动化/端到端测试**：不要硬编码 `filename`。应**先**调用 `etf-pcfs --date YYYYMMDD`，从响应 `items[].filename` 取真实文件名（上交所/深交所前缀不同），**再**调用本 skill；否则易 404 或文件不存在。
