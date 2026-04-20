# Shopline Same-Day Order Check

Read this file when performing Step 4 (same-day order exclusion) of the workflow.

## Purpose

Prevent sending WhatsApp recovery messages to customers who already placed an order today. This is the most critical exclusion step — sending a "come back and buy" message to someone who just purchased causes brand damage.

## Procedure

1. Navigate to: `https://admin.shoplineapp.com/admin/ysrecipes/orders?createdBy=admin`
2. The default view shows today's orders. Verify the date filter shows today's date.
3. Extract all customer names and emails from the visible orders.
4. Scroll through all pages if there are multiple pages of orders.
5. Cross-reference extracted names/emails against the broadcast list.
6. Remove any matching customers from the broadcast list.
7. Log removed names in the execution summary.

## Important Notes

- Match by both name AND email to avoid false positives from common names.
- Check all order statuses (pending, paid, shipped) — any order today means exclusion.
- If Shopline is unreachable, STOP the workflow and notify the user. Do NOT send the list without this check.
