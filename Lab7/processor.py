import math


def lookup_drink_code(code_string):
    """
    Looks up the base price for a 3-letter drink code prefix.
    Safely handles None, non-string, malformed, or missing codes.
    Returns float price if valid; None if invalid or not found.
    """
    if code_string is None or not isinstance(code_string, str):
        return None

    cleaned = code_string.strip()
    if len(cleaned) < 3:
        return None

    code_prefix = cleaned.upper()[:3]
    menu_prices = {
        "LAT": 4.50,
        "CAP": 4.00,
        "ESP": 3.00,
        "AME": 3.50,
        "MOC": 5.00
    }
    return menu_prices.get(code_prefix, None)


def calculate_average_shot_cost(pricing_csv):
    """
    Calculates average espresso shot cost from comma-separated string.
    Safely handles None, non-string, empty string, malformed entries,
    negative prices, non-finite values, and zero division.
    Returns non-negative float average; 0.0 if no valid prices found.
    """
    if pricing_csv is None or not isinstance(pricing_csv, str):
        return 0.0

    tokens = pricing_csv.split(',')
    prices = []
    for token in tokens:
        cleaned = token.strip()
        if not cleaned:
            continue
        try:
            val = float(cleaned)
            if not math.isnan(val) and not math.isinf(val) and val >= 0:
                prices.append(val)
        except (ValueError, OverflowError):
            continue

    if not prices:
        return 0.0

    return round(sum(prices) / len(prices), 2)


def parse_order_modifiers(order_spec):
    """
    Parses semicolon-delimited key:value pairs into a modifier dictionary.
    Safely handles None, non-string, empty strings, missing colons,
    extra colons, and malformed whitespace.
    Returns dictionary of parsed modifiers; empty dict if none valid.
    """
    modifier_dict = {}
    if order_spec is None or not isinstance(order_spec, str):
        return modifier_dict

    items = order_spec.split(';')
    for item in items:
        cleaned = item.strip()
        if not cleaned or ':' not in cleaned:
            continue
        parts = cleaned.split(':', 1)
        key = parts[0].strip()
        value = parts[1].strip()
        if key:
            modifier_dict[key] = value

    return modifier_dict


def main():
    print("==== Running lookup_drink_code ====")
    drink_input = input("Enter drink code prefix (e.g. LAT, CAP, ESP): ")
    price = lookup_drink_code(drink_input)
    if price is not None:
        print("Base Price: $", price)
    else:
        print("Base Price: $ None (Invalid Code)")

    print("\n==== Running calculate_average_shot_cost ====")
    shots_input = input("Enter CSV of shot prices (e.g. 1.0, 1.5, 2.0): ")
    avg_price = calculate_average_shot_cost(shots_input)
    print("Average Shot Price: $", avg_price)

    print("\n==== Running parse_order_modifiers ====")
    spec_input = input("Enter modifiers (e.g. milk:oat;syrup:vanilla): ")
    mods = parse_order_modifiers(spec_input)
    print("Parsed Modifiers:", mods)


if __name__ == "__main__":
    main()
