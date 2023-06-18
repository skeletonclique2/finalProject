import pandas as pd
import random

locations = [(floor, apartment) for floor in range(1, 9) for apartment in range(1, 6)]

apartments = pd.DataFrame(locations, columns=['Floor', 'Apartment'])

# Add boolean columns for broken_window, broken_lock, and intrusion variables
apartments['broken_window'] = False
apartments['broken_lock'] = False
apartments['both_broken'] = False

# Select a random apartment index
intrusion_index = random.randint(0, len(locations) - 1)

# Randomly set either or both variables to True for the selected apartment
apartments.loc[intrusion_index, 'broken_window'] = random.choice([True, False])
apartments.loc[intrusion_index, 'broken_lock'] = random.choice([True, False])

# Set the intrusion variable to True if both broken_window and broken_lock variables are True
apartments.loc[(apartments['broken_window'] == True) & (apartments['broken_lock'] == True), 'both_broken'] = True

# Search and print the apartment with either or both variables set to True
filtered_apartments = apartments.loc[(apartments['broken_window'] == True) | (apartments['broken_lock'] == True)]

print("Found the Intrusion!")
for _, apartment in filtered_apartments.iterrows():
    print(f"Floor: {apartment['Floor']}, Apartment: {apartment['Apartment']}")

# Print the DataFrame
print(apartments)
