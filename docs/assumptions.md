# Assumptions

## General
- A single representative dark store is modeled, not a platform-wide P&L
- Tier-1 refers to a metro city, Tier-2 refers to a non-metro city
- All figures are in INR

## Demand
- Orders arrive randomly but at a known average rate (modeled via Poisson distribution)
- Peak demand windows are determined from available industry data and may vary by platform and geography
- Demand patterns are consistent across weekdays (weekends treated separately if needed)
- Demand is independent between successive orders
- Order cancellations are ignored in the base model

## Operations
- Average delivery distance is assumed constant within each city tier
- Rent is stable month-on-month (no seasonal variation)
- Picking staff count is fixed during a shift
- Picker productivity (orders picked per hour) remains constant during normal operations
- Rider availability is assumed stable — surge pricing, weather disruptions, 
  and gig worker shortages are not modeled
- Dark store capacity constraints are not reached unless explicitly modeled  

## Financials
- EBITDA is calculated as contribution margin less fixed operating expenses 
- Take rate, fulfillment cost, and delivery fee are held constant per scenario
- Expiry/write-off provision is a fixed % of COGS
- No platform-level cross-subsidization is modeled
- Technology and overhead costs (app, warehouse management) are 
  either explicitly included or excluded per scenario — not silently ignored
- Fixed costs are allocated at the dark-store level and do not vary with order volume 

## Competition
- The dark store operates in a stable competitive environment
- Entry of a competing store within the delivery radius is not modeled
- Market share is assumed constant across all scenarios

## Customer retention
- Repeat order frequency is held constant within each scenario
- Customer churn is treated as stable unless varied explicitly in the 
  sensitivity analysis
- Retention impact of delivery time degradation is modeled in Model 3 only

## Weather and surcharge
- Base model assumes standard weather conditions
- Rain and late-night surcharges on rider payouts are acknowledged but not 
  modeled in the base case
- Surcharge impact may be explored as a scenario in the sensitivity analysis

## Data Sources
- Public company filings, earnings calls, investor presentations, and industry reports are assumed to be reliable unless contradictory evidence is identified
- Missing values may be estimated using industry benchmarks with explicit documentation

## Limitations
- Real-world demand may have additional seasonality (festivals, weather)
- Actual platform figures may differ from public benchmarks
- Return logistics for non-grocery items are approximated as a cost provision only
- Competitive dynamics, rider availability shocks, and tax differences 
  across SKU categories are outside the base model scope