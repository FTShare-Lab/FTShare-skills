---
name: company-hk
description: 按港股交易代码查询公司介绍（market.ft.tech）。用户问港股公司简介、公司介绍、公司名称、成立日期、注册资本、法人代表、主营业务、员工人数、公司网址、企业类型、腾讯公司介绍、00700 公司信息时使用。参数 trade_code 须带后缀如 00700.HK。
---

# 查询港股公司介绍（company-hk）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询港股公司介绍 |
| 外部接口 | `/api/v1/market/data/hk/company-hk` |
| 请求方式 | GET |
| 适用场景 | 按港股交易代码查询该公司介绍，含公司名称、成立日期、注册资本、法人代表、公司简介、主营业务等 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| trade_code | string | 是 | 港股交易代码 | 00700.HK | 带市场后缀，如 00700.HK |

## 3. 响应说明

返回值为港股公司介绍对象（`CompanyHkResponse`），主要字段如下：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| security_name | String | 证券简称 |
| trade_code | String | 交易代码 |
| company_name | String | 公司名称 |
| company_name_en | String | 公司英文名称 |
| reg_date | int | 成立日期，YYYYMMDD 整数（如 `19991123`），东八区 |
| business_status | String | 经营状态 |
| reg_money | String | 注册资本（元） |
| currencyid | int | 币种 ID |
| currency | String | 币种 |
| legal | String | 法人代表 |
| reg_address | String | 注册地址 |
| office_address | String | 办公地址 |
| company_prof | String | 公司简介 |
| business_main | String | 主营业务 |
| staff_num | int | 员工人数 |
| website | String | 公司网址 |
| phone | String | 公司电话 |
| fax | String | 公司传真 |
| enterprise_type | String | 企业类型 |

## 4. 调用方式

本 handler 与上级 `FTShare-hk-data/run.py` 配合使用：

```bash
python <RUN_PY> company-hk --trade_code 00700.HK
```

其中 `<RUN_PY>` 为 `FTShare-hk-data/run.py` 的绝对路径。

### 直接执行 handler（调试）

```bash
python scripts/handler.py --trade_code 00700.HK
```

（需在 `sub-skills/company-hk` 目录下执行，或传入脚本完整路径。）

## 5. 请求示例

```
GET /api/v1/market/data/hk/company-hk?trade_code=00700.HK
```
