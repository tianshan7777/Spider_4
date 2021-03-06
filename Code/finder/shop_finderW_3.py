from math import asin, sin, acos, cos, radians, sqrt
import pandas as pd

EARTH_R = 6378.1
#adult walking speed: 1.4 m/s or 5.0 km/h
WALKING_DIS = 2.52
radius = WALKING_DIS / EARTH_R

lats_max = []
lats_min = []
lons_max = []
lons_min = []

amh_list = []
beauty_list = []
clothing_list = []
convenience_list = []
department_list = []
discount_list = []
food_list = []
health_list = []
laundry_list = []
mall_list = []
sgbn_list = []
supermarket_list = []
travel_agency_list = []
other_list = []

#Calculate distance between two pointss
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

def find_lat(lat):

    lat_min = lat - radius
    lat_max = lat + radius

    return (lat_max, lat_min)

def find_lon(lat, lon):

    lat_T = asin(sin(lat)/cos(radius))
    delta_lon = acos( ( cos(radius) - sin(lat_T) * sin(lat) ) / ( cos(lat_T) * cos(lat) ) )
    lon_min = lon - delta_lon 
    lon_max = lon + delta_lon

    return (lon_max, lon_min)

#Load .csv data
print('This is number 10')
data = pd.read_csv('./MergedData/real_sale_apar/real_sale_apar_10.csv')
poi_data = pd.read_csv('./osm_data_clean/shop_clean.csv')

latitudes = data[['Latitude']]
longitudes = data[['Longitude']]
coordinates = poi_data['coordinate']
poi_types = poi_data['shop_types']

#Conver pandas onject to numpy array
latitudes = latitudes.values
longitudes = longitudes.values

#Iterate through
for i, j in zip(latitudes, longitudes):

    #Convert to float
    lat = float(i[0]) 
    lon = float(j[0])
    print("original:", lat, lon)

    lat, lon = map(radians, [lat, lon])
    print("in radians:", lat, lon)

    lat_max, lat_min = find_lat(lat)
    print("lat max:", lat_max)
    lats_max.append(lat_max)
    print("lat min:", lat_min)
    lats_min.append(lat_min)

    lon_max, lon_min = find_lon(lat, lon)
    print("lon max:", lon_max)
    lons_max.append(lon_max)
    print("lon min:", lon_min)
    lons_min.append(lon_min)

    counter = 0
    amh = 0
    beauty = 0
    clothing = 0
    convenience = 0
    department = 0
    discount = 0
    food = 0
    health = 0
    laundry= 0
    mall = 0
    sgbn = 0
    supermarket = 0
    travel_agency = 0
    other = 0

    for poi in coordinates:

        print("shop type:", str(poi_types[counter]))

        print("poi:", poi)

        point = poi.split(',')
        #Convert to float
        point[0] = radians(float(point[0]))
        point[1] = radians(float(point[1]))
        print(point)

        if (point[1] < lat_max and  point[1] > lat_min):
            if (point[0] < lon_max and point[0] > lon_min):
                print("_____________within area_______________:", point)

                haversine_dis = haversine(point[0], point[1], lon, lat)
                print("==========Haversine Calculated===========:", haversine_dis)

                if haversine_dis <= WALKING_DIS:
                    print("******************Accept*******************")
                    if str(poi_types[counter]) == 'Art, music, hobbies':
                        amh += 1
                    elif str(poi_types[counter]) == 'Beauty':
                        beauty += 1
                    elif str(poi_types[counter]) == 'Clothing, shoes, accessories':
                        clothing += 1
                    elif str(poi_types[counter]) == 'Convenience shop':
                        convenience += 1
                    elif str(poi_types[counter]) == 'Department Store':
                        department += 1
                    elif str(poi_types[counter]) == 'Discount store, charity':
                        discount += 1
                    elif str(poi_types[counter]) == 'Food, beverages':
                        food += 1
                    elif str(poi_types[counter]) == 'Health':
                        health += 1
                    elif str(poi_types[counter]) == 'Laundry':
                        laundry += 1
                    elif str(poi_types[counter]) == 'Mall':
                        mall += 1
                    elif str(poi_types[counter]) == 'Stationery, gifts, books, newspapers':
                        sgbn += 1
                    elif str(poi_types[counter]) == 'Travel Agency':
                        travel_agency += 1
                    elif str(poi_types[counter]) == 'Supermarket':
                        supermarket += 1
                    else:
                        other += 1
                        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&This is Others&&&&&&&&&&&&&&&&&&&&&&&&&&&&7')

        counter += 1

    amh_list.append(amh)
    beauty_list.append(beauty)
    clothing_list.append(clothing)
    convenience_list.append(convenience)
    department_list.append(department)
    discount_list.append(discount)
    food_list.append(food)
    health_list.append(health)
    laundry_list.append(laundry)
    mall_list.append(mall)
    sgbn_list.append(sgbn)
    travel_agency_list.append(travel_agency)
    supermarket_list.append(supermarket)
    other_list.append(other)

data['Shop: Art, music, hobbies'] = pd.Series(amh_list)
data['Shop: Beauty'] = pd.Series(beauty_list)
data['Shop: Clothing, shoes, accessories'] = pd.Series(clothing_list)
data['Shop: Convenience shop'] = pd.Series(convenience_list)
data['Shop: Department Store'] = pd.Series(department_list)
data['Shop: Discount store, charity'] = pd.Series(discount_list)
data['Shop: Food, beverages'] = pd.Series(food_list)
data['Shop: Health'] = pd.Series(health_list)
data['Shop: Laundry'] = pd.Series(laundry_list)
data['Shop: Mall'] = pd.Series(mall_list)
data['Shop: Stationery, gifts, books, newspapers'] = pd.Series(sgbn_list)
data['Shop: Supermarket'] = pd.Series(supermarket_list)
data['Shop: Travel Agency'] = pd.Series(travel_agency_list)
data['Shop: Others'] = pd.Series(other_list)
data.to_csv('real_sale_apar_10_shop_10minswalk.csv', index=False)







