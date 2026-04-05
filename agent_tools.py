from pricer import MultiAssetPricer

pricer = MultiAssetPricer()

def pricing_tool(input_text: str) -> str:
    try:
        parts = input_text.lower().split()

        if "bond" in parts:
            # format: price bond 1000 0.05 5
            face_value = float(parts[2])
            rate = float(parts[3])
            time = float(parts[4])

            price = pricer.price_bond(face_value, rate, time)
            return f"Bond Price = {price:.2f}"

        elif "option" in parts:
            # format: price option 100 100 1 0.05 0.2
            S = float(parts[2])
            K = float(parts[3])
            T = float(parts[4])
            r = float(parts[5])
            sigma = float(parts[6])

            price = pricer.price_option(S, K, T, r, sigma)
            return f"Option Price = {price:.2f}"

        elif "eln" in parts:
            # format: price eln 300 0.03 0.25
            S = float(parts[2])
            r = float(parts[3])
            sigma = float(parts[4])

            price = pricer.price_eln(S, r, sigma)
            return f"ELN Price = {price:.2f}"

        else:
            return "Invalid product type"

    except Exception as e:
        return f"Error: {str(e)}"