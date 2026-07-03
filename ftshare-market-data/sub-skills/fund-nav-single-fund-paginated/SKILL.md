---
name: fund-nav-single-fund-paginated
description: Get paginated NAV history for a specific fund. Use when user asks about 基金净值, 单位净值, 累计净值, 日增长率, 基金净值历史.
---

# 查询指定基金的净值历史（分页）

## 参数

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `--institution-code` | string | 是 | 6 位数字基金代码 | `000001` |
| `--page` | int | 否 | 页码，从 1 开始（默认 1） | `1` |
| `--page-size` | int | 否 | 每页记录数（默认 50） | `50` |

## 用法

通过主目录 `run.py` 调用（必填 `--institution-code`，可选 `--page`、`--page-size`）：

```bash
python <RUN_PY> fund-nav-single-fund-paginated --institution-code 000001 --page 1 --page-size 50
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出带分页信息的 JSON，每项含日期（`end_date` YYYYMMDD）、单位净值（`unitnv`）、累计净值（`accum_unitnv`）、日增长率（`unitnv_grw`，%）、申购/赎回状态等字段，以表格展示。

## 注意

- `unitnv_grw`、`annurtn_7d` 单位为 %
- 需要全量历史时，循环请求直到 `page > total_pages`
- 若用户只给基金名称，建议先用 `fund-support-symbols-all-funds-paginated` 或 `fund-overview-all-funds-paginated` 查到对应 6 位 `institution-code` 再查询净值。
