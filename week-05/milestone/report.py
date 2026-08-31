"""The program. All the printing lives here. No requests import.

    build_rows(client, user, products_by_id, orders)
        one dict per order: product, quantity, price, line_total

    summarise(client)     per-user summaries, biggest spender first
    render(summaries)     the whole report as a SINGLE STRING
    main()                prints it, or prints a clear failure

See README.md for the exact output format.
"""
