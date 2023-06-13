import pandas as pd
import random
import tkinter as tk

# Function to update the apartment status
def update_apartment_status():
    floor_number = random.randint(1, 6)
    apartment_number = random.randint(1, 4)

    # Update the 'broken_window' and 'broken_lock' variables for a specific apartment
    apartments.loc[(apartments['Floor'] == floor_number) & (apartments['Apartment'] == apartment_number), 'broken_window'] = True
    apartments.loc[(apartments['Floor'] == floor_number) & (apartments['Apartment'] == apartment_number), 'broken_lock'] = True

    # Clear the previous results
    result_label.config(text="")

    # Search and display apartments with both variables set to True
    filtered_apartments = apartments.loc[(apartments['broken_window'] == True) & (apartments['broken_lock'] == True)]
    if not filtered_apartments.empty:
        result = ", ".join([f"Floor: {row['Floor']}, Apartment: {row['Apartment']}" for _, row in filtered_apartments.iterrows()])
        result_label.config(text=result)
    else:
        result_label.config(text="No apartments found")

# Create the Tkinter window
window = tk.Tk()
window.title("Intruder Detection and Localization")
window.geometry("400x200")

# Create a DataFrame to store apartment information
locations = [(floor, apartment) for floor in range(1, 7) for apartment in range(1, 5)]
apartments = pd.DataFrame(locations, columns=['Floor', 'Apartment'])
apartments['broken_window'] = False
apartments['broken_lock'] = False

# Create the update button
update_button = tk.Button(window, text="Update Status", command=update_apartment_status)
update_button.pack(pady=10)

# Create the result label
result_label = tk.Label(window, text="", font=("Arial", 12))
result_label.pack()

# Run the Tkinter event loop
window.mainloop()
