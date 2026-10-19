# Import the required libraries
import pandas as pd

# Import the data
booking_data = pd.read_csv("data/Hotel_bookings.csv")

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