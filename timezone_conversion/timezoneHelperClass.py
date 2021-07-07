import datetime
import pytz
from pytz import timezone
import phonenumbers
from phonenumbers import geocoder
from faker import Faker
import pandas as pd

class TimeZoneHelper:
    def __init__(self, phoneNumber):
        self.phoneNumber = phoneNumber
        self.tzs_df = pd.read_csv("./data/tzmapping.csv")
        self.tzs_df.index = self.tzs_df['State']
        self.user_zone = self.numberToTimeZone()
        self.fmt = '%Y-%m-%d %H:%M:%S %Z%z'

    def numberToTimeZone(self):
        """converts a phone number to a timezone"""
        fmtNum = phonenumbers.parse("+" + str(self.phoneNumber))
        state = geocoder.description_for_number(fmtNum, 'en')
        time_zone = self.tzs_df.loc[state]['Zone'].split(" ")[0]
        return "US/" + time_zone

    def utcToLocal(self):
        """gets current local time from utc time given a zone in 24-hour time format"""
        # get utc time
        utc_dt = datetime.datetime.utcnow()
        # convert to localtime using tz object and string formatter
        zone_objct = timezone(self.user_zone)
        loc_dt = utc_dt.astimezone(zone_objct)
        return loc_dt.strftime(self.fmt)


tz = TimeZoneHelper("16692419870")
tz.numberToTimeZone()
print(tz.utcToLocal())
