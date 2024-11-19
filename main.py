from geopy.distance import distance
from folium import Map, Marker, Icon

from config import KEY
from utils import fetch_coordinates
from server import app

from json import load


def get_all_info_coffee(all_info_coffee: dict) -> list:
    accumulate = []
    for info in all_info_coffee:
        main_info = {
            "title": info['Name'],
            "longitude": info['Longitude_WGS84'],
            "latitude": info['Latitude_WGS84'],
        }
        accumulate.append(main_info)
    return accumulate


def define_my_coordinates() -> tuple:
    longitude_luntitude = fetch_coordinates(KEY, input("Гдк вы находитесь?: "))
    return longitude_luntitude


def combine_data(coffee_houses: list) -> tuple:
    coffee_house_with_distance = []
    for coffee_house in coffee_houses:
        coffee_location = (coffee_house["longitude"], coffee_house["latitude"])
        distance_km = distance(my_coordinates, coffee_location).km
        coffee_house.update(distance=distance_km)
        coffee_house_with_distance.append(coffee_house)
    return coffee_house_with_distance


def coffee_near_me(coffee_houses_with_distance):
    return coffee_houses_with_distance['distance']


def map_html(my_coord: tuple, nearest_5: list):
    map = Map(my_coord, zoom_start=15)
    Marker(
        location=[my_coord[0], my_coord[1]],
        popup="Me",
        icon=Icon(
            icon='person',
            icon_color='#f3f6f4',
            prefix='fa'
        )
    ).add_to(map)
    for coffee_house in nearest_5:
        Marker(
                location=[coffee_house["latitude"], coffee_house["longitude"]],
                tooltip="Click me",
                popup=coffee_house['title'],
                icon=Icon(
                    color='black',
                    icon_color='#f3f6f4',
                    icon='hamburger',
                    prefix='fa'
                )
        ).add_to(map)
    map.save("Coffee_map.html")


if __name__ == "__main__":
    with open('coffee.json', "r", encoding='cp1251') as read_json:
        coffee = load(read_json)
    coffee_houses = get_all_info_coffee(coffee)
    my_coordinates = fetch_coordinates(KEY, input("Гдк вы находитесь?: "))
    coffee_with_distance = combine_data(coffee_houses=coffee_houses)
    nearest_5 = sorted(coffee_with_distance, key=coffee_near_me)[:5]
    lantitude, longitude = my_coordinates
    map_html((longitude, lantitude), nearest_5)
    app.run('0.0.0.0')
