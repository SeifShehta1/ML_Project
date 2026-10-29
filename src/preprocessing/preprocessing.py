# =================================
# Initial comments for preprcessing
# =================================

#drop ReservationStatus and ReservationStatusDate. Check-Out always means IsCanceled=0, and Canceled or No-Show always means 1. The status date is when that outcome was recorded
#Text columns are padded with whitespace. Strip them before any grouping or encoding.
#Agent and Company use the string 'NULL' instead of real missing values, so isna() won’t find them.
#Children is float, but should be an integer.
#167 rows with zero guests and 331 rows with zero nights: remove them.
#Undefined categories: MarketSegment (2 rows), DistributionChannel (4 rows). Merge into the most common category.
#296 repeat guests have no prior bookings recorded, and 4,647 non-repeat guests have previous cancellations.
#DaysInWaitingList is 0 for 96% of rows. Convert to a binary flag.
#Lead times over 500 days (455 rows) and stays over 30 nights (15 rows) are rare but plausible, cap them rather than delete.

#Feature engineering ideas:
#TotalNights, TotalGuests, HasKids, RoomTypeChanged
#An actual arrival date, which gives weekday and season
#Total cost (ADR × TotalNights)
#The redundant columns ArrivalDateWeekNumber and ArrivalDateDayOfMonth can be dropped once we have a proper date.

#The 2015 data covers only 6 months, 2016 covers 12 and 2017 covers 8. Don’t treat ArrivalDateYear as a generalisable feature, and be careful with month effects because the years aren’t balanced.
#Stratify on IsCanceled.

#Duplicates and Categorical encoding 


# Import the required libraries
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
        ((booking_data['Adults'] == 0) & (booking_data['IsCanceled'] == 0)) | 
        (booking_data['MarketSegment'] == 'Undefined') | 
        (booking_data['DistributionChannel'] == 'Undefined')
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

# Clip extreme outliers in non-continous numeric columuns to specific upper limit
booking_data['Babies'] = booking_data['Babies'].clip(upper=1)
booking_data['Children'] = booking_data['Children'].clip(upper=2)