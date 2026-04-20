# GA4 User Explorer CSV Column Mapping

Read this file when debugging GA4 CSV parsing issues or when the CSV format changes.

## The Column-Shift Problem

GA4 Exploration exports have a known structural issue: the User ID occupies the first unnamed column (treated as the DataFrame index by pandas), causing all subsequent column headers to shift left by one position.

## Correct Mapping

| Data Position | CSV Header (Wrong) | Actual Meaning | Data Type |
|:---|:---|:---|:---|
| Col 0 | *(unnamed/index)* | `user_id` | string (24-char hex for Shopline) |
| Col 1 | `Effective user ID` | `stream_name` | string (e.g. "https://www.ysrecipes.com.hk - GA4") |
| Col 2 | `Stream name` | `namespace_id` | string (e.g. "ENHANCED_USER_ID") |
| Col 3 | `Namespace ID` | `event_count` | integer |
| Col 4 | `Event count` | `sessions` | integer |
| Col 5 | `Sessions` | `avg_session_duration` | float (seconds) |
| Col 6 | `Average session duration` | `purchase_revenue` | float (HK$) |
| Col 7 | `Purchase revenue` | `transactions` | integer |
| Col 8 | `Transactions` | `active_users` | integer |
| Col 9 | `Active users` | `key_events` | integer |

## Parsing Notes

- Skip rows starting with `#` (GA4 comment lines at top of file).
- Skip the first non-comment row (original header).
- Use `csv.reader` for reliable parsing (avoids pandas index issues).
- Valid Shopline IDs: exactly 24 lowercase hex characters (`^[0-9a-f]{24}$`).
- Filter `stream_name` to contain `ysrecipes` to exclude other properties.
