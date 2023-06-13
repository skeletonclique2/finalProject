import pandas as pd
import random

locations = [(floor, apartment) for floor in range(1, 7) for apartment in range(1, 5)]

apartments = pd.DataFrame(locations, columns=['Floor', 'Apartment'])

# Add boolean columns for broken_window and broken_lock
apartments['broken_window'] = False
apartments['broken_lock'] = False

floor_number = random.randint(1, 6)
apartment_number = random.randint(1, 4)

# Update the 'broken_window' variable for a specific apartment
apartments.loc[(apartments['Floor'] == floor_number) & (apartments['Apartment'] == apartment_number), 'broken_window'] = True
apartments.loc[(apartments['Floor'] == floor_number) & (apartments['Apartment'] == apartment_number), 'broken_lock'] = True

# Search and print apartments with both variables set to True
filtered_fl = apartments.loc[(apartments['broken_window'] == True) & (apartments['broken_lock'] == True), 'Floor']
filtered_app = apartments.loc[(apartments['broken_window'] == True) & (apartments['broken_lock'] == True), 'Apartment']

print("Apartment number with broken window and broken lock:")
for apartment in filtered_fl:
    print(apartment)

for floor in filtered_app:
    print(floor)

# Print the DataFrame
print(apartments)