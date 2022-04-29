import requests


def find_place(toponim_to_find):
    toponim_to_find = '+'.join(toponim_to_find.split())

    server_gtocoder = 'http://geocode-maps.yandex.ru/1.x/'
    params = {'apikey': "40d1649f-0493-4b70-98ba-98533de7710b",
              'geocode': toponim_to_find,
              'format': 'json'}

    response_geocoder = requests.get(server_gtocoder, params=params)
    json_response = response_geocoder.json()

    pos = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    coord_x, coord_y = pos.split()

    full_address = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']

    return float(coord_x), float(coord_y), full_address


def picture(coord_x, coord_y, scale, space='map', new_pt=False):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coord_x},{coord_y}&spn={scale},{scale}&l={space}"

    # метка
    pt = f'&pt={coord_x},{coord_y},pm2rdm'
    map_request += pt

    response = requests.get(map_request)

    map_file = "static/img/map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


def work_with_api(title_find_place, new_picture=False):
    coord_x, coord_y, full_address = find_place(title_find_place)
    if new_picture:
        picture(coord_x, coord_y, 0.2)

    return full_address
