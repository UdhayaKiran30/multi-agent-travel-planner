# ✈️ Odyssey - Multi-Agent AI Travel Planner

An **Agentic AI travel planning platform** that converts a natural-language travel request into a complete, personalized itinerary using multiple specialized AI agents, real-time travel APIs, budget analysis, and LangGraph-based orchestration.

The system automatically extracts trip requirements, searches for flights, hotels, and activities, evaluates options against the user's budget, and generates a day-by-day itinerary.

## 🚀 Live Demo

**Frontend:** https://multi-agent-travel-planner-ten.vercel.app

**Backend API:** https://multi-agent-travel-planner-****.onrender.com (deployed in render)

> The first request may take longer because the backend is hosted on a free-tier service and may need to wake up.

---

## 🎯 Key Features

* 🧠 **Multi-Agent AI Architecture**
* 🔄 **LangGraph workflow orchestration**
* 💬 Natural-language travel requests
* ✈️ Real-time flight search
* 🏨 Real-time hotel search
* 📍 Real-time attraction and activity discovery
* 💰 Budget-aware option selection
* 💱 Live currency conversion
* 🗓️ AI-generated day-by-day itinerary
* 🌗 Dark / Light theme
* 📄 Export travel plans as PDF
* ⚡ FastAPI backend
* 🎨 Next.js frontend
* ☁️ Production deployment with Vercel + Render

---

# 🏗️ Architecture

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │  Next.js Client │
                  │    (Vercel)     │
                  └────────┬────────┘
                           │ HTTPS
                           ▼
                  ┌─────────────────┐
                  │  FastAPI API    │
                  │    (Render)     │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │    LangGraph    │
                  │  Orchestrator   │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Coordinator     │
                  │     Agent       │
                  └────────┬────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
      ┌────────────┐ ┌────────────┐ ┌────────────┐
      │   Flight   │ │   Hotel    │ │  Activity  │
      │   Agent    │ │   Agent    │ │   Agent    │
      └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
            │              │              │
            ▼              ▼              ▼
        Google          Google         Google
        Flights         Hotels          Maps
        via SerpApi     via SerpApi     via SerpApi
            │              │              │
            └──────────────┼──────────────┘
                           ▼
                  ┌─────────────────┐
                  │  Budget Agent   │
                  └────────┬────────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
              Currency API   Cost Analysis
                    │             │
                    └──────┬──────┘
                           ▼
                  ┌─────────────────┐
                  │ Itinerary Agent │
                  └────────┬────────┘
                           ▼
                    FINAL TRAVEL PLAN
```

---

# 🤖 AI Agents

## 1. Coordinator Agent

The Coordinator Agent converts the user's natural-language request into structured travel requirements.

It extracts:

* Origin city
* Origin airport
* Destination city
* Destination airport
* Number of days
* Number of travelers
* Budget
* Travel preferences
* Departure date
* Return date

Example:

```text
"Plan a 5-day trip from Chennai to Singapore
for 2 people with a budget of ₹80,000."
```

is converted into structured state such as:

```text
Origin: Chennai
Airport: MAA
Destination: Singapore
Airport: SIN
Days: 5
Travelers: 2
Budget: ₹80,000
```

---

## 2. Flight Agent

The Flight Agent searches for real flight options using **SerpApi Google Flights**.

It retrieves information such as:

* Airline
* Departure airport
* Arrival airport
* Flight timing
* Return flight
* Total price
* Number of travelers

The agent does not invent flight information.

---

## 3. Hotel Agent

The Hotel Agent retrieves real accommodation options using **SerpApi Google Hotels**.

Hotel information includes:

* Hotel name
* Location
* Rating
* Reviews
* Price per night
* Total price
* Amenities
* Coordinates
* Booking/source link

---

## 4. Activity Agent

The Activity Agent searches for real attractions and activities using **Google Maps through SerpApi**.

Examples:

* Tourist attractions
* Parks
* Museums
* Observation decks
* Nature attractions
* Entertainment venues

The system also attempts to retrieve admission prices for selected activities.

---

## 5. Activity Pricing Agent

A specialized pricing component searches the web for current admission/ticket information.

It:

1. Searches for the activity.
2. Retrieves relevant search results.
3. Uses Gemini to identify a reliable adult admission price.
4. Preserves the original currency.
5. Returns `null` when reliable pricing cannot be determined.

This prevents the system from inventing activity prices.

---

## 6. Budget Agent

The Budget Agent evaluates the available travel options against the user's budget.

It selects:

* One flight
* One hotel
* Up to three activities

The agent considers:

* User budget
* Number of travelers
* Travel preferences
* Flight cost
* Hotel cost
* Activity costs

Currency conversion is performed programmatically using a live exchange-rate API.

The final cost is calculated by Python rather than relying on the LLM for financial arithmetic.

---

## 7. Itinerary Agent

The final agent generates a practical day-by-day itinerary using the options selected by the Budget Agent.

Each day contains:

```text
Morning
Afternoon
Evening
```

The itinerary uses the selected flight, hotel, and activities rather than inventing additional attractions.

---

# 🔄 LangGraph Workflow

The project uses **LangGraph** to orchestrate the agents through a shared state.

```text
START
  │
  ▼
Coordinator
  │
  ├──────────────┬──────────────┐
  ▼              ▼              ▼
Flight          Hotel        Activity
Agent           Agent          Agent
  │              │              │
  └──────────────┼──────────────┘
                 ▼
             Budget
               Agent
                 │
                 ▼
           Itinerary Agent
                 │
                 ▼
                END
```

The agents communicate through a shared `TravelState`.

---

# 🧠 Shared State

The LangGraph state contains information such as:

```python
TravelState:
    user_request
    origin
    origin_airport
    destination
    destination_airport
    days
    travelers
    budget
    preferences
    departure_date
    return_date
    flight_options
    hotel_options
    activity_options
    budget_analysis
    itinerary
```

This allows information produced by one agent to be consumed by downstream agents.

---

# 🛠️ Technology Stack

## Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS
* Next.js Fonts
* Browser Print API for PDF export

## Backend

* Python
* FastAPI
* Pydantic
* Requests

## AI / Agentic AI

* Google Gemini
* LangChain
* LangGraph
* Structured LLM outputs
* Tool calling
* Multi-agent orchestration

## External APIs

* SerpApi Google Flights
* SerpApi Google Hotels
* SerpApi Google Maps
* SerpApi Google Search
* Frankfurter Exchange Rate API

## Deployment

* GitHub
* Vercel
* Render

---

# 📁 Project Structure

```text
multi-agent-travel-planner/
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   └── globals.css
│   ├── public/
│   ├── package.json
│   └── tsconfig.json
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── coordinator.py
│   │   │   ├── flight_agent.py
│   │   │   ├── hotel_agent.py
│   │   │   ├── activity_agent.py
│   │   │   ├── activity_price_agent.py
│   │   │   ├── budget_agent.py
│   │   │   └── itinerary_agent.py
│   │   │
│   │   ├── graph/
│   │   │   ├── state.py
│   │   │   └── travel_graph.py
│   │   │
│   │   ├── tools/
│   │   │   ├── flight_tools.py
│   │   │   ├── hotel_tools.py
│   │   │   ├── activity_tools.py
│   │   │   ├── activity_price_tools.py
│   │   │   └── currency_tools.py
│   │   │
│   │   ├── config.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── test_full_graph.py
│
└── README.md
```

---

# ⚙️ Local Setup

## Prerequisites

Install:

* Python 3.10+
* Node.js 18+
* npm
* Git

---

## 1. Clone the repository

```bash
git clone https://github.com/UdhayaKiran30/multi-agent-travel-planner.git

cd multi-agent-travel-planner
```

---

# 🐍 Backend Setup

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create:

```text
backend/.env
```

Add:

```env
GOOGLE_API_KEY=your_gemini_api_key
SERPAPI_KEY=your_serpapi_api_key
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend will run at:

```text
http://localhost:8000
```

Health check:

```text
http://localhost:8000/health
```

---

# 💻 Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open:

```text
http://localhost:3000
```

---

# 🔐 Environment Variables

Never commit API keys to GitHub.

Backend `.env`:

```env
GOOGLE_API_KEY=your_gemini_api_key
SERPAPI_KEY=your_serpapi_api_key
```

The repository's `.gitignore` excludes:

```text
.env
venv/
node_modules/
.next/
```

---

# 📡 API

## Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

## Generate Travel Plan

```http
POST /plan
```

Request:

```json
{
  "request": "Plan a 5-day trip from Chennai to Singapore for 2 people with a budget of ₹80,000. Travel dates are 15–19 October 2026. We like sightseeing and food."
}
```

The API returns:

```text
travel_details
flight_options
hotel_options
activity_options
budget_analysis
itinerary
```

---

# 🌐 Production Architecture

The application is deployed using separate frontend and backend services.

```text
                    INTERNET
                       │
                       ▼
        ┌──────────────────────────┐
        │       Vercel             │
        │    Next.js Frontend      │
        └────────────┬─────────────┘
                     │ HTTPS
                     ▼
        ┌──────────────────────────┐
        │        Render            │
        │ FastAPI + LangGraph      │
        └────────────┬─────────────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Gemini     SerpApi   Frankfurter
```

---

# 🧪 Example Request

```text
Plan a 5-day trip from Chennai to Singapore
for 2 people with a budget of ₹80,000.

Travel dates:
15 October 2026 to 19 October 2026.

Preferences:
sightseeing and food.
```

The system:

```text
1. Extracts travel requirements
2. Searches real flights
3. Searches real hotels
4. Finds attractions
5. Retrieves available activity prices
6. Converts currencies
7. Selects budget-friendly options
8. Calculates available costs
9. Generates a day-by-day itinerary
```

---

# 🛡️ Error Handling

The system includes fault-tolerant behavior for external API failures.

Examples include:

* API request timeouts
* Failed activity price searches
* Missing activity prices
* Currency conversion failures
* Invalid agent-selected indices
* Missing travel information

When reliable activity pricing is unavailable, the system does not invent a price.

---

# 📈 Future Improvements

* Faster parallel API execution
* Caching of repeated searches
* Streaming agent progress to the frontend
* User authentication
* Persistent trip history
* PostgreSQL integration
* More travel providers
* Better activity price verification
* Hotel booking integration
* Flight booking integration
* Advanced preference matching
* Observability and agent tracing

---

# 👨‍💻 Author

**Udhaya Kiran M V**

Computer Science Engineering Graduate | Software Engineer | AI Engineer

* GitHub: https://github.com/UdhayaKiran30
* LinkedIn: https://www.linkedin.com/in/udhayakiran/

---

## ⭐ Project Highlights

This project demonstrates practical experience with:

**Agentic AI • Multi-Agent Systems • LangGraph • Gemini • Tool Calling • FastAPI • Next.js • TypeScript • Python • REST APIs • Real-Time Data • Budget Optimization • API Integration • Vercel • Render • GitHub**
