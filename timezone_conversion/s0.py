import datetime
import pytz
from pytz import timezone
import phonenumbers
from phonenumbers import geocoder
from faker import Faker
import pandas as pd

from models import db, Patient
from utils import *

"""zone = "US/Pacific"
time = "3 pm"
time = int(time.split(" ")[0])
print(convertLocalStartToUtcStart(zone, time))
"""


# fake users
numbers = ["16692419870", "16617480240", "14436533745"]
available = [["3 pm", "7 pm"], ["11 am", "3 pm"], ["11 am", "3 pm"]]
names = [fake.name() for i in range(len(numbers))]
zones = [convertNumberToTimeZone(i) for i in numbers]

# extract digits from each element of list in lists
available = availabilityToUTC(available)
for idx, i in enumerate(available):
    print(convertLocalStartToUtcStart(zones[idx], available[idx][0]), convertLocalStartToUtcStart(zones[idx], available[idx][1]))
