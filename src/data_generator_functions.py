'''
Users
    - name
    - email
    - rating
    - country
'''
from time import time
import numpy as np
import pandas as pd
import json

from faker import Faker
from datetime import date, timedelta
from collections import OrderedDict


Faker.seed(1)
np.random.seed(1)
fake = Faker("en_ca")


##### Generate User Data #####
def create_users(n):
    users = []
    for _ in range(n):
        users.append(fake.profile(fields=("username","name",  "mail")))
    return users

def create_country_codes(n):
    country = []
    for _ in range(n):
        country.append(fake.country_code())
    return country



def create_rating(n):
    return np.round(np.random.normal(3.0, size = n),2)



def generate_user_data(n):
    users = create_users(n)
    countries = create_country_codes(n)
    ratings = create_rating(n)

    users_df = pd.DataFrame.from_dict(users)
    users_df['country_code'] = countries
    users_df['rating'] = ratings

    return users_df


##### Generate Room Data #####
'''
Rooms
    - owner_id (1,2500)
    - Address
    - summary
    - Max Capacity
    - Num_bedrooms
    - num_baths
    - Type (house, apartment, cottage)
    - rating
    - Cleaning Fee
'''

def randomize_owner(n):
    owners = []
    if n <= 1:
        owners.append(1)
    else:
        for _ in range(n):
            owners.append(np.random.randint(1,n))

    return owners

def create_addresses(n):
    addresses = []
    for _ in range(n):
        addresses.append(fake.street_address())
    return addresses

def create_summaries(n):
    summaries = []
    for _ in range(n):
        summaries.append(fake.paragraph(nb_sentences=3))
    return summaries

def create_max_capacity(n):
    max_cap = []
    for _ in range(n):
        max_cap.append(fake.random_element(
            elements=(OrderedDict([(4,0.2),(6, 0.5),(8, 0.25), (10, 0.04), (12, 0.01)])))
            )
    return max_cap

def create_num_baths(n):
    num_baths = []
    for _ in range(n):
        num_baths.append(np.random.randint(1,4))
    return num_baths

def create_type(n):
    room_type = []
    for _ in range(n):
        room_type.append(fake.random_element(
            elements=(OrderedDict([("house", 0.20), ("condo", 0.70), ("cottage", 0.10)])))
            )
    return room_type

def create_cleaning_fee(n):
    fees = []
    for _ in range(n):
        fees.append(fake.random_element(
            elements=(OrderedDict([(0.00, 0.50), (25, 0.25), (75, 0.2), (150, 0.05)]))
        ))
    return fees

def generate_room_data(n):
    owner_id = randomize_owner(n)
    address = create_addresses(n)
    summary = create_summaries(n)
    max_capacity = create_max_capacity(n)
    num_bathrooms = create_num_baths(n)
    room_type = create_type(n)
    room_rating = create_rating(n)
    cleaning_fee = create_cleaning_fee(n)

    rooms = pd.DataFrame.from_dict({'owner_id':owner_id})
    rooms['address'] = address
    rooms['summary'] = summary
    rooms['max_capcity'] = max_capacity
    rooms['num_bathrooms'] = num_bathrooms
    rooms['room_type'] = room_type
    rooms['room_rating'] = room_rating
    rooms['cleaning_fee'] = cleaning_fee

    return rooms

##### Generate Bookings Data #####
'''
Bookings
    - room_id
    - user_id (2501,10000)
    - duration
    - check in date
    - price
    - Total Cost
'''

def random_room_id(n):
    rooms = []
    for _ in range(n):
        rooms.append(np.random.randint(1,n))
    return rooms

def create_guest(n):
    guests = []
    for _ in range(n):
        guests.append(np.random.randint((n/4) + 1, n))
    return guests

def create_duration(n):
    duration = []
    for _ in range(n):
        duration.append(np.random.randint(1,n))
    return duration

def create_checkin(n):
  checkin = []
  for _ in range(n):
      checkin.append(fake.date_between_dates(date(2016,1,1), date(2021,12,31)))
  return checkin

def create_price(n):
    return np.round(np.random.normal(50.0, size = n),2)

def generate_booking_data(n, cleaning_fees):
    room_ids = random_room_id(n)
    check_in = create_checkin(n)
    user_id = create_guest(n)
    duration = create_duration(n)
    price_per_night = create_price(n)

    bookings = pd.DataFrame.from_dict({'room_id':room_ids})
    bookings['user_id'] = user_id
    bookings['check_in'] = check_in
    bookings['duration'] = duration

    calc_checkout = lambda x,y: x + timedelta(y)
    bookings['check_out'] = bookings.apply(lambda x: x['check_in'] + timedelta(x['duration']),1)
    bookings['price_per_night'] = price_per_night
    bookings['total_price'] = round((bookings['price_per_night'] + cleaning_fees), 2)

    return bookings
