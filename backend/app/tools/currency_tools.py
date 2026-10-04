from typing import Optional
import requests

from langchain_core.tools import tool


@tool
def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str = "INR",
) -> Optional[float]:
    """
    Convert an amount from one currency to another
    using a live exchange-rate API.
    """

    url = "https://api.frankfurter.app/latest"

    params = {
        "amount": amount,
        "from": from_currency,
        "to": to_currency,
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        rates = data.get("rates", {})

        return rates.get(to_currency)

    except Exception as e:
        print(
            f"[WARNING] Currency conversion failed: {e}"
        )
        return None