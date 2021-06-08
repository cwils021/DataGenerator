import data_generator_functions as dgf
import pandas as pd

def generate_data(n):
    users = dgf.generate_user_data(n)
    rooms = dgf.generate_room_data(n)
    bookings = dgf.generate_booking_data(n, rooms['cleaning_fee'])
    try:
        users.to_sql()
        rooms.to_sql()
        bookings.to_sql()
    except:
        print("Write to DB unsuccessful")

if __name__ == '__main__':
    generate_data(100)
