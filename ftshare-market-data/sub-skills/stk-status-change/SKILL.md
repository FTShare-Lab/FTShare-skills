---
name: stk-status-change
description: "查询 A 股状态变更记录。用户问股票上市日期、退市、暂停上市、终止上市、A股上市历史、状态变更、变更类型时使用。三个过滤参数均可选，可任意组合，亦可全部不填（可能返回较大响应体）。"
---

# 查询 A 股状态变更记录

## 接口说明

| 项目     | 说明                                            |
|----------|-------------------------------------------------|
| 接口名称 | 查询 A 股状态变更记录                            |
| 外部接口 | `/api/v1/market/data/stk-status-change`         |
| 请求方式 | GET                                             |
| 适用场景 | 查询 A 股的状态变更记录，如上市、退市、暂停上市等 |

## 请求参数

| 参数名       | 类型   | 是否必填 | 描述                                              | 取值示例     | 备注                                                                  |
|--------------|--------|----------|---------------------------------------------------|--------------|-----------------------------------------------------------------------|
| trade_code   | string | 否       | 股票代码                                          | 600848.SH    | 带 .SZ/.SH 后缀，支持逗号分隔多个；不填表示不按代码过滤                |
| change_date  | string | 否       | 变更日期，精确过滤                                | 19910703     | `YYYYMMDD` 格式                                                       |
| change_type  | string | 否       | 变更类型，精确过滤                                | 上市         | 常见值如 `上市`、`退市`、`暂停上市`                                    |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> stk-status-change --trade_code 600848.SH
python <RUN_PY> stk-status-change --trade_code 600848.SH --change_type 上市
python <RUN_PY> stk-status-change --change_date 19910703
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

```json
[
    {
        "trade_code": "000003.SZ",
        "name": "PT金田A",
        "change_date": "19910703",
        "change_type": "上市",
        "change_details": ""
    }
]
```

### 字段说明

| 字段名          | 类型   | 是否可为空 | 说明                                                |
|-----------------|--------|------------|-----------------------------------------------------|
| trade_code      | string | 否         | 股票代码（带 .SZ/.SH 后缀）                          |
| name            | string | 否         | 股票名称                                            |
| change_date     | string | 否         | 变更日期（`YYYYMMDD`）                              |
| change_type     | string | 否         | 变更类型（如上市、退市、暂停上市）                   |
| change_details  | string | 是         | 变更说明                                            |

## 注意事项

- 三个过滤参数均可选，可任意组合，亦可全部不填（可能返回较大响应体）。
- `trade_code` 未填时可能返回全表结果，调用方需注意响应大小。
- 排序：`trade_code` 升序、`change_date` 降序。
- 日期参数格式为 `YYYYMMDD`，非时间戳。
