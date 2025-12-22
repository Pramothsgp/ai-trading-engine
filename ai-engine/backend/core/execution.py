def apply_costs_and_tax(
    gross_return: float,
    transaction_cost: float,
    tax: float,
) -> float:
    """
    Applies transaction cost and tax to a single trade return.

    gross_return: e.g. 0.05 = +5%
    transaction_cost: e.g. 0.001 = 0.1% per trade
    tax: e.g. 0.15 = 15% on profits
    """

    # Deduct transaction cost
    net_return = gross_return - transaction_cost

    # Apply tax only if profitable
    if net_return > 0:
        net_return = net_return * (1 - tax)

    return net_return
