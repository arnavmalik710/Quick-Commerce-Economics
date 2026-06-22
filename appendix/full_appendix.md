# Technical Appendix
## Profitability Thresholds in Indian Quick Commerce: Dark Store Unit Economics

---

## 1. Problem Statement

What is the exact mathematical tipping point required for a single dark store to achieve sustainable EBITDA profitability, and how does that differ between a representative Tier-1 and Tier-2 Indian city?

The quick-commerce sector in India has grown from $0.5B GMV in FY22 to $6.2B by FY25, with platforms like Blinkit, Zepto, and Swiggy Instamart collectively operating over 5,000 dark stores across 100+ cities. Despite this scale, most dark stores remain individually unprofitable, sustained by platform-level cross-subsidisation and venture capital. This project strips away the platform-level narrative to model profitability at the level of a single representative dark store, identifying the exact combination of order volume, product mix, and logistics efficiency required to flip a store from loss-making to EBITDA positive.

---

## 2. Methodology

### 2.1 Research approach

The project follows a bottom-up unit economics framework. Rather than analysing consolidated platform P&Ls, all modelling is conducted at the individual dark store level. This isolates the operational mechanics that determine whether a single store is viable, independent of platform-wide subsidies or marketing spend.

The analysis combines five elements:
1. Industry research and public disclosures
2. Unit economics modelling (Model 1)
3. Demand modelling (Model 2)
4. Sensitivity analysis (Model 3)
5. Tier-1 vs Tier-2 scenario comparison across all three models

All data was sourced from public filings, industry reports, and financial journalism. No primary data collection was conducted. Full citations are in Section 6.

### 2.2 Model 1 — Unit economics P&L waterfall

A store-level contribution margin model built bottom-up at the per-order level. The formula calculates what is left after all per-order costs are subtracted from per-order revenue.

**Key variables:**
- **AOV** — total revenue per order. The primary revenue driver. Varies significantly by SKU mix — a grocery-heavy store has a lower AOV than one selling electronics and beauty products.
- **Take rate** — the percentage of AOV the platform retains as commission, sourced from public filings.
- **Delivery fee** — flat fee charged to the customer per order, added to the revenue side.
- **Rider payout** — cost paid to the delivery rider per order. One of the largest per-order costs.
- **Picking and packing cost** — labour cost of the in-store picker assembling the order.
- **Rent allocation per order** — monthly dark store rent divided by total monthly orders. Converts a fixed cost into a per-order figure.
- **Inventory expiry provision** — a percentage of COGS written off due to unsold perishable stock. Higher for grocery-heavy stores.
- **Overhead allocation** — technology, warehouse management, and other fixed costs allocated per order. Explicitly included, not silently ignored.
- **SKU mix** — the proportion of high-margin (electronics, beauty) vs low-margin (grocery, FMCG) products. The central lever in the model, affecting both AOV and expiry provision simultaneously.

**Scenarios modelled:** grocery-only, current mix (74% grocery), mixed (50/50), non-grocery-led (20% grocery), across both Tier-1 and Tier-2 cost structures.

### 2.3 Model 2 — Demand modelling

Order arrivals are modelled using a Poisson distribution to approximate demand intensity across peak and off-peak windows. The Poisson distribution models the probability of a given number of orders arriving in a fixed time window, assuming orders arrive independently and randomly at a known average rate.

**Key variables:**
- **λ (lambda)** — average orders arriving per hour in a given time window. A separate λ is defined for each period of the day: early morning, morning rush, midday, evening rush, late night. Calibrated from daily order totals sourced from public data; the intraday shape is a documented modelling assumption (see Section 3.3).
- **k** — the actual number of orders arriving in a given hour. The distribution predicts the probability of exactly k orders arriving given λ.
- **s** — number of pickers on shift in a given time window. Compared against k to identify overstaffing or understaffing.
- **μ (mu)** — service rate: orders a single picker can handle per hour (12 orders/hr, sourced from IIMA). Total store capacity = s × μ.
- **Cost per idle staff hour** — when λ < s × μ, idle workers are a direct cost. Used to quantify idle-time waste across the day.

**Core comparison:** when λ > s × μ → capacity crash, delayed deliveries. When λ < s × μ → idle staff, margin drain.

### 2.4 Model 3 — Sensitivity analysis

Each key input variable from Model 1 is varied independently by ±20% from its base value while holding all others constant. The resulting change in contribution margin is recorded, ranked by impact magnitude, and visualised as a tornado chart.

**Variables tested:** AOV, take rate, delivery fee, rider payout, picking cost, monthly rent, orders per day, overhead, grocery share, expiry provision.

**Method:** each variable is moved ±20% from its base case. The resulting CM change is recorded. Variables are ranked by total swing (sum of upside and downside impact). A delivery time vs retention S-curve is separately modelled to identify the retention cliff — the delivery time threshold beyond which customer churn accelerates sharply.

---

## 3. Assumptions

### 3.1 General

- A single representative dark store is modelled, not a platform-wide P&L.
- Tier-1 refers to a metro city (representative of Delhi, Mumbai, Bengaluru). Tier-2 refers to a non-metro city.
- All figures are in INR unless stated otherwise.
- EBITDA is calculated as contribution margin less fixed operating expenses. The model captures contribution margin at the per-order level; full EBITDA requires subtracting additional fixed overheads not modelled here (central technology infrastructure, corporate marketing, SBC, D&A).
- Fixed costs are allocated at the dark-store level and do not vary with order volume except rent per order, which dilutes as volume grows.
- Public company filings, earnings calls, investor presentations, and industry reports are assumed to be reliable unless contradictory evidence is identified. Missing values are estimated using industry benchmarks with explicit documentation.

### 3.2 Demand assumptions

- Orders arrive randomly but at a known average rate, modelled via Poisson distribution.
- Two peak demand windows are assumed: morning rush (7–11am) and evening rush (6–10pm), consistent with qualitative industry descriptions.
- Demand patterns are consistent across weekdays. Weekends and festivals are not modelled in the base case.
- Orders are independent between successive arrivals (standard Poisson assumption).
- Order cancellations are ignored in the base model.

### 3.3 Operational assumptions

- Average delivery distance is assumed constant within each city tier (2 km Tier-1, 4 km Tier-2).
- Rent is stable month-on-month — no seasonal variation modelled.
- Picking staff count is fixed during a shift and does not flex intraday.
- Picker productivity (12 orders/hr) remains constant during normal operations.
- Rider availability is assumed stable — surge pricing, weather disruptions, and gig worker shortages are not modelled in the base case.
- Dark store capacity constraints are not reached unless explicitly modelled.

### 3.4 Financial assumptions

- Take rate, fulfillment cost, and delivery fee are held constant per scenario.
- Expiry/write-off provision is a fixed percentage of COGS.
- No platform-level cross-subsidisation is modelled.

### 3.5 Competition and retention assumptions

- The dark store operates in a stable competitive environment. Entry of a competing store within the delivery radius is not modelled.
- Market share is assumed constant across all scenarios.
- Repeat order frequency is held constant within each scenario. Customer churn is treated as stable unless varied explicitly in the sensitivity analysis.
- Retention impact of delivery time degradation is modelled in Model 3 only.

### 3.6 Weather and surcharge

- Base model assumes standard weather conditions.
- Rain and late-night surcharges on rider payouts are acknowledged but not modelled in the base case.

### 3.7 City-level parameter assumptions

| Parameter | Tier-1 | Tier-2 | Source |
|-----------|--------|--------|--------|
| Store size | ~4,000 sq ft | ~1,500 sq ft | Swiggy AR FY25, India Foundation |
| Monthly rent | ₹2,00,000 | ₹60,000 | RedSeer benchmarks |
| AOV (base) | ₹600 | ₹390 | Blended Blinkit/Instamart; Tier-2 = −35% (RedSeer) |
| Take rate | 18% of GOV | 16% of GOV | Derived from Blinkit 23.3% of NOV and Instamart 15.3% of GOV |
| Rider payout | ₹50/order | ₹55/order | Xylem PMS field data; Tier-2 higher due to longer radius |
| Delivery radius | 2 km | 4 km | India Foundation / IIMA |
| Mature orders/day | 1,300 | 800 | Blinkit implied ~1,450; Instamart peak ~1,260; Tier-2 scaled |
| Grocery share | 74% | 85% | Swiggy Corp Deck Nov 2025 (Tier-1); assumed higher in Tier-2 |
| Expiry provision | 3% of COGS | 5% of COGS | India Foundation (<5% QC wastage); higher in Tier-2 |
| Base staff (pickers) | 10 | 5 | Project charter; picker throughput 12 orders/hr (IIMA) |

### 3.8 Documented assumptions not directly sourced

The following parameters were estimated with explicit rationale and are flagged as low-confidence in the assumptions CSV:

- **Picking/packing cost (₹15/order):** Derived from picker monthly earnings (₹18,000) ÷ (26 days × 8 hrs × 12 orders/hr throughput), rounded up to include overhead.
- **Overhead allocation (₹20/order Tier-1, ₹25 Tier-2):** Approximated from Instamart's below-contribution costs of ~9.5% of GOV (Swiggy Nov 2025 deck), with marketing removed to isolate tech and support.
- **Delivery fee (₹25 Tier-1, ₹20 Tier-2):** Estimated from revenue decomposition; platforms charge ₹15–40 depending on basket size.
- **Intraday demand shape (Model 2):** The hourly distribution of orders is a modelled assumption. The daily total is sourced; the hourly split is not. Explicitly flagged in the model code.
- **Retention cliff curve (Model 3):** Modelled as a logistic S-curve with a cliff at ~15 minutes. No source provided a measured curve. Shape is consistent with qualitative evidence that platforms moved from 10-minute to 13–15 minute delivery promises as their sustainable standard.

---

## 4. Quantitative Analysis

### 4.1 Model 1 — Unit Economics P&L Waterfall

**Formula:**

```
CM = (AOV × Take Rate) + Delivery Fee
     − Rider Payout
     − Picking & Packing Cost
     − Rent Allocation per Order
     − Overhead Allocation
     − Expiry Provision
```

Where:
- Rent per order = Monthly rent ÷ (Orders/day × 30)
- Expiry provision = COGS × Expiry % where COGS = AOV × (1 − Blended margin)
- Blended margin = Grocery share × 12.5% + Non-grocery share × 42.5%

**Tier-1 base case walkthrough (at 1,300 orders/day):**

| Line item | Calculation | Value |
|-----------|-------------|-------|
| Revenue from take rate | ₹600 × 18% | +₹108.00 |
| Delivery fee | — | +₹25.00 |
| Rider payout | — | −₹50.00 |
| Picking & packing | — | −₹15.00 |
| Rent per order | ₹2,00,000 ÷ (1,300 × 30) | −₹5.13 |
| Overhead | — | −₹20.00 |
| Expiry provision | ₹409 COGS × 3% | −₹12.27 |
| **Contribution margin** | | **+₹30.60/order** |

**Key findings:**

Tier-1 crosses into positive contribution margin at approximately 210 orders/day. At mature volume (1,300 orders/day), CM reaches ~₹30/order. This is broadly consistent with Blinkit's reported contribution per order of ₹22.5 in FY25, with the gap reflecting the model's use of industry-average rather than Blinkit-specific cost assumptions.

Tier-2 does not reach positive contribution margin at any order volume within the modelled range (200–2,000 orders/day). CM remains between −₹39 and −₹30/order regardless of volume, because the primary costs (rider payout, picking, overhead) are fixed per-order and not diluted by volume — only rent dilutes with more orders, and rent is a small fraction of total cost.

**SKU mix scenarios (at fixed order volume):**

| Scenario | Tier-1 AOV | Tier-1 CM | Tier-2 AOV | Tier-2 CM |
|----------|-----------|-----------|-----------|-----------|
| Grocery-only (100% grocery) | ₹600 | +₹27.12 | ₹390 | −₹32.16 |
| Current mix (74% grocery) | ₹662 | +₹38.27 | ₹431 | −₹25.77 |
| Mixed (50/50) | ₹720 | +₹48.81 | ₹468 | −₹19.59 |
| Non-grocery-led (20% grocery) | ₹792 | +₹62.34 | ₹515 | −₹11.48 |

SKU mix is the most powerful lever in Tier-1 — shifting from grocery-only to non-grocery-led more than doubles CM per order (₹27 → ₹62). This is consistent with the real-world trend observed in Instamart's data, where non-grocery share of GOV grew from 9% (Q2FY25) to 26% (Q2FY26).

Tier-2 improves significantly with SKU shift but cannot reach breakeven. This confirms that Tier-2 viability requires structural cost reduction — particularly in rider payout and logistics — not just a better product mix.

**Output files:** `outputs/figures/model1_breakeven_chart.png`, `outputs/figures/model1_sku_mix_waterfall.png`, `outputs/tables/model1_cm_vs_orders.csv`, `outputs/tables/model1_sku_mix_scenarios.csv`

---

### 4.2 Model 2 — Poisson Demand Modeling

**Formula:**

```
P(X = k) = (λ^k × e^−λ) / k!
```

Where λ = average orders per hour in a given time window.

Crash probability per hour: `P(crash) = 1 − P(X ≤ capacity) = 1 − Poisson.CDF(capacity, λ)`

Staff capacity per hour: `capacity = staff count × picker throughput (12 orders/hr)`

**Intraday λ construction:**

The daily order total (1,300 for Tier-1, 800 for Tier-2) is distributed across 24 hours using a documented weight shape reflecting the morning rush (7–11am peak) and evening rush (6–10pm peak). Peak hour λ values:

| Time window | Tier-1 λ (orders/hr) | Tier-2 λ (orders/hr) |
|-------------|---------------------|---------------------|
| 8am (morning peak) | 111 | 68 |
| 7pm (evening peak) | 122 | 75 |
| 3am (trough) | 1 | 1 |

**Daily staffing results:**

| Metric | Tier-1 (10 staff, cap 120/hr) | Tier-2 (5 staff, cap 60/hr) |
|--------|------------------------------|----------------------------|
| Hours with crash risk >50% | 1 | 5 |
| Daily idle cost | ₹17,579 | ₹4,874 |
| Daily crash cost | ₹38 | ₹539 |
| Peak crash probability | 57% (7pm) | 96% (7pm) |

**Key findings:**

Tier-1 stores, sized at 10 pickers, operate comfortably within capacity for 23 of 24 hours. The dominant cost is idle capacity during off-peak hours (₹17,579/day), not crash-related delays.

Tier-2 stores, sized at 5 pickers, experience capacity crashes for 5 hours daily with peak crash probability reaching 96% at 7pm. The same lean fixed staff that is right-sized for average daily volume cannot absorb its own peak demand spikes.

This reinforces the finding from Model 1 from a different angle: Tier-2 is not just economically weaker, it is operationally less reliable. Both disadvantages compound each other — delivery delays during peak hours reduce retention, which reduces the ordering frequency that the economic model depends on.

**Output files:** `outputs/figures/model2_demand_vs_capacity.png`, `outputs/figures/model2_crash_probability.png`, `outputs/tables/model2_hourly_staffing.csv`, `outputs/tables/model2_daily_summary.csv`

---

### 4.3 Model 3 — Sensitivity Analysis

**Method:** Each of 10 input variables was varied by ±20% from its base value while holding all others fixed. The resulting change in CM per order was recorded and ranked by total swing magnitude.

**Tier-1 sensitivity ranking (±20% variation):**

| Rank | Variable | CM swing (+20%) | CM swing (−20%) | Total swing |
|------|----------|----------------|----------------|-------------|
| 1 | Platform take rate | +₹21.6 | −₹21.6 | ₹43.2 |
| 2 | Average Order Value | +₹19.4 | −₹19.4 | ₹38.8 |
| 3 | Rider payout | +₹10.0 | −₹10.0 | ₹20.0 |
| 4 | Delivery fee | +₹5.0 | −₹5.0 | ₹10.0 |
| 5 | Overhead per order | +₹4.0 | −₹4.0 | ₹8.0 |
| 6–10 | Picking cost, expiry, volume, rent, SKU mix | <₹5 each | <₹5 each | — |

**Tier-2 sensitivity ranking (key differences):**

In Tier-2, rider payout overtakes AOV as the second most impactful variable. The gap between top variables is also narrower — the system is more uniformly sensitive across all inputs, meaning no single lever dominates. This confirms that Tier-2 economics require structural cost reduction across multiple dimensions simultaneously, not optimisation of one variable.

**Key findings:**

Take rate is the single biggest lever for Tier-1 profitability. Blinkit's deliberate growth of take rate from 18.7% (FY23) to 23.3% (FY25) — driven by advertising and higher commission categories — is directly validated by this ranking. AOV is second, which explains why platforms are aggressively expanding into higher-ticket non-grocery categories. Rent and order volume, often cited as the key levers in popular analysis, rank near the bottom.

**Retention cliff:** The delivery time vs retention curve shows a sharp drop beginning around 15 minutes. Instamart's national average of 13 minutes sits just before this cliff. Tier-2 stores' estimated 20-minute average sits past it, at a point where the model indicates retention near collapse. This creates a compounding risk for Tier-2 operators: capacity crashes during peak hours (Model 2) directly cause delivery time breaches, which then damage the repeat order frequency that unit economics (Model 1) depend on.

**Output files:** `outputs/figures/model3_tornado_chart.png`, `outputs/figures/model3_retention_cliff.png`, `outputs/tables/model3_sensitivity.csv`, `outputs/tables/model3_retention_curve.csv`

---

## 5. Limitations

**Cost estimates for low-confidence parameters.** Four parameters — picking/packing cost, overhead per order, delivery fee, and packaging cost — could not be sourced directly and were derived from first principles. These are clearly marked as low-confidence in the assumptions CSV. The sensitivity analysis confirms that none of these are top-ranked variables, which limits their impact on the core findings.

**Intraday demand shape is modelled, not measured.** No public source provided hour-by-hour order data. The demand curve shape is a documented modelling choice calibrated to match qualitative descriptions of peak windows. The daily totals are sourced; the hourly distribution is not.

**Tier-2 analysis is structurally thinner.** Most public data (annual reports, industry reports) focuses on Tier-1 metro markets. Tier-2 parameters are largely derived by applying RedSeer's published differentials (−35% AOV, +25% logistics costs, 1.5–2× breakeven OPD) to the Tier-1 base. There is no Tier-2 equivalent of the Blinkit or Instamart operating metrics.

**The model captures contribution margin, not EBITDA.** Platform-level costs — central technology infrastructure, corporate marketing, SBC, D&A — are not modelled. The steady-state EBITDA target of 5–6% of NOV (stated by both Blinkit and Instamart management) is used as an external benchmark, not derived from this model.

**Competition and seasonality are held constant.** Real-world dark store economics are affected by competitor store openings, festival demand spikes, monsoon-related disruption, and rider supply shocks. These are acknowledged in the assumptions document but are outside the model's scope.

---

## 6. References

### Public filings

1. Eternal Limited (Zomato). *Annual Report FY2024-25.* https://b.zmtcdn.com/investor-relations/Eternal_Annual_Report_2024-25.pdf

2. Swiggy Limited. *Annual Report FY2024-25.* https://www.swiggy.com/corporate/wp-content/uploads/2025/07/Swiggy-Annual-Report-FY-2024-25.pdf

3. Swiggy Limited. *Corporate Deck FY2024-25.* https://www.swiggy.com/corporate/wp-content/uploads/2025/08/Corporate-Deck-FY24-25.pdf

4. Swiggy Limited. *Corporate Presentation November 2025.* https://www.swiggy.com/corporate/wp-content/uploads/2025/11/Swiggy-Corporate-Presentation_Nov-25.pdf

### Research reports

5. India Foundation. *The Promise of Quick Commerce for India's Economic and Social Development.* 2026. https://indiafoundation.in/wp-content/uploads/2026/04/ifn-5.pdf

6. Ranjekar, G. & Roy, D. *Rise of Quick Commerce in India: Business Models and Infrastructure Requirements.* IIM Ahmedabad, Centre for Transportation and Logistics. March 2023. https://www.iima.ac.in/sites/default/files/2023-06/Q-com%20-%20Ranjekar%20%26%20Roy_0.pdf

### Industry analysis

7. RedSeer Strategy Consultants. *Fast to Faster: Exploring India's Q-Commerce Boom.* https://redseer.com/articles/fast-to-faster-exploring-indias-q-commerce-boom/

8. RedSeer Strategy Consultants. *Scaling Quick Commerce Beyond Metros: A Strategic Reassessment.* https://redseer.com/articles/scaling-quick-commerce-beyond-metros-a-strategic-reassessment/

9. RedSeer Strategy Consultants. *Quick Commerce: India's Retail Darling or Profit Mirage?* https://redseer.com/articles/quick-commerce-indias-retail-darling-or-profit-mirage/

### Financial journalism

10. Xylem Investment Research. *The Economics of Quick Commerce in India.* https://www.xyleminvestment.com/post/the-economics-of-quick-commerce-in-india

11. Entrackr. *Eternal's Reality Check: Blinkit's Thin Margins and District's Losses.* https://entrackr.com/analysis/eternals-reality-check-blinkits-thin-margins-and-districts-losses-11777148

12. Medium — Anubhav Satpathy. *How Quick Commerce in India Can Pump Up Its Average Order Value.* https://medium.com/@anubhavsatpathy5/how-quick-commerce-in-india-can-pump-up-its-average-order-value-aov-51407a40dc92

### Video reference

13. YouTube. *Q-Commerce Economics Overview.* https://www.youtube.com/watch?v=F2jsNYPqaIg

### Google Drive (internal research compilation)

14. Research compilation (personal). https://drive.google.com/file/d/1zUiVcIYLxjM7Iqe6QAFeMijPp_RHQs2o/view