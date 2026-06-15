# Data sources

## Primary sources — public filings
| # | Source | Year | URL | Metrics extracted | Used in |
|---|--------|------|-----|------------------|---------|

## Industry reports
| # | Source | Year | URL | Metrics extracted | Used in |
|---|--------|------|-----|------------------|---------|

## Financial journalism
| # | Source | Article | Date | URL | Metrics extracted | Used in |
|---|--------|---------|------|-----|------------------|---------|

## Assumptions log

| Parameter | Value used | Rationale | Confidence |
|-----------|-----------|-----------|------------|






# Data Sources & References

> Every number used in the model is traced to a row here. Last updated: Phase 1 complete.

---

## Primary Sources — Public Filings

| # | Source | Year | Key Metrics Extracted | Used In |
|---|--------|------|-----------------------|---------|
| 1 | Eternal (Zomato) Annual Report FY2024-25 | FY25 | Blinkit GOV (₹28,273Cr), NOV (₹22,371Cr), orders (424M), AOV (₹667), NAOV (₹528), take rate (23.3% of NOV), CM (4.3% of NOV), EBITDA (-1.3% of NOV), stores (1,301), NOV/day/store (₹766k), contribution per order (₹22.5), EBITDA loss/order (-₹6.9) | Model 1, 2 |
| 2 | Swiggy Annual Report FY2024-25 | FY25 | Instamart GOV (₹14,683Cr), orders (285.5M), AOV (₹514), CM (-4% of GOV), EBITDA (-14.3% of GOV), stores (1,021), store area (4.0M sq ft), avg store size (3,889 sq ft), standard store 3,500-4,500 sq ft / 20,000 SKUs, megapod 10,000-12,000 sq ft / 50,000 SKUs, delivery time ~12.5 min | Model 1, 2, 3 |
| 3 | Swiggy Corporate Presentation FY2024-25 | Nov 2025 | Quarterly orders/store/day (peak 1,260 in Q2FY25), take rate progression (14.8-15.7% of GOV), SKU mix shift (grocery 91%→74%, non-grocery 9%→26%), store capacity 2,000+ orders/day, GOV per user per month (₹1,955 in Q2FY26), variable costs % GOV (17.4% Q2FY26), below-contribution costs % GOV (9.5%), annualized GOV ₹28,000Cr | Model 1, 2, 3 |
| 4 | Eternal Q4 FY26 Shareholder Letter | Q4 FY26 | Blinkit stores (2,243), NOV (₹14,386Cr), EBITDA (₹37Cr, 0.3% of NOV), net AOV (₹525), MTU 27.2M, Delhi NCR steady state 5-6%, capex ₹1,700Cr FY26 | Model 1 |
| 5 | Eternal Q3 FY25 Shareholder Letter | Q3 FY25 | Consistent rider monthly earnings ₹27,726 excl. fuel | Model 1, 2 |

---

## Industry Reports

| # | Source | Year | Key Metrics Extracted | Used In |
|---|--------|------|-----------------------|---------|
| 1 | RedSeer — Tier-1 vs Tier-2 Profitability Drivers | 2024-25 | Tier-2 AOV 35% lower than Tier-1, Tier-2 logistics costs 25% higher, Tier-2 breakeven OPD 1.5-2x higher than Tier-1 | Model 1, 3 |
| 2 | RedSeer — Q-Commerce Beyond Metros | FY25 | Non-metro = 15-17% of QC GMV, metro top-8 = 83-85%, QC growing at ~150% YoY | Context |
| 3 | RedSeer — Q-Commerce India Ascent | FY25 | Market ₹0.53T (FY25), projected ₹4-6T (FY2030P), MTU grew >40% FY24, ordering frequency ~6/month FY24 | Model 2 |
| 4 | RedSeer — AOV Trap / Kirana Report | 2026 | Kirana 91% grocery market share CY2025, kirana AOV ₹100-200, QC expected <10% of grocery market | Context |
| 5 | Savills — Dark Store India Report | Oct 2025 | Total dark stores 2,525, total area 13.0M sq ft, Tier-1: 1,725 stores / 9.0M sq ft, Tier-2+: 800 stores / 4.0M sq ft, typical store 3,000-8,000 sq ft, delivery radius 2-4 km | Model 1 |
| 6 | Kearney — Rise of Quick Commerce | 2025 | QC creates 62-64 jobs per ₹1Cr monthly GMV, industry pays avg ₹23,200/month | Context |
| 7 | Morgan Stanley India QC Report | 2025 | India QC TAM $57B by 2030 | Context |
| 8 | IIMA Working Paper — Ranjekar & Roy | Mar 2023 | Order processing time max 5 min, dispatch prep 2-2.5 min, three-tier supply chain (mother warehouse → DC → dark store), five QC business model types, purchase typology (stock-up / top-up / emergency) | Model 2 |

---

## Research Reports & Journalism

| # | Source | Year | Key Metrics Extracted | Used In |
|---|--------|------|-----------------------|---------|
| 1 | India Foundation — Promise of Quick Commerce | 2026 | Dark store network Oct 2025 (Savills data), rider earnings ₹21,000-27,726/month, median rider 38 days/year, 65% EV fleet share, traditional post-harvest loss 30-50% vs QC <5%, packaged foods 28% of QC sales, dairy 22%, EV avg speed 16km/h, avg delivery distance ~2km, Blinkit EBITDA positive Q3FY26 | Model 1, 2, 3 |
| 2 | Xylem PMS Research — Delivery Experiment | 2024-25 | Single delivery: 6km round trip, rider earned ₹54, petrol fuel cost ₹30, EV fuel cost ₹6 | Model 1 |
| 3 | Batch 1 — AOV & Rider Cost Comparison Chart | 2024-25 | Blinkit rider cost 7% of AOV, Zepto rider cost 10% of AOV, Blinkit AOV as % of GDP/capita 0.31%, Zepto 0.21% | Model 1 |
| 4 | Batch 1 — Rider Vehicle Cost Table | 2024-25 | Petrol scooter: ₹2.3-2.4/km, ₹14,000-16,000/month operating cost; EV charging: ₹1.0/km, ₹6,000-8,000/month; EV battery swap: ₹1.5-1.6/km, ₹8,000-10,000/month | Model 1, 2 |
| 5 | Batch 1 — Dark Store Investment Comparison | 2024-25 | Blinkit: 800-4,000 sq ft, ₹1Cr-1.5Cr investment, ₹1.4L-3L/month profit, 12-24 month payback; Zepto: 800-1,500 sq ft, ₹50L-60L; Instamart: 800-1,200 sq ft, ₹35L-40L, ₹1.4L-2.5L/month profit | Model 1 |
| 6 | Batch 1 — Gig Worker Earnings Table | 2024-25 | Gig economy partner: ₹35,000-40,000/month; India nominal per capita income: ₹20,500 | Model 1, 2 |
| 7 | Batch 2 — EBITDA Margin Outlook Chart | 2024-25 | Blinkit EBITDA 2023: -2.5%, 2026E: 4.4%; Instamart 2023: 2.5%, 2026E: 2.9%; QC steady state DuPont: EBIT 5% GMV, net profit 4%, RoE 38% | Model 1 |
| 8 | Batch 2 — RedSeer User Behaviour FY24 | 2024 | MTU grew >40%, ordering frequency ~6/month (up from 4.4 in FY21), AOV grew >15%, metro = ~90% GMV | Model 2, 3 |
| 9 | Batch 1 — Buying Frequency by Category | 2024 | Dairy: 44% daily, 17% 4-6x/week; F&V: 9% daily; Staples: 62% once in 2+ months | Model 2 |

---

## Assumptions Log

> Parameters that cannot be directly sourced — logged with rationale.

| Parameter | Value Used | Rationale | Confidence |
|-----------|-----------|-----------|------------|
| Tier-1 AOV assumption | ₹600 | Blended between Blinkit NAOV (₹525) and Instamart AOV (₹667); accounts for platform maturity differences | Medium |
| Tier-2 AOV assumption | ₹390 | Tier-1 × 0.65 (RedSeer -35% differential applied) | Medium |
| Tier-1 monthly rent | ₹2,00,000 | Midpoint of RedSeer benchmark range ₹1.5L-3L | Medium |
| Tier-2 monthly rent | ₹60,000 | Midpoint of RedSeer benchmark range ₹40K-80K | Medium |
| Picking/packing cost per order | ₹15 | Derived: picker handles 12 orders/hour (IIMA), monthly salary ₹18,000 → ₹18,000/(26×8×12) ≈ ₹7.2/order plus overhead; rounded to ₹15 | Low |
| Overhead per order (Tier-1) | ₹20 | Below-contribution costs ~9.5% of GOV (Swiggy data); at ₹600 GOV = ₹57/order total below-contribution; subtract marketing/CAC to isolate tech+overhead ≈ ₹20 | Low |
| Delivery fee per order | ₹25 | Estimated from revenue decomposition; platforms charge ₹15-40 depending on basket size | Low |
| Tier-2 breakeven OPD | 1,020-1,200 | RedSeer states 1.5-2x Tier-1 breakeven; Tier-1 breakeven ~600 orders (low AOV scenario); upper end used conservatively | Medium |
| Non-grocery margin | 42.5% | Midpoint of 35-50% industry benchmark range | Medium |
| Grocery margin | 12.5% | Midpoint of 10-15% FMCG industry standard | Medium |
| Expiry provision Tier-1 | 3% of COGS | QC wastage <5%; conservative estimate for mature store with good inventory management | Medium |
| Expiry provision Tier-2 | 5% of COGS | Higher wastage risk in lower-volume Tier-2 stores | Medium |