import pandas as pd
import glob

# Get all CSV files from the data folder
csv_files = glob.glob('data/*.csv')

# Create an empty list to store processed dataframes
all_data = []

# Process each CSV file
for file in csv_files:
    # Read the CSV file
    df = pd.read_csv(file)
    
    # Filter to only Pink Morsels
    df = df[df['product'] == 'pink morsel']
    
    # Remove $ sign from price and convert to float
    df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
    
    # Calculate sales (quantity * price)
    df['sales'] = df['quantity'] * df['price']
    
    # Keep only the columns we need: sales, date, region
    df = df[['sales', 'date', 'region']]
    
    # Add to our list
    all_data.append(df)
    print(f"Processed {file}: found {len(df)} pink morsel records")

# Combine all dataframes
final_df = pd.concat(all_data, ignore_index=True)

# Save to a single CSV file
final_df.to_csv('formatted_data.csv', index=False)

print("\n" + "="*50)
print(f"Total pink morsel records: {len(final_df)}")
print("\nPreview of formatted data:")
print(final_df.head(10))
print("\nData saved to formatted_data.csv")