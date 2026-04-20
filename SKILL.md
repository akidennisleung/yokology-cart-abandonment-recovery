---
name: yokology-cart-abandonment-recovery
description: Automate the daily YOKOLOGY cart abandonment recovery workflow. Cross-references GA4 User Explorer CSV with Shopline customer data to generate a WhatsApp broadcast list of high-intent non-purchasers, then tracks conversion effectiveness. Use when user says "執行日常未結帳挽回流程", provides a GA4 User Explorer CSV and requests a WhatsApp broadcast list, asks to run the cart abandonment recovery process, or requests to review broadcast effectiveness.
---

# YOKOLOGY Cart Abandonment Recovery

Daily workflow to identify high-intent website visitors who did not purchase, match them with Shopline customer records, produce a WhatsApp broadcast list, and measure conversion effectiveness.

## Prerequisites

1. **GA4 User Explorer CSV** — User provides a fresh export covering the last 3 days.
2. **Shopline customer report** (`.xls`) — Located at `/home/ubuntu/ga_data/shopline_latest.xls` or user-uploaded. Updated weekly (Monday).
3. **Send History** — CSV at `/home/ubuntu/ga_data/send_history.csv` (auto-created on first run).
4. **Unsubscribe list** (`.xlsx`) — Located at `/home/ubuntu/ga_data/unsubscribed.xlsx`. Contains phone numbers of customers who opted out. Updated when user provides a new version.

## Workflow Overview

The process has 8 sequential steps split into two phases:

**Phase A — Daily Broadcast (Steps 1-6)**
1. Parse GA4 CSV
2. Classify intent tiers & match Shopline
3. Check today's Shopline orders (browser)
4. Remove same-day purchasers, finalize & present
5. Deliver output files
6. Update Send History Log

**Phase B — Effectiveness Review (Steps 7-8)**
7. Extract recent orders from Shopline & cross-reference
8. Present effectiveness report with actionable insights

Phase B runs at the **start** of each daily session, BEFORE Phase A. This ensures yesterday's results inform today's messaging decisions.

**Recommended daily sequence:**
> Step 7-8 (review yesterday) → Step 1-6 (execute today)

## Step 1: Parse GA4 CSV

```bash
python scripts/parse_ga4_csv.py <user_provided_ga4.csv> /home/ubuntu/ga_data/parsed_ga4.csv
```

**CRITICAL**: GA4 Exploration CSV has a column-shift bug. The script handles this automatically. See `references/ga4_csv_column_map.md` for details.

## Step 2: Classify & Match

```bash
python scripts/classify_and_match.py \
  /home/ubuntu/ga_data/parsed_ga4.csv \
  /home/ubuntu/ga_data/shopline_latest.xls \
  /home/ubuntu/ga_data/send_history.csv \
  <DDMon> \
  /home/ubuntu
```

Where `<DDMon>` is today's date (e.g. `15Apr`). See `references/tier_criteria.md` for tier thresholds.

The script automatically applies the following exclusions in order:
1. **10-day cooldown** — Removes recipients sent within the last 10 days
2. **Unsubscribe list** — Removes customers who opted out (from `/home/ubuntu/ga_data/unsubscribed.xlsx`)
3. **Phone deduplication** — Keeps first occurrence only

**New Member Alert**: If GA4 User IDs cannot be found in Shopline, the script prints a warning with the unknown User IDs. For each unknown ID, automatically look up the customer profile in Shopline and record their details (see Step 2b below).

## Step 2b: New Member Lookup (if applicable)

If Step 2 reports any unknown GA4 User IDs (new members not yet in Shopline report), automatically look up each one:

1. Navigate to `https://admin.shoplineapp.com/admin/ysrecipes/users/{user_id}` for each unknown ID
2. Extract and record the following fields from the page:
   - **姓名** (Full name)
   - **電郵** (Email)
   - **手機號碼** (Phone — 8-digit HK number)
   - **加入日期** (Join date)
   - **會員級別** (Member tier, e.g. 一般會員)
   - **訂單數量** (Order count — check if any orders exist)
3. Present a summary table to the user:

```
## ⚠️ 新會員資料（未在 Shopline 報表中）
| 姓名 | 電郵 | 電話 | 加入日期 | 會員等級 | 訂單 |
|:---|:---|:---|:---|:---|:---:|
| Fiona Chow | fionachow528@yahoo.com | 97145353 | 2026-04-13 | 一般會員 | 0 |
```

4. If the new member has a valid HK phone number AND has **no existing orders**, add them to the broadcast list manually with `Tier B` intent (they visited the site but are not yet in the weekly Shopline export).
5. If they already placed an order, skip them.

**Note**: The Shopline weekly export lags by up to 7 days for newly registered members. This step bridges that gap.

## Step 3: Same-Day Order Exclusion (CRITICAL)

**Browser required.** See `references/shopline_order_check.md` for full procedure.

1. Navigate to `https://admin.shoplineapp.com/admin/ysrecipes/orders?createdBy=admin`
2. Extract names/emails of all customers who placed orders **today**
3. Cross-reference against the broadcast list from Step 2
4. Remove any matches — log removed names

**NEVER skip this step.**

## Step 4: Finalize & Present

Present the execution summary to the user:

```
## 執行摘要 — [Date]
| 步驟 | 結果 |
|:---|:---|
| GA4 數據範圍 | [date range] |
| GA4 有效用戶 | X 位 |
| 高意向未結帳 (Tier A) | X 位 |
| 高意向未結帳 (Tier B) | X 位 |
| 一般意向未結帳 (Tier C) | X 位 |
| 排除：今天已下單 | -X 位 |
| 排除：10天冷卻期內 | -X 位 |
| 排除：取消訂閱 | -X 位 |
| **最終廣播名單** | **X 位** |
```

Wait for user confirmation before delivering files.

## Step 5: Deliver Output Files

Two XLSX files:

**File 1: Internal Review (內部查閱版)**
`YOKOLOGY_WhatsApp_Broadcast_<DDMon>.xlsx`

**File 2: Direct Upload (直接上傳版)**
`YOKOLOGY_WhatsApp_Upload_<DDMon>.xlsx`

## Step 6: Update Send History

```bash
python scripts/generate_send_history_xlsx.py \
  /home/ubuntu/ga_data/send_history.csv \
  /home/ubuntu/YOKOLOGY_Send_History_Log.xlsx
```

## Step 7: Extract Orders & Cross-Reference (Effectiveness Analysis)

This step measures how many previous broadcast recipients subsequently placed orders. See `references/effectiveness_analysis.md` for full methodology.

### 7a. Extract Recent Orders from Shopline

Navigate to `https://admin.shoplineapp.com/admin/ysrecipes/orders?createdBy=admin` and extract all **paid, non-cancelled** orders from the last 3 days into a CSV:

```csv
order_date,customer_name,email,amount
2026-04-14,Rita Kwong,ritakwongsl@yahoo.com.hk,2272.36
```

Save to `/home/ubuntu/ga_data/orders_recent.csv`. Exclude test/internal orders (customer3, Experts Y's Recipes).

### 7b. Run Analysis Script

```bash
python scripts/analyze_effectiveness.py \
  /home/ubuntu/ga_data/send_history.csv \
  /home/ubuntu/ga_data/orders_recent.csv \
  <DDMon> \
  /home/ubuntu
```

The script automatically:
- Matches send records to orders within 3-day attribution window
- Calculates per-batch and overall conversion rates
- Breaks down by tier and customer value
- Generates formatted XLSX report with 3 sheets (摘要/轉換明細/未轉換名單)

## Step 8: Present Effectiveness Report

Present the report to the user in this format:

```
## 成效回顧 — [Date]
| 廣播批次 | 發送人數 | 轉換人數 | 轉換率 | 帶來收益 |
|:---|:---:|:---:|:---:|:---|
| [batch] | X | X | X% | HK$X,XXX |
| **合計** | **X** | **X** | **X%** | **HK$X,XXX** |

### 轉換明細
[List each converted customer with name, batch, order date, amount, tier]

### 分析解讀
[Provide 3-5 actionable insights based on the data]

### 建議調整
[Suggest specific changes to messaging, timing, or tier thresholds]
```

**Actionable insights should address:**
1. Which tiers convert best → adjust thresholds or messaging priority
2. Which customer value segments respond → tailor message content
3. Conversion timing (same-day vs +1/+2 days) → optimize send time
4. Revenue concentration → identify high-value recovery opportunities
5. Non-converter patterns → suggest follow-up strategies

Attach the XLSX report file.

## Key Rules

- **Output format**: Always XLSX, never CSV for user-facing files.
- **Cooldown**: 10 days. Same phone number cannot appear in consecutive lists within 10 days.
- **Shopline report**: Updated weekly (Monday). If stale, remind user.
- **GA4 data window**: Always the most recent 3 days.
- **Attribution window**: 3 days for effectiveness measurement.
- **Phone format**: HK 8-digit numbers only. Country code 852 for WhatsApp upload.
- **Daily sequence**: Always review yesterday's results BEFORE executing today's broadcast.
- **Unsubscribe list**: Permanently exclude opted-out phone numbers. File at `/home/ubuntu/ga_data/unsubscribed.xlsx`. When user provides a new version, overwrite the file. Format: column A = country code (852), column B = phone number (8 digits).
