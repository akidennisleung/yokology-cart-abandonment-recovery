# Intent Tier Classification Criteria

Read this file when adjusting tier thresholds or understanding the classification logic.

## Tier Definitions

| Tier | Label | Criteria | Behavior Profile |
|:---|:---|:---|:---|
| **A** | 極高優先 | `event_count >= 40` AND `key_events > 0` AND `purchase_revenue == 0` | Deep browsing + conversion actions (e.g. add-to-cart) but abandoned |
| **B** | 高優先 | `event_count >= 20` AND `purchase_revenue == 0` | Sustained browsing interest, no conversion actions |
| **C** | 一般優先 | `event_count >= 5` AND `purchase_revenue == 0` | Basic browsing activity |

All tiers require: `purchase_revenue == 0` AND `transactions == 0`.

## Customer Value Classification

Based on Shopline `累積金額` (cumulative spending):

| Value Label | Threshold |
|:---|:---|
| VIP客戶 | >= HK$100,000 |
| 重要客戶 | >= HK$50,000 |
| 活躍客戶 | >= HK$10,000 |
| 一般客戶 | > HK$0 |
| 潛在新客 | HK$0 |

## Suggested WhatsApp Message Types

| Customer Value | Message Strategy |
|:---|:---|
| VIP客戶 / 重要客戶 | VIP關懷問候 + 專屬優惠 |
| 活躍客戶 | 新品推薦 + 回購優惠 |
| 一般客戶 | 產品推薦 + 滿額免運 |
| 潛在新客 | 品牌介紹 + 首購優惠碼 |
