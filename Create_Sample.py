import pandas as pd


# Load the full dataset
df = pd.read_csv('csv/Full_Fellowship_Dataset.csv')

# Filter by label
# Keep all the possitive rows because they are the smallest number
positive_rows = df[df['Fellowship'] == 'Positive']
# Because Negative are over twice the size of Positive (380 > 151 ) we keep a little bigger sample from the
# positive chunks something like 172
negative_rows = df[df['Fellowship'] == 'Negative'].sample(n=172, random_state=42)
# finally from the vast neutral chunks(1870) we keep 157 so the final sample will be 480 chunks
neutral_rows = df[df['Fellowship'] == 'Neutral'].sample(n=157, random_state=42)

# Combine all into one DataFrame
combined = pd.concat([positive_rows, negative_rows, neutral_rows], ignore_index=True)

# Shuffle the combined DataFrame
combined_shuffled = combined.sample(frac=1, random_state=42).reset_index(drop=True)

# Save to CSV
combined_shuffled.to_csv('csv/Sample_Fellowship_Dataset.csv', index=False)

print("Sample_Fellowship_Dataset.csv created successfully.")