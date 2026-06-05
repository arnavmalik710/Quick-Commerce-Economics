# Methodology

## Objective
Determine the operational conditions required for a quick-commerce dark store 
to achieve sustainable EBITDA profitability and compare profitability 
thresholds between Tier-1 and Tier-2 cities.

## Research approach
The project follows a bottom-up unit economics framework. Rather than 
analyzing platform-level financial statements, profitability is modeled at 
the individual dark-store level.

The analysis combines:
1. Industry research and public disclosures
2. Unit economics modeling
3. Demand modeling
4. Sensitivity analysis
5. Tier-1 vs Tier-2 scenario comparison

## Model 1 — Unit economics
A store-level contribution margin model constructed using publicly available 
industry benchmarks. Built bottom-up at the per-order level, then scaled to 
daily and monthly store-level EBITDA.

**Key variables:**

- AOV (Average Order Value) — total revenue per order placed. The primary 
  revenue driver. Varies significantly by SKU mix — a grocery-heavy store 
  has a lower AOV than one selling electronics and beauty products.

- Take rate — the percentage of AOV the platform retains as commission. 
  Sourced from public filings.

- Delivery fee — flat fee charged to the customer per order. Added to 
  revenue side.

- Rider payout — cost paid to the delivery rider per order. One of the 
  largest per-order costs.

- Picking and packing cost — labor cost of the in-store picker assembling 
  the order.

- Rent allocation per order — monthly dark store rent divided by total 
  monthly orders. Converts a fixed cost into a per-order figure.

- Inventory expiry provision — a percentage of COGS written off due to 
  unsold perishable stock. Higher for grocery-heavy stores.

- Overhead allocation — technology, warehouse management, and other fixed 
  costs allocated per order.

- SKU mix — the proportion of high-margin (electronics, beauty) vs 
  low-margin (grocery, FMCG) products in the store's inventory. The 
  central lever in the model.

**The formula:**
CM = (AOV × Take Rate) + Delivery Fee − Rider Payout− Picking and Packing Cost− Rent Allocation per Order− Expiry Provision−Overhead Allocation

**Scenarios modeled:**
- Grocery-only store
- Mixed SKU store
- Non-grocery-led store
- Tier-1 vs Tier-2 cost structure

**Objectives:**
- Calculate contribution margin per order across AOV levels
- Find breakeven order volume per day for each scenario
- Quantify the margin impact of shifting SKU mix

## Model 2 — Demand modeling
Order arrivals modeled using a Poisson distribution to approximate demand 
intensity across peak and off-peak windows.

The Poisson distribution models the probability of a given number of orders 
arriving in a fixed time window, assuming orders arrive independently and 
randomly at a known average rate.

**Key variables:**

- λ (lambda) — average orders arriving per hour in a given time window. 
  A separate λ is defined for each period of the day: early morning, 
  morning rush, midday, evening rush, and late night. Sourced from public 
  industry reports and calibrated separately for Tier-1 and Tier-2 stores.

- k — the actual number of orders arriving in a given hour. The distribution 
  predicts the probability of exactly k orders arriving given λ.

- s — number of riders/pickers on shift in a given time window. Compared 
  against k to identify overstaffing or understaffing.

- μ (mu) — service rate, the number of orders a single staff member can 
  handle per hour. Combined with s to give total store capacity (s × μ).

- Cost per idle staff hour — when k < s × μ, each idle worker is a direct 
  cost. Used to quantify idle-time waste across the day.

**The core comparison the model makes:**
- When λ > s × μ → capacity crash, delayed deliveries, lost orders
- When λ < s × μ → idle staff, margin drain

**Objectives:**
- Estimate order-density fluctuations across the day
- Evaluate staffing requirements per time window
- Identify and quantify capacity bottlenecks during demand surges

## Model 3 — Sensitivity analysis
Each key input variable from Model 1 is varied independently while holding 
all others constant. The resulting change in contribution margin and EBITDA 
is recorded, ranked, and visualized.

**Key variables:**

- AOV — tested across a range from low (grocery-heavy) to high 
  (non-grocery-led) to measure revenue sensitivity.

- Orders per day — varied to find the exact breakeven threshold and to 
  show how margin scales with volume.

- Rider cost — tested under base, surge (rain/night), and optimized 
  (dynamic scheduling) scenarios.

- Delivery fee — varied to find the minimum fee required to cover 
  last-mile costs at different order volumes.

- SKU mix (grocery vs non-grocery share) — the proportion of high-margin 
  products varied from 0% to 100% to map the full margin curve.

- Rent — varied between Tier-1 and Tier-2 cost structures to isolate the 
  impact of location on breakeven.

- Delivery time — varied to find the retention cliff, the point at which 
  customer churn accelerates sharply and repeat order frequency drops.

**Method:**
Each variable is moved by a fixed percentage (e.g. ±10%, ±20%) from its 
base case value. The resulting change in EBITDA is recorded. Variables are 
then ranked by impact magnitude.

**Outputs:**
- Tornado chart — variables ranked by their impact on EBITDA
- Retention cliff chart — delivery time vs customer retention curve
- Breakeven surface plot — AOV vs orders per day across SKU mix scenarios

## Outputs
- Breakeven order thresholds (Tier-1 vs Tier-2)
- EBITDA sensitivity charts
- Demand distribution visualizations
- Tier-1 vs Tier-2 comparison tables
- Final strategic recommendations