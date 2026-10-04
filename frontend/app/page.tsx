"use client";

import { useEffect, useState } from "react";
import { Bungee, Rubik } from "next/font/google";

const display = Bungee({ subsets: ["latin"], weight: "400" });
const body = Rubik({ subsets: ["latin"] });

/* ---------------- types ---------------- */

interface Plan {
  travel_details?: {
    origin?: string; destination?: string; days?: number; travelers?: number;
    budget?: number | null; preferences?: string | string[];
  };
  flight_options?: { airline?: string; departure_airport?: string; arrival_airport?: string; total_price?: number | null }[];
  hotel_options?: { name?: string; location?: string; rating?: number | null; price_per_night?: number | null }[];
  activity_options?: { name?: string; location?: string; rating?: number | null; price_per_person?: number | null; currency?: string }[];
  budget_analysis?: {
    flight_cost?: number | null; hotel_cost?: number | null; activity_cost?: number | null;
    total_cost?: number | null; budget_status?: string; reasoning?: string;
  };
  itinerary?: { days?: { day: number; morning: string; afternoon: string; evening: string }[] };
}

type Theme = "dark" | "light";

const STEPS = ["Coordinator", "Flights", "Hotels", "Activities", "Budget", "Itinerary"];
const EXAMPLES = [
  "5 days from Chennai to Singapore for 2 people, ₹80,000 budget, 15–19 Oct 2026. Sightseeing and food.",
  "Long weekend in Goa for 4 friends, ₹60,000 total, beaches and nightlife.",
  "7 days in Tokyo from Chennai, solo, ₹1,50,000, anime, food and temples.",
];

const inr = (n?: number | null) => (n == null ? "—" : `₹${n.toLocaleString("en-IN")}`);

/* ---------------- theme tokens ---------------- */

const css = `
.theme-dark{--bg:#0F172A;--panel:#1E293B;--line:#334155;--text:#F8FAFC;--mute:#94A3B8;--brand:#0F766E;--brandhover:#115E59;--brandtext:#10B981;--accent:#10B981;--ok:#4ADE80;--warn:#F59E0B;--err:#F87171}
.theme-light{--bg:#F8FAFC;--panel:#FFFFFF;--line:#E2E8F0;--text:#0F172A;--mute:#64748B;--brand:#0F766E;--brandhover:#115E59;--brandtext:#0F766E;--accent:#10B981;--ok:#16A34A;--warn:#D97706;--err:#DC2626}
.t-root{background:var(--bg);color:var(--text);transition:background .25s,color .25s}
.panel{background:var(--panel);border:1px solid var(--line)}
.mute{color:var(--mute)} .brand{color:var(--brandtext)} .accent{color:var(--accent)}
.ok{color:var(--ok)} .warn{color:var(--warn)} .err{color:var(--err)}
.bg-brand{background:var(--brand);color:#fff}
.btn:hover:not(:disabled){background:var(--brandhover)}
.bg-accent{background:var(--accent)}
.rule{border-color:var(--line)} .rule-brand{border-color:var(--accent)} .rule-err{border-color:var(--err)}
.field{background:var(--panel);border:1px solid var(--line);color:var(--text)}
.field:focus{outline:2px solid var(--accent);outline-offset:1px}
.btn:focus-visible,.chip:focus-visible,.sw:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.pulse{animation:pulse 1.1s ease-in-out infinite}
@keyframes pulse{50%{opacity:.25}}
.theme-dark{--edge:#10B981;--shade:#0F766E}
.theme-light{--edge:#0F172A;--shade:#10B981}
.t-root{isolation:isolate;background-image:linear-gradient(color-mix(in srgb,var(--line) 55%,transparent) 1px,transparent 1px),linear-gradient(90deg,color-mix(in srgb,var(--line) 55%,transparent) 1px,transparent 1px);background-size:44px 44px;background-attachment:fixed}
.panel{border:2px solid var(--edge);box-shadow:6px 6px 0 var(--shade)}
.panel:not(.sw):not(.chip){border-radius:0!important}
.sw.panel,.chip.panel{box-shadow:3px 3px 0 var(--shade)}
.field{border:2px solid var(--edge);border-radius:0!important;box-shadow:6px 6px 0 var(--shade)}
.btn{border:2px solid var(--edge);border-radius:0!important;box-shadow:4px 4px 0 var(--edge);transition:transform .08s,box-shadow .08s,background .15s}
.btn:active:not(:disabled){transform:translate(3px,3px);box-shadow:1px 1px 0 var(--edge)}
.hero-title{text-shadow:4px 4px 0 var(--brand)}
.sun{position:absolute;right:0;top:24px;width:200px;height:200px;border-radius:50%;z-index:-1;background:linear-gradient(var(--accent),var(--brand));-webkit-mask:repeating-linear-gradient(#000 0 13px,transparent 13px 17px);mask:repeating-linear-gradient(#000 0 13px,transparent 13px 17px)}
@media (max-width:640px){.sun{width:110px;height:110px;opacity:.5}}
.theme-dark.t-root::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:50;background:repeating-linear-gradient(0deg,rgba(0,0,0,.14) 0 1px,transparent 1px 3px)}
@media (prefers-reduced-motion:reduce){.pulse{animation:none}.t-root{transition:none}}
`;

/* ---------------- small pieces ---------------- */

function Heading({ children, count }: { children: React.ReactNode; count?: number }) {
  return (
    <div className="mb-5 flex items-center gap-3">
      <span className="bg-brand h-6 w-1.5" />
      <h2 className={`${display.className} text-xl sm:text-2xl`}>{children}</h2>
      {count !== undefined && <span className="mute text-sm">{count} found</span>}
    </div>
  );
}

function Fact({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div>
      <p className="mute text-sm">{label}</p>
      <p className="mt-0.5 text-lg font-semibold">{value}</p>
    </div>
  );
}

/* ---------------- page ---------------- */

export default function Home() {
  const [theme, setTheme] = useState<Theme>("dark");
  const [request, setRequest] = useState("");
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(0);
  const [result, setResult] = useState<Plan | null>(null);
  const [error, setError] = useState("");

  /* remember theme; fall back to the system setting */
  useEffect(() => {
    try {
      const saved = localStorage.getItem("theme") as Theme | null;
      setTheme(saved ?? (window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark"));
    } catch { }
  }, []);

  const toggleTheme = () => {
    const next: Theme = theme === "dark" ? "light" : "dark";
    setTheme(next);
    try { localStorage.setItem("theme", next); } catch { }
  };

  /* walk the agent board while the request is in flight */
  useEffect(() => {
    if (!loading) return;
    setStep(0);
    const id = setInterval(() => setStep((s) => Math.min(s + 1, STEPS.length - 1)), 2200);
    return () => clearInterval(id);
  }, [loading]);

  const createPlan = async () => {
    if (!request.trim()) {
      setError("Describe your trip first: where, how many days, who's going and your budget.");
      return;
    }
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await fetch("http://localhost:8000/plan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ request }),
      });
      if (!res.ok) throw new Error(`Server responded with ${res.status}`);
      setResult(await res.json());
    } catch (e) {
      console.error(e);
      setError("Couldn't create the plan. Check that the backend is running on localhost:8000, then try again.");
    } finally {
      setLoading(false);
    }
  };

  const td = result?.travel_details;
  const ba = result?.budget_analysis;
  const prefs = Array.isArray(td?.preferences) ? td?.preferences.join(", ") : td?.preferences;

  const parts = [
    { label: "Flights", value: ba?.flight_cost ?? 0, shade: 1 },
    { label: "Hotels", value: ba?.hotel_cost ?? 0, shade: 0.7 },
    { label: "Activities", value: ba?.activity_cost ?? 0, shade: 0.4 },
  ];
  const total = ba?.total_cost ?? parts.reduce((a, p) => a + p.value, 0);
  const scale = Math.max(total, td?.budget ?? 0, 1);
  const over = td?.budget != null && total > td.budget;

  return (
    <main className={`t-root ${body.className} theme-${theme} min-h-screen`}>
      <style>{css}</style>

      <div className="mx-auto max-w-5xl px-5 pb-24 pt-6">
        {/* top bar */}
        <header className="flex items-center justify-between">
          <div className="flex items-center gap-2 font-bold">
            <span className="bg-brand inline-flex h-7 w-7 items-center justify-center rounded-full text-sm">✈</span>
            Multi-Agent Travel Planner
          </div>
          <button
            role="switch"
            aria-checked={theme === "light"}
            aria-label="Switch between light and dark theme"
            onClick={toggleTheme}
            className="sw panel relative flex h-8 w-16 items-center rounded-full px-1.5 text-xs"
          >
            <span className="mute absolute left-2">☾</span>
            <span className="mute absolute right-2">☀</span>
            <span
              className="bg-brand absolute top-1 h-6 w-6 rounded-full transition-all"
              style={{ left: theme === "dark" ? 4 : 36 }}
            />
          </button>
        </header>

        {/* hero */}
        <section className="relative pb-10 pt-16 sm:pt-24">
          <div aria-hidden className="sun" />
          <h1 className={`${display.className} hero-title text-5xl leading-[1.05] sm:text-7xl`}>
            Where to next?
          </h1>
          <p className="mute mt-5 max-w-xl text-lg">
            Tell us about your trip in your own words. Six AI agents find flights, hotels and things to do, check
            your budget and build the itinerary.
          </p>

          <textarea
            value={request}
            onChange={(e) => setRequest(e.target.value)}
            onKeyDown={(e) => { if ((e.metaKey || e.ctrlKey) && e.key === "Enter" && !loading) createPlan(); }}
            placeholder="Plan a 5-day trip from Chennai to Singapore for 2 people with a budget of ₹80,000. Travel dates are 15–19 October 2026. We like sightseeing and food."
            aria-label="Your travel request"
            className="field mt-8 min-h-36 w-full rounded-lg p-4 text-base"
          />

          <div className="mt-3 flex flex-wrap gap-2">
            {EXAMPLES.map((ex) => (
              <button key={ex} onClick={() => setRequest(ex)} className="chip panel mute max-w-xs truncate rounded-full px-3 py-1 text-sm hover:text-[var(--text)]">
                {ex}
              </button>
            ))}
          </div>

          <div className="mt-5 flex flex-wrap items-center gap-4">
            <button
              onClick={createPlan}
              disabled={loading}
              className="btn bg-brand rounded-lg px-7 py-3 text-base font-bold transition disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Planning…" : "Plan my trip"}
            </button>
            <span className="mute hidden text-sm sm:inline">or press Ctrl + Enter</span>
          </div>

          {error && (
            <p role="alert" className="rule-err err mt-5 border-l-4 py-2 pl-4 text-sm">
              {error}
            </p>
          )}
        </section>

        {/* agent board */}
        {loading && (
          <section aria-live="polite" className="panel rounded-lg p-6">
            <p className="font-semibold">Your agents are working</p>
            <ul className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {STEPS.map((s, i) => (
                <li key={s} className="flex items-center gap-3">
                  <span
                    className={`h-3 w-3 rounded-full border-2 rule-brand ${i < step ? "bg-accent" : ""} ${i === step ? "bg-accent pulse" : ""}`}
                  />
                  <span className={i > step ? "mute" : ""}>
                    {s}
                    {i < step ? " · done" : i === step ? " · working" : ""}
                  </span>
                </li>
              ))}
            </ul>
          </section>
        )}

        {/* results */}
        {result && !loading && (
          <div className="space-y-14">
            {/* route summary */}
            <section className="panel rounded-lg p-6 sm:p-8">
              <div className="flex flex-wrap items-end gap-x-6 gap-y-2">
                <p className={`${display.className} text-3xl sm:text-5xl`}>{td?.origin ?? "—"}</p>
                <span className="accent pb-1 text-3xl sm:text-5xl">→</span>
                <p className={`${display.className} text-3xl sm:text-5xl`}>{td?.destination ?? "—"}</p>
              </div>
              <div className="rule mt-8 grid grid-cols-2 gap-6 border-t pt-6 sm:grid-cols-4">
                <Fact label="Days" value={td?.days ?? "—"} />
                <Fact label="Travelers" value={td?.travelers ?? "—"} />
                <Fact label="Budget" value={inr(td?.budget)} />
                <Fact label="Interests" value={prefs || "—"} />
              </div>
            </section>

            {/* flights as boarding passes */}
            <section>
              <Heading count={result.flight_options?.length ?? 0}>Flights</Heading>
              <div className="space-y-4">
                {(result.flight_options ?? []).map((f, i) => (
                  <article key={i} className="panel flex overflow-hidden rounded-lg">
                    <div className="flex-1 p-5">
                      <p className="mute text-sm">{f.airline ?? "Airline unavailable"}</p>
                      <p className="mt-1 text-2xl font-bold tracking-tight">
                        {f.departure_airport ?? "—"} <span className="accent">→</span> {f.arrival_airport ?? "—"}
                      </p>
                    </div>
                    <div className="rule flex min-w-32 flex-col items-end justify-center border-l-2 border-dashed p-5 text-right">
                      <p className="mute text-sm">Total</p>
                      <p className="text-xl font-bold">{inr(f.total_price)}</p>
                    </div>
                  </article>
                ))}
              </div>
            </section>

            {/* hotels */}
            <section>
              <Heading count={result.hotel_options?.length ?? 0}>Hotels</Heading>
              <div className="grid gap-4 md:grid-cols-2">
                {(result.hotel_options ?? []).map((h, i) => (
                  <article key={i} className="panel rounded-lg p-5">
                    <h3 className="text-lg font-bold">{h.name}</h3>
                    <p className="mute mt-1 text-sm">{h.location}</p>
                    <div className="rule mt-5 flex items-baseline justify-between border-t pt-4">
                      <p><span className="warn">★</span> {h.rating ?? "No rating"}</p>
                      <p className="font-bold">
                        {inr(h.price_per_night)} <span className="mute text-sm font-normal">per night</span>
                      </p>
                    </div>
                  </article>
                ))}
              </div>
            </section>

            {/* activities */}
            <section>
              <Heading count={result.activity_options?.length ?? 0}>Things to do</Heading>
              <div className="grid gap-4 md:grid-cols-2">
                {(result.activity_options ?? []).map((a, i) => (
                  <article key={i} className="panel rounded-lg p-5">
                    <h3 className="text-lg font-bold">{a.name}</h3>
                    <p className="mute mt-1 text-sm">{a.location}</p>
                    <div className="rule mt-5 flex items-baseline justify-between border-t pt-4">
                      <p><span className="warn">★</span> {a.rating ?? "No rating"}</p>
                      <p className={a.price_per_person == null ? "mute text-sm" : "font-bold"}>
                        {a.price_per_person == null
                          ? "Price unavailable"
                          : `${a.currency ?? ""} ${a.price_per_person} per person`}
                      </p>
                    </div>
                  </article>
                ))}
              </div>
            </section>

            {/* budget as a bar against the limit */}
            <section>
              <Heading>Budget</Heading>
              <div className="panel rounded-lg p-6 sm:p-8">
                <div className="flex flex-wrap items-baseline justify-between gap-2">
                  <p className="text-4xl font-extrabold tracking-tight">{ba?.total_cost == null && !total ? "Unavailable" : inr(total)}</p>
                  <p className={`font-semibold ${over ? "err" : "ok"}`}>{ba?.budget_status}</p>
                </div>

                <div className="relative mt-6">
                  <div className="rule flex h-5 overflow-hidden rounded-full border">
                    {parts.map((p) => (
                      <div
                        key={p.label}
                        title={`${p.label}: ${inr(p.value)}`}
                        className="bg-brand"
                        style={{ width: `${(p.value / scale) * 100}%`, opacity: p.shade }}
                      />
                    ))}
                  </div>
                  {td?.budget != null && (
                    <div
                      className="absolute -top-2 h-9 w-0.5"
                      style={{ left: `${(td.budget / scale) * 100}%`, background: "var(--text)" }}
                      aria-label={`Budget limit ${inr(td.budget)}`}
                    />
                  )}
                </div>
                {td?.budget != null && (
                  <p className="mute mt-3 text-sm">
                    The vertical line marks your budget of {inr(td.budget)}.
                  </p>
                )}

                <ul className="mt-6 grid gap-4 sm:grid-cols-3">
                  {parts.map((p) => (
                    <li key={p.label} className="flex items-center gap-3">
                      <span className="bg-brand h-3 w-3 rounded-full" style={{ opacity: p.shade }} />
                      <span className="mute text-sm">{p.label}</span>
                      <span className="ml-auto font-semibold">{inr(p.value)}</span>
                    </li>
                  ))}
                </ul>

                {ba?.reasoning && <p className="mute rule mt-6 max-w-2xl border-t pt-5 leading-relaxed">{ba.reasoning}</p>}
              </div>
            </section>

            {/* itinerary as a route line */}
            <section>
              <Heading>Itinerary</Heading>
              <ol className="rule-brand ml-3 space-y-8 border-l-2">
                {(result.itinerary?.days ?? []).map((d) => (
                  <li key={d.day} className="relative pl-8">
                    <span className="bg-brand absolute -left-[11px] top-1 flex h-5 w-5 items-center justify-center rounded-full text-[10px] font-bold">
                      {d.day}
                    </span>
                    <h3 className="text-xl font-bold">Day {d.day}</h3>
                    <dl className="panel mt-3 divide-y rounded-lg" style={{ borderColor: "var(--line)" }}>
                      {([["Morning", d.morning], ["Afternoon", d.afternoon], ["Evening", d.evening]] as const).map(([k, v]) => (
                        <div key={k} className="rule grid gap-1 p-4 sm:grid-cols-[110px_1fr] sm:gap-4">
                          <dt className="brand font-semibold">{k}</dt>
                          <dd className="leading-relaxed">{v}</dd>
                        </div>
                      ))}
                    </dl>
                  </li>
                ))}
              </ol>
            </section>
          </div>
        )}
      </div>
    </main>
  );
}