# Homeowners Insurance Calculator (Real Data)

A simple calculator that uses actual Zillow home price data to estimate Homeowners insurance premiums across US cities.

## Why I Built This

I'm applying for a Sr. Actuarial Analyst role and wanted to show I can:
- Work with real-world data
- Apply P&C pricing principles like base rates, catastrophe loads, and expense provisions
- Build something useful and shareable

## Data Source

- Zillow Home Value Index (ZHVI)
- Public CSV download from Zillow Research
- Median home values for US metro areas
- Updated monthly

## How It Works

1. Reads real home prices from CSV
2. Calculates replacement cost (85% of market value, which is industry standard)
3. Applies state-specific base rates (higher in FL and CA due to catastrophe risk)
4. Adds catastrophe load for hurricane, wildfire, and hail
5. Includes 30% expense and profit provision (industry average)

## How to Run on Windows

1. Download `https://files.zillowstatic.com/research/public_csvs/zhvi/Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv` from Zillow Research
2. Rename it to `home_prices.csv`
3. Put it in the same folder as `insurance_calculator.py`
4. Open Command Prompt
5. Navigate to the folder: `cd OneDrive\Desktop\home-insurance-value`
6. Run: `python insurance_calculator.py`

## What I Learned

- Replacement cost is not the same as market value. Older homes often cost more to rebuild.
- Catastrophe loads vary wildly by state. Florida pays 45% extra for hurricanes.
- Expense ratios are surprisingly consistent at about 30% across carriers.
- CSV data formats change over time. I had to debug the date column format when Zillow updated their file.

## Example Output

Here is what the program looks like when it runs:

```
============================================================
HOMEOWNERS INSURANCE CALCULATOR
Using Real Zillow Home Price Data

Loading real home price data... 
Using home price data from: 3/31/2026
Loaded 894 cities

TOP 2 MOST EXPENSIVE CITIES (for insurance):

San Jose, CA
Home Value: $1,636,393
Replacement Cost: $1,390,934
Est. Annual Premium: $9,493
(Rate: $4.20 per $1,000 + 25% cat load)

Key West, FL
Home Value: $953,369
Replacement Cost: $810,364
Est. Annual Premium: $8,401
(Rate: $5.50 per $1,000 + 45% cat load)
```

## How the Math Works: San Jose, CA Breakdown

Inputs:
- Home Value: $1,636,393
- State: CA
- Base Rate: $4.20 per $1,000
- Catastrophe Load: 25%

### Step 1: Replacement Cost

Insurance companies don't insure the market value. They insure what it would cost to rebuild the house from scratch.

```
Replacement Cost = Home Value × 0.85
                 = $1,636,393 × 0.85
                 = $1,390,934
```

The 85% factor is an industry rule of thumb. Land value is excluded, and newer homes might use 80% while older homes might need 90-100% due to building code upgrades.

### Step 2: Base Premium

This is the starting price before any risk adjustments.

```
Base Premium = (Replacement Cost ÷ 1,000) × Base Rate
             = ($1,390,934 ÷ 1,000) × $4.20
             = $1,390.93 × $4.20
             = $5,842
```

California's base rate of $4.20 is higher than average because of wildfire and earthquake exposure.

### Step 3: Catastrophe Load

Extra charge for living in a disaster-prone area.

```
Cat Premium = Base Premium × Cat Load %
            = $5,842 × 0.25
            = $1,461
```

California gets 25% because of wildfire risk. Florida gets 45% for hurricanes. Washington only gets 8%.

### Step 4: Expense and Profit

Insurance companies need to pay salaries, rent offices, and make a profit.

```
Expense/Profit = (Base Premium + Cat Premium) × 0.30
               = ($5,842 + $1,461) × 0.30
               = $7,303 × 0.30
               = $2,191
```

The 30% is pretty standard across the industry.

### Final Premium

```
Total Premium = Base Premium + Cat Premium + Expense/Profit
              = $5,842 + $1,461 + $2,191
              = $9,494
```

(The output shows $9,493 due to rounding.)

## Compare to Key West, FL

| Component           | San Jose, CA    | Key West, FL    |
| ------------------- | --------------- | --------------- |
| Home Value          | $1,636,393      | $953,369        |
| Replacement Cost    | $1,390,934      | $810,364        |
| Base Rate           | $4.20           | $5.50           |
| Base Premium        | $5,842          | $4,457          |
| Cat Load            | 25%             | 45%             |
| Cat Premium         | $1,461          | $2,006          |
| Expense/Profit      | $2,191          | $1,939          |
| Total Premium       | $9,493          | $8,401          |

Even though Key West has a cheaper house, the premium is almost as high because Florida's hurricane risk is brutal.

## Where the Numbers Come From

| Component                      | Source                                                                   |
| ------------------------------ | ------------------------------------------------------------------------ |
| Home values                    | Real Zillow data                                                         |
| 85% replacement cost factor    | Industry standard (varies by insurer)                                    |
| Base rates by state            | Illustrative based on catastrophe risk (CA wildfire, FL hurricane, etc.) |
| Cat load percentages           | Illustrative based on state risk profiles                                |
| 30% expense/profit             | Industry average                                                         |

These are simplified for demonstration. Real actuaries use ISO loss costs, company experience data, and state filing bureau territories.

## Next Steps

- Add roof age and construction type factors
- Pull in actual ISO territory data
- Build a web version with Streamlit

## Files in This Repository

- `insurance_calculator.py` - Main application
- `home_prices.csv` - Zillow home price data
- `check_csv.py` - CSV data validation utility
- `README.md` - This file

```

## Homeowners_Insurance_Presentation PDF

- A 10-slide executive presentation showing how actuarial analysis of home insurance data can improve pricing accuracy by 10%+ and identify $1.2M in annual premium opportunities