import psycopg2
import googlemaps
from django.shortcuts import render, request
import pandas as pd
import json
import requests
from time import sleep


body_unicode = request.body.decode('utf-8')
body = json.loads(body_unicode)
content = body['content']

# Create your views here.
lat_ori = input('Masukkan lat asal:')
long_ori = input('Masukkan long asal:')
radius = input('Masukkan radius(dalam meter):')
types_user = input('Masukkan types:')
keyword_user = input('Masukkan keyword:')
# -6.2097
# 106.90166


def scrapping():
    """
    /////////////////////////////////////////////////////////////////////////////

    CODING FIRST PAGE

    /////////////////////////////////////////////////////////////////////////////
    """

    data_cust = {}
    #token, latitude, longitude, name, place_id, types_places, vicinity = [],[],[],[],[],[], []

    apik = 'AIzaSyDiFSOQvPbWVh3voJPSSORT9TSfKAXMy7E'
    urls = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&key={}&type={}&keyword={}'.format(
        lat_ori, long_ori, radius, apik, types_user, keyword_user)
    r = requests.get(urls)
    data_cust['0'] = r.json()

    """
    /////////////////////////////////////////////////////////////////////////////

    CODE FOR NEXT PAGE TOKEN

    /////////////////////////////////////////////////////////////////////////////
    """

    for number in range(10):

        content = str(number)
        if 'next_page_token' in data_cust[content].keys():
            sleep(5)
            pagetoken = data_cust[content]['next_page_token']
            apik = 'AIzaSyDiFSOQvPbWVh3voJPSSORT9TSfKAXMy7E'
            urls = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&type={}&keyword={}&key={}{pagetoken}'.format(
                lat_ori, long_ori, radius, types_user, keyword_user, apik, pagetoken="&pagetoken="+pagetoken if pagetoken else "")
            r = requests.get(urls)
            get = requests.post(urls)
            print(get)
            new_id = str(number+1)
            data_cust[new_id] = r.json()
        else:
            print("Done")
            break

    latitude, longitude, name, place_id, types_places, vicinity = [], [], [], [], [], []
    for i in range(number+1):
        content = str(i)
        for numbers in range(len(data_cust[content]['results'])):
            latitude.append(data_cust[content]['results']
                            [numbers]['geometry']['location']['lat'])
            longitude.append(data_cust[content]['results']
                             [numbers]['geometry']['location']['lng'])
            name.append(data_cust[content]['results'][numbers]['name'])
            place_id.append(data_cust[content]['results'][numbers]['place_id'])
            types_places.append(
                data_cust[content]['results'][numbers]['types'][0])
            vicinity.append(data_cust[content]['results'][numbers]['vicinity'])

    datacustype = pd.DataFrame({'customer_name': name, 'customer_type': types_places, 'place_id': place_id,
                                'keyword': keyword_user, 'radius': radius, 'latitude_origin': lat_ori, 'longitude_origin': long_ori, 'latitude_destination': latitude,
                                'longitude_destination': longitude})
    datacustype

    """
    /////////////////////////////////////////////////////////////////////////////

    PHONE NUMBER

    /////////////////////////////////////////////////////////////////////////////
    """

    data_number = {}
    for number in datacustype['place_id'].values:
        apik = 'AIzaSyDiFSOQvPbWVh3voJPSSORT9TSfKAXMy7E'
        urls = 'https://maps.googleapis.com/maps/api/place/details/json?place_id={}&fields=name,formatted_address,rating,formatted_phone_number&key={}'.format(
            number, apik)
        r = requests.get(urls)
        data_number[number] = r.json()

    data_number

    datanumb = pd.DataFrame.from_dict(data_number).T.reset_index()
    datanumb.columns = ['place_id', 'html_attributions', 'result', 'status']
    datanumb

    name, phone, alamat = [], [], []

    for number in range(len(datanumb)):
        if datanumb['status'][number] == 'NOT_FOUND':
            name.append('Unknown')
            phone.append(0)
            alamat.append('-')
        else:
            name.append(datanumb['result'][number]['name'])
            alamat.append(datanumb['result'][number]['formatted_address'])
            if 'formatted_phone_number' in (datanumb['result'][number].keys()):
                phone.append(datanumb['result'][number]
                             ['formatted_phone_number'])
            else:
                phone.append(0)

    datanumb2 = pd.DataFrame(
        {'customer_name': name, 'customer_address': alamat, 'phone_number': phone})
    datanumb2['place_id'] = datanumb['place_id']
    datanumb2

    """
    /////////////////////////////////////////////////////////////////////////////

    DATA MERGE

    /////////////////////////////////////////////////////////////////////////////
    """

    datamerge = datacustype.merge(datanumb2, how='left', on='place_id')
    datamerge

    """
    /////////////////////////////////////////////////////////////////////////////

    DUMMY

    /////////////////////////////////////////////////////////////////////////////
    """

    datadummy = datamerge.copy()
    datadummy

    datadummydrop = datadummy.drop(['customer_name_y'], axis=1)
    datadummydrop.rename(
        columns={'customer_name_x': 'customer_name'}, inplace=True)
    datadummydrop2 = datadummydrop[['customer_name', 'customer_address', 'customer_type', 'keyword', 'radius',
                                    'place_id', 'latitude_origin', 'longitude_origin', 'latitude_destination', 'longitude_destination', 'phone_number']]
    datadummydrop2

    """
    /////////////////////////////////////////////////////////////////////////////

    DISTANCE MATRIX

    /////////////////////////////////////////////////////////////////////////////
    """

    API_key = 'AIzaSyDiFSOQvPbWVh3voJPSSORT9TSfKAXMy7E'  # enter Google Maps API key
    gmaps = googlemaps.Client(key=API_key)

    distancedrive, distancewalks = [], []

    # Loop through each row in the data frame using pairwise
    for number in range(datadummydrop2.shape[0]):
        # Assign latitude and longitude as origin/departure points
        LatOrigin = datadummydrop2['latitude_origin'][number]
        LongOrigin = datadummydrop2['longitude_origin'][number]
        origins = (LatOrigin, LongOrigin)

        # Assign latitude and longitude from the next row as the destination point
        # Save value as lat
        LatDest = datadummydrop2['latitude_destination'][number]
        # Save value as lat
        LongDest = datadummydrop2['longitude_destination'][number]
        destination = (LatDest, LongDest)

        # pass origin and destination variables to distance_matrix function# output in meters
        result = gmaps.distance_matrix(origins, destination, mode='driving', avoid='tolls',
                                       units='metric', departure_time=1703981100)["rows"][0]["elements"][0]["distance"]["value"]
    # 1703981100    #1606867500
        # append result to list
        distancedrive.append(result)

    datadummydrop2['distance_driving'] = distancedrive
    datadummydrop3 = datadummydrop2.sort_values(
        by=['distance_driving'], ascending=True, ignore_index=True)
    datadummydrop3

    """
    /////////////////////////////////////////////////////////////////////////////

    DATAFRAME TO POSTGRE

    /////////////////////////////////////////////////////////////////////////////
    """

    database = psycopg2.connect(database="customerDB",
                                user="postgres",
                                password="1234",
                                host="localhost")

    cursor = database.cursor()

    for i in datadummydrop3.index:
        c1 = datadummydrop3['customer_name'][i]
        c2 = datadummydrop3['customer_address'][i]
        c3 = datadummydrop3['customer_type'][i]
        c4 = datadummydrop3['keyword'][i]
        c5 = datadummydrop3['radius'][i]
        c6 = datadummydrop3['place_id'][i]
        c7 = datadummydrop3['latitude_origin'][i]
        c8 = datadummydrop3['longitude_origin'][i]
        c9 = datadummydrop3['latitude_destination'][i]
        c10 = datadummydrop3['longitude_destination'][i]
        c11 = datadummydrop3['phone_number'][i]
        c12 = datadummydrop3['distance_driving'][i]
        query = """
        Insert into customertarget_customerpotential(customer_name, customer_address, customer_type, keyword, radius, place_id, latitude_origin, longitude_origin, latitude_destination, longitude_destination, phone_number, distance_driving) VALUES('%s','%s','%s','%s','%s','%s',%s,%s,%s,%s,'%s',%s);
        """ % (c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12)
        cursor.execute(query)
    cursor.close()

    database.commit()
    database.close()

    print("Data berhasil di upload")
