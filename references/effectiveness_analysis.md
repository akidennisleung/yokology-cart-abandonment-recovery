# Effectiveness Analysis Reference

Read this file when performing Step 7 (effectiveness analysis) of the workflow.

## Purpose

Close the feedback loop by measuring how many WhatsApp broadcast recipients subsequently placed orders. This enables data-driven decisions on message timing, content strategy, and tier targeting.

## Orders CSV Preparation

Before running the analysis script, extract recent orders from Shopline into a CSV file.

### Browser Extraction Method

1. Navigate to `https://admin.shoplineapp.com/admin/ysrecipes/orders?createdBy=admin`
2. Scroll through all orders from the last 3 days
3. Record each **paid, non-cancelled** order into a CSV with this exact format:

```csv
order_date,customer_name,email,amount
2026-04-14,Rita Kwong,ritakwongsl@yahoo.com.hk,2272.36
2026-04-13,Rachel Tam,racheltam726@gmail.com,4099.00
```

**Rules:**
- `order_date` format: `YYYY-MM-DD`
- `amount` is numeric only (no `HK$`, no commas)
- Exclude cancelled orders (已取消) and test orders (customer3, Experts Y's Recipes)
- Combine multiple orders from the same customer on the same day into separate rows

Save to: `/home/ubuntu/ga_data/orders_recent.csv`

## Attribution Window

Default: **3 days**. A conversion is attributed to a broadcast if the customer places an order within 3 days of the send date.

| Send Date | Attribution Window |
|:---|:---|
| 12 Apr | 12-15 Apr |
| 13 Apr | 13-16 Apr |
| 14 Apr | 14-17 Apr |

## Matching Logic

1. **Primary match**: Email (case-insensitive)
2. **Fallback match**: Customer name (case-insensitive, exact)
3. If both match, email takes priority

## Key Metrics

| Metric | Formula | Benchmark |
|:---|:---|:---|
| Conversion Rate (CVR) | Converted / Sent x 100 | 5-15% is good for WhatsApp |
| Revenue per Send | Total Revenue / Total Sent | Higher = better targeting |
| Average Order Value | Total Revenue / Converted | Compare with store average |
| Tier A CVR vs Overall | Tier A CVR / Overall CVR | Should be >1.5x |

## Interpreting Results

- **CVR > 10%**: Excellent — message content and timing are effective
- **CVR 5-10%**: Good — standard performance for recovery campaigns
- **CVR < 5%**: Review needed — check message content, timing, or tier thresholds
- **High Tier A CVR, Low Tier C CVR**: Expected — validates tier classification
- **VIP revenue dominance**: Normal — focus VIP messaging on retention, not discounts

## Actionable Recommendations Template

Based on results, suggest adjustments:

1. **If Tier A CVR is high**: Consider lowering Tier A threshold to capture more high-intent users
2. **If Tier C CVR is near zero**: Consider removing Tier C or raising its threshold
3. **If same-day conversions dominate**: Messages are effective but timing could be earlier
4. **If +2/+3 day conversions dominate**: Consider follow-up messages
5. **If VIP/重要客戶 convert well**: Strengthen VIP-specific messaging with exclusive offers
