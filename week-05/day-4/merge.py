"""Answering questions no single endpoint answers.

    get_orders(base_url, user_id)       that user's raw order dicts
    enrich_orders(base_url, user_id)    one dict per order with:
                                        product, quantity, price, line_total
    user_summary(base_url, user_id)     name, city, order_count, total_spent
    ranked_customers(base_url)          a summary per user, highest spend first

enrich_orders must fetch the product list ONCE, not once per order.
Round money to 2dp.
"""
