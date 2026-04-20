# YOKOLOGY 購物車棄單回收自動化系統

針對 YOKOLOGY 品牌的每日 WhatsApp 廣播流程，自動從 GA4 行為數據中識別高意向未結帳用戶，比對 Shopline 客戶資料庫，生成 WhatsApp 名單並追蹤轉換成效。

---

## 功能概覽

- **解析 GA4 CSV**：自動修正 GA4 User Explorer 匯出時的欄位偏移 bug
- **分層分類**：依行為事件數與購買信號，將用戶分為 Tier A / B / C
- **Shopline 比對**：與客戶資料庫交叉比對，篩出可聯繫的名單
- **多重排除規則**：10 天冷卻期 / 退訂名單 / 電話號碼去重
- **WhatsApp 名單生成**：輸出內部審查版與平台上傳版兩份 XLSX
- **成效分析**：3 天歸因窗口，自動計算 CVR、營業額、各層級轉換率

---

## 目錄結構

```
yokology-cart-abandonment-recovery/
├── SKILL.md                          # 完整操作流程指引（8 步驟）
├── scripts/
│   ├── parse_ga4_csv.py              # 解析並修正 GA4 CSV 欄位偏移
│   ├── classify_and_match.py         # 分層分類、比對、生成廣播名單
│   ├── analyze_effectiveness.py      # 成效分析報告
│   └── generate_send_history_xlsx.py # 發送記錄匯出為 XLSX
└── references/
    ├── tier_criteria.md              # 意向層級與客戶價值分類標準
    ├── ga4_csv_column_map.md         # GA4 CSV 欄位偏移說明
    ├── shopline_order_check.md       # 當日訂單排除操作步驟
    └── effectiveness_analysis.md    # 成效分析方法論
```

---

## 安裝

```bash
pip install pandas openpyxl
```

---

## 每日執行流程

### Phase A — 生成廣播名單

**Step 1：解析 GA4 CSV**

```bash
python scripts/parse_ga4_csv.py <ga4_匯出檔案.csv> /home/ubuntu/ga_data/parsed_ga4.csv
```

**Step 2：分層分類與比對**

```bash
python scripts/classify_and_match.py \
  /home/ubuntu/ga_data/parsed_ga4.csv \
  /home/ubuntu/ga_data/shopline_latest.xls \
  /home/ubuntu/ga_data/send_history.csv \
  15Apr \
  /home/ubuntu
```

> 日期格式：`DDMon`，例如 `15Apr`

**Step 3（手動）**：登入 Shopline 後台，確認當日已有訂單的客戶，並從名單中移除。

**Step 4：生成發送記錄 XLSX**

```bash
python scripts/generate_send_history_xlsx.py \
  /home/ubuntu/ga_data/send_history.csv \
  /home/ubuntu/YOKOLOGY_Send_History_Log.xlsx
```

---

### Phase B — 成效分析（建議在每日 Phase A 前執行）

**Step 1（手動）**：從 Shopline 匯出最近訂單，儲存至 `/home/ubuntu/ga_data/orders_recent.csv`

**Step 2：執行成效分析**

```bash
python scripts/analyze_effectiveness.py \
  /home/ubuntu/ga_data/send_history.csv \
  /home/ubuntu/ga_data/orders_recent.csv \
  15Apr \
  /home/ubuntu
```

---

## 輸出檔案

| 檔案 | 說明 |
|------|------|
| `YOKOLOGY_WhatsApp_Broadcast_[DDMon].xlsx` | 內部審查用，含完整客戶資料與訊息類型建議 |
| `YOKOLOGY_WhatsApp_Upload_[DDMon].xlsx` | WhatsApp 平台上傳用（852 + 8 位電話） |
| `YOKOLOGY_Effectiveness_Report_[DDMon].xlsx` | 成效報告（摘要 / 轉換明細 / 未轉換名單） |
| `YOKOLOGY_Send_History_Log.xlsx` | 發送記錄總表與冷卻狀態 |
| `send_history.csv` | 每日自動追加的廣播記錄（供排重使用） |

---

## 分層標準

| 層級 | 條件 | 優先級 |
|------|------|--------|
| Tier A | `event_count ≥ 40` 且 `key_events > 0` | 極高 |
| Tier B | `event_count ≥ 20` | 高 |
| Tier C | `event_count ≥ 5` | 一般 |

## 客戶價值分類

| 等級 | 累計消費 | 建議訊息方向 |
|------|----------|------------|
| VIP 客戶 | ≥ HK$100,000 | VIP 關懷 + 獨家優惠 |
| 重要客戶 | ≥ HK$50,000 | VIP 關懷 + 獨家優惠 |
| 活躍客戶 | ≥ HK$10,000 | 新品 + 忠誠折扣 |
| 一般客戶 | > HK$0 | 產品推薦 |
| 潛在新客 | HK$0 | 品牌介紹 + 首購優惠碼 |

---

## 必備資料檔案

| 路徑 | 說明 | 更新頻率 |
|------|------|----------|
| `/home/ubuntu/ga_data/shopline_latest.xls` | Shopline 客戶資料庫 | 每週一更新 |
| `/home/ubuntu/ga_data/send_history.csv` | 廣播發送記錄 | 每日自動追加 |
| `/home/ubuntu/ga_data/unsubscribed.xlsx` | 退訂名單（A欄：852，B欄：8位電話） | 按需更新 |

---

## 重要規則

- **10 天冷卻期**：同一電話在 10 天內不重複發送
- **3 天歸因窗口**：廣播後 3 天內完成的訂單計入轉換
- **僅限香港號碼**：8 位數字、WhatsApp 上傳需加國碼 852
- **同日購買排除**：需手動確認 Shopline 當日訂單後再發送

---

## 完整操作文件

詳見 [SKILL.md](./SKILL.md)，包含完整 8 步驟流程、輸出規格與注意事項。
