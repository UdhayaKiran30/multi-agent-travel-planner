from typing import Optional

from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GOOGLE_API_KEY
from app.tools.activity_price_tools import search_activity_price


class ActivityPrice(BaseModel):
    price_per_person: Optional[float] = Field(
        description=(
            "Ticket price per person. "
            "Return null if no reliable price is found."
        )
    )

    currency: Optional[str] = Field(
        description=(
            "Currency code such as SGD, USD, INR. "
            "Return null if unavailable."
        )
    )

    source_text: Optional[str] = Field(
        description=(
            "Short text from the search results "
            "supporting the selected price."
        )
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.0,
)

structured_llm = llm.with_structured_output(ActivityPrice)


def get_activity_price(
    activity_name: str,
    destination: str,
) -> ActivityPrice:

    search_results = search_activity_price.invoke({
        "activity_name": activity_name,
        "destination": destination,
    })

    if not search_results:
        return ActivityPrice(
            price_per_person=None,
            currency=None,
            source_text=None,
        )

    prompt = f"""
You are an Activity Pricing Agent.

Activity:
{activity_name}

Destination:
{destination}

Google Search results:
{search_results}

Your task is to identify a reliable admission/ticket
price for ONE adult/person.

Rules:
1. Prefer official or clearly stated admission prices.
2. Prefer prices specifically for this activity.
3. Ignore hotel prices and unrelated prices.
4. Do not invent a price.
5. If multiple prices exist, choose the clearest
   standard adult admission price.
6. Return null if no reliable admission price exists.
7. Preserve the original currency.
"""

    try:
        return structured_llm.invoke(prompt)

    except Exception as e:
        print(
            f"[WARNING] Gemini price extraction failed "
            f"for {activity_name}: {e}"
        )

        return ActivityPrice(
            price_per_person=None,
            currency=None,
            source_text=None,
        )
