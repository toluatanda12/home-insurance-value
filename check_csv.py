import csv

with open('home_prices.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    print("First 15 columns:")
    for i, name in enumerate(reader.fieldnames[:15]):
        print(f"  {i}: {name}")
    
    print("\nLooking for date/price columns:")
    for name in reader.fieldnames:
        if '20' in name or '-' in name:
            print(f"  -> {name}")
            break
    
    print("\nFirst row sample:")
    row = next(reader)
    for key in reader.fieldnames[:8]:
        print(f"  {key}: {row.get(key, 'N/A')}")