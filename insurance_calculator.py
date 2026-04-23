"""
Homeowners Insurance Calculator - Real World Data
Uses actual Zillow home price data to estimate insurance premiums
"""

import csv
import os


def load_home_prices(filename):
    """Read real home price data from Zillow CSV"""
    cities = []
    
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Find month columns (format: M/D/YYYY or MM/DD/YYYY)
        months = [col for col in reader.fieldnames if '/' in col and len(col.split('/')[-1]) == 4]
        latest_month = months[-1] if months else None
        
        print(f"Using home price data from: {latest_month}")
        print("-" * 50)
        
        for row in reader:
            city = row.get('RegionName', 'Unknown')
            state = row.get('StateName', '')
            price = row.get(latest_month, '')
            
            # Skip rows with missing data or non-metro areas
            if price and price != '' and state and state != '':
                try:
                    cities.append({
                        'city': city,
                        'state': state,
                        'home_value': float(price)
                    })
                except ValueError:
                    continue  # Skip if price isn't a number
    
    return cities


def estimate_insurance_premium(home_value, state):
    """
    Estimate HO-3 premium based on real home value
    Uses simplified but realistic actuarial approach
    """
    
    # Base rate per $1,000 of coverage (varies by state risk)
    STATE_BASE_RATES = {
        'CA': 4.20, 'FL': 5.50, 'TX': 3.80, 'NY': 3.20, 'IL': 2.90,
        'WA': 3.10, 'OR': 3.15, 'CO': 3.40, 'AZ': 2.80, 'NC': 3.00,
        'MI': 2.85, 'OH': 2.80, 'GA': 2.95, 'PA': 3.00, 'VA': 2.90,
        'MA': 3.30, 'TN': 2.85, 'IN': 2.80, 'MO': 2.85, 'MD': 3.10,
        'WI': 2.90, 'MN': 2.95, 'SC': 2.90, 'AL': 2.95, 'LA': 4.50,
        'KY': 2.80, 'OK': 3.20, 'CT': 3.20, 'UT': 2.85, 'IA': 2.80,
        'NV': 2.90, 'AR': 2.80, 'MS': 2.90, 'KS': 2.90, 'NM': 2.85,
        'NE': 2.80, 'WV': 2.75, 'ID': 2.80, 'HI': 4.00, 'NH': 3.00,
        'ME': 2.95, 'MT': 2.80, 'RI': 3.10, 'DE': 3.00, 'SD': 2.75,
        'ND': 2.75, 'AK': 3.50, 'VT': 2.90, 'WY': 2.80, 'DC': 3.20,
    }
    
    # Default if state not in our list
    base_rate = STATE_BASE_RATES.get(state, 3.50)
    
    # Calculate base premium from home value
    replacement_cost = home_value * 0.85
    base_premium = (replacement_cost / 1000) * base_rate
    
    # State-specific catastrophe load
    cat_loads = {
        'CA': 0.25, 'FL': 0.45, 'TX': 0.15, 'LA': 0.40, 'OK': 0.12,
        'KS': 0.10, 'HI': 0.30, 'AK': 0.15, 'WA': 0.08, 'OR': 0.18,
        'CO': 0.12, 'NY': 0.05, 'MA': 0.06,
    }
    
    cat_load = cat_loads.get(state, 0.10)
    cat_premium = base_premium * cat_load
    
    # Fixed expense and profit provision (industry standard ~30%)
    expense_profit = (base_premium + cat_premium) * 0.30
    
    total_premium = base_premium + cat_premium + expense_profit
    
    return {
        'home_value': home_value,
        'replacement_cost': replacement_cost,
        'base_premium': base_premium,
        'cat_load': cat_premium,
        'expense_profit': expense_profit,
        'total_premium': total_premium,
        'rate_per_1000': base_rate,
        'cat_load_pct': cat_load * 100
    }


def main():
    """Main program - runs the calculator"""
    
    print("=" * 60)
    print("HOMEOWNERS INSURANCE CALCULATOR")
    print("Using Real Zillow Home Price Data")
    print("=" * 60)
    print()
    
    # Find the data file
    filename = 'home_prices.csv'
    
    if not os.path.exists(filename):
        print("ERROR: Can't find home_prices.csv")
        print("Please download it from Zillow and put it in this folder.")
        return
    
    # Load real home prices
    print("Loading real home price data...")
    cities = load_home_prices(filename)
    print(f"Loaded {len(cities)} cities")
    print()
    
    if len(cities) == 0:
        print("ERROR: No valid cities found in the CSV file.")
        return
    
    # Calculate insurance for all and sort
    for city in cities:
        city['insurance'] = estimate_insurance_premium(
            city['home_value'], 
            city['state']
        )
    
    # Sort by total premium
    sorted_cities = sorted(cities, key=lambda x: x['insurance']['total_premium'], reverse=True)
    
    # Show top 10 most expensive cities
    print("TOP 10 MOST EXPENSIVE CITIES (for insurance):")
    print("-" * 60)
    
    for i, city in enumerate(sorted_cities[:10], 1):
        ins = city['insurance']
        print(f"{i}. {city['city']}, {city['state']}")
        print(f"   Home Value: ${ins['home_value']:,.0f}")
        print(f"   Replacement Cost: ${ins['replacement_cost']:,.0f}")
        print(f"   Est. Annual Premium: ${ins['total_premium']:,.0f}")
        print(f"   (Rate: ${ins['rate_per_1000']:.2f} per $1,000 + {ins['cat_load_pct']:.0f}% cat load)")
        print()
    
    # Interactive mode
    print("-" * 60)
    print("INTERACTIVE MODE")
    print("-" * 60)
    
    while True:
        print("\nOptions:")
        print("1. Look up a city from the data")
        print("2. Enter your own home value")
        print("3. Quit")
        
        choice = input("\nPick 1, 2, or 3: ").strip()
        
        if choice == '3':
            print("Goodbye!")
            break
        
        elif choice == '1':
            city_name = input("Enter city name (or part of it): ").strip().lower()
            matches = [c for c in cities if city_name in c['city'].lower()]
            
            if not matches:
                print("City not found. Try again.")
                continue
            
            print(f"\nFound {len(matches)} match(es):")
            for match in matches[:5]:
                ins = match['insurance']
                print(f"\n  {match['city']}, {match['state']}")
                print(f"  Home Value: ${ins['home_value']:,.0f}")
                print(f"  Base Premium: ${ins['base_premium']:,.0f}")
                print(f"  Cat Load: ${ins['cat_load']:,.0f}")
                print(f"  TOTAL PREMIUM: ${ins['total_premium']:,.0f}")
        
        elif choice == '2':
            try:
                value = float(input("Enter your home value ($): "))
                state = input("Enter state (2-letter code, e.g., CA, TX, FL): ").strip().upper()
                
                ins = estimate_insurance_premium(value, state)
                
                print(f"\n  Home Value: ${ins['home_value']:,.0f}")
                print(f"  Replacement Cost: ${ins['replacement_cost']:,.0f}")
                print(f"  Base Premium: ${ins['base_premium']:,.0f}")
                print(f"  Cat Load: ${ins['cat_load']:,.0f}")
                print(f"  Expense/Profit: ${ins['expense_profit']:,.0f}")
                print(f"  TOTAL PREMIUM: ${ins['total_premium']:,.0f}")
                
            except ValueError:
                print("Please enter a valid number for home value.")
        
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()