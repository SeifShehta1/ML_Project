import pandas as pd

# Import the data
booking_data = pd.read_csv("data/Hotel_bookings.csv")

# Remove Missing values in ['Children', 'Country'] columns
booking_data.dropna(subset=['Children', 'Country'], inplace=True)
print (booking_data.shape) # New shape => (79302, 31)

# Remove invalid bookings
booking_data = booking_data[
    ~(
        ((booking_data['StaysInWeekNights'] == 0) & (booking_data['StaysInWeekendNights'] == 0) & (booking_data['IsCanceled'] == 0)) |
        ((booking_data['Adults'] == 0) & (booking_data['Children'] == 0) & (booking_data['Babies'] == 0) & (booking_data['IsCanceled'] == 0))
    )
]
print (booking_data.shape) # New shape => (78907, 31)

# Convert "NULL" in ['Company'] into "Unknown" as a category
booking_data['Company'] = booking_data['Company'].str.strip()
booking_data['Company'] = booking_data['Company'].str.replace('NULL', 'Unknown', regex=False)
print (booking_data['Company'].value_counts())
print (booking_data.shape)

# Remove row with ADR 5400 [Very outlier]
booking_data = booking_data[
    ~(
        ((booking_data['ADR'] == 5400)))
]
print (booking_data.shape)