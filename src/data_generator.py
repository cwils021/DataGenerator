import data_generator_functions as dgf
import pandas as pd

def generate_data_csvs(n):
    users = dgf.generate_user_data(n)
    rooms = dgf.generate_room_data(n)
    bookings = dgf.generate_booking_data(n)

    users.to_csv("users.csv")
    rooms.to_csv("rooms.csv")
    bookings.to_csv("bookings.csv")


if __name__ == "__main__":
    generate_data_csvs(10000)
