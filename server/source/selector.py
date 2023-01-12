import math
import sqlite3
import database
import os
import atexit
import threading
import json

DB_FILENAME = "city.db"
RESULTS_FILENAME = "results.json"
SOURCE_DIR  = os.path.join(os.path.dirname(os.path.realpath(__file__)), '')
CATEGORIES = ("edukacja", "zdrowie", "rozrywka", "jedzenie", "sport", "kultura", "dzieci", "kawiarnie", "natura", "biznes", "uslugi", "transport", "sklepy")
RADIUS = 1000 # in meters
PRECALCULATED_COORDS = (
(54.46,18.425),
(54.46,18.444411764705883),
(54.46,18.463823529411766),
(54.46,18.483235294117648),
(54.46,18.50264705882353),
(54.46,18.522058823529413),
(54.46,18.541470588235295),
(54.46,18.560882352941178),
(54.46,18.58029411764706),
(54.46,18.59970588235294),
(54.46,18.61911764705882),
(54.46,18.638529411764704),
(54.46,18.657941176470587),
(54.46,18.67735294117647),
(54.46,18.69676470588235),
(54.46,18.716176470588234),
(54.46,18.735588235294117),
(54.44866666666667,18.425),
(54.44866666666667,18.444411764705883),
(54.44866666666667,18.463823529411766),
(54.44866666666667,18.483235294117648),
(54.44866666666667,18.50264705882353),
(54.44866666666667,18.522058823529413),
(54.44866666666667,18.541470588235295),
(54.44866666666667,18.560882352941178),
(54.44866666666667,18.58029411764706),
(54.44866666666667,18.59970588235294),
(54.44866666666667,18.61911764705882),
(54.44866666666667,18.638529411764704),
(54.44866666666667,18.657941176470587),
(54.44866666666667,18.67735294117647),
(54.44866666666667,18.69676470588235),
(54.44866666666667,18.716176470588234),
(54.44866666666667,18.735588235294117),
(54.437333333333335,18.425),
(54.437333333333335,18.444411764705883),
(54.437333333333335,18.463823529411766),
(54.437333333333335,18.483235294117648),
(54.437333333333335,18.50264705882353),
(54.437333333333335,18.522058823529413),
(54.437333333333335,18.541470588235295),
(54.437333333333335,18.560882352941178),
(54.437333333333335,18.58029411764706),
(54.437333333333335,18.59970588235294),
(54.437333333333335,18.61911764705882),
(54.437333333333335,18.638529411764704),
(54.437333333333335,18.657941176470587),
(54.437333333333335,18.67735294117647),
(54.437333333333335,18.69676470588235),
(54.437333333333335,18.716176470588234),
(54.437333333333335,18.735588235294117),
(54.426,18.425),
(54.426,18.444411764705883),
(54.426,18.463823529411766),
(54.426,18.483235294117648),
(54.426,18.50264705882353),
(54.426,18.522058823529413),
(54.426,18.541470588235295),
(54.426,18.560882352941178),
(54.426,18.58029411764706),
(54.426,18.59970588235294),
(54.426,18.61911764705882),
(54.426,18.638529411764704),
(54.426,18.657941176470587),
(54.426,18.67735294117647),
(54.426,18.69676470588235),
(54.426,18.716176470588234),
(54.426,18.735588235294117),
(54.41466666666667,18.425),
(54.41466666666667,18.444411764705883),
(54.41466666666667,18.463823529411766),
(54.41466666666667,18.483235294117648),
(54.41466666666667,18.50264705882353),
(54.41466666666667,18.522058823529413),
(54.41466666666667,18.541470588235295),
(54.41466666666667,18.560882352941178),
(54.41466666666667,18.58029411764706),
(54.41466666666667,18.59970588235294),
(54.41466666666667,18.61911764705882),
(54.41466666666667,18.638529411764704),
(54.41466666666667,18.657941176470587),
(54.41466666666667,18.67735294117647),
(54.41466666666667,18.69676470588235),
(54.41466666666667,18.716176470588234),
(54.41466666666667,18.735588235294117),
(54.403333333333336,18.425),
(54.403333333333336,18.444411764705883),
(54.403333333333336,18.463823529411766),
(54.403333333333336,18.483235294117648),
(54.403333333333336,18.50264705882353),
(54.403333333333336,18.522058823529413),
(54.403333333333336,18.541470588235295),
(54.403333333333336,18.560882352941178),
(54.403333333333336,18.58029411764706),
(54.403333333333336,18.59970588235294),
(54.403333333333336,18.61911764705882),
(54.403333333333336,18.638529411764704),
(54.403333333333336,18.657941176470587),
(54.403333333333336,18.67735294117647),
(54.403333333333336,18.69676470588235),
(54.403333333333336,18.716176470588234),
(54.403333333333336,18.735588235294117),
(54.392,18.425),
(54.392,18.444411764705883),
(54.392,18.463823529411766),
(54.392,18.483235294117648),
(54.392,18.50264705882353),
(54.392,18.522058823529413),
(54.392,18.541470588235295),
(54.392,18.560882352941178),
(54.392,18.58029411764706),
(54.392,18.59970588235294),
(54.392,18.61911764705882),
(54.392,18.638529411764704),
(54.392,18.657941176470587),
(54.392,18.67735294117647),
(54.392,18.69676470588235),
(54.392,18.716176470588234),
(54.392,18.735588235294117),
(54.38066666666667,18.425),
(54.38066666666667,18.444411764705883),
(54.38066666666667,18.463823529411766),
(54.38066666666667,18.483235294117648),
(54.38066666666667,18.50264705882353),
(54.38066666666667,18.522058823529413),
(54.38066666666667,18.541470588235295),
(54.38066666666667,18.560882352941178),
(54.38066666666667,18.58029411764706),
(54.38066666666667,18.59970588235294),
(54.38066666666667,18.61911764705882),
(54.38066666666667,18.638529411764704),
(54.38066666666667,18.657941176470587),
(54.38066666666667,18.67735294117647),
(54.38066666666667,18.69676470588235),
(54.38066666666667,18.716176470588234),
(54.38066666666667,18.735588235294117),
(54.36933333333333,18.425),
(54.36933333333333,18.444411764705883),
(54.36933333333333,18.463823529411766),
(54.36933333333333,18.483235294117648),
(54.36933333333333,18.50264705882353),
(54.36933333333333,18.522058823529413),
(54.36933333333333,18.541470588235295),
(54.36933333333333,18.560882352941178),
(54.36933333333333,18.58029411764706),
(54.36933333333333,18.59970588235294),
(54.36933333333333,18.61911764705882),
(54.36933333333333,18.638529411764704),
(54.36933333333333,18.657941176470587),
(54.36933333333333,18.67735294117647),
(54.36933333333333,18.69676470588235),
(54.36933333333333,18.716176470588234),
(54.36933333333333,18.735588235294117),
(54.358,18.425),
(54.358,18.444411764705883),
(54.358,18.463823529411766),
(54.358,18.483235294117648),
(54.358,18.50264705882353),
(54.358,18.522058823529413),
(54.358,18.541470588235295),
(54.358,18.560882352941178),
(54.358,18.58029411764706),
(54.358,18.59970588235294),
(54.358,18.61911764705882),
(54.358,18.638529411764704),
(54.358,18.657941176470587),
(54.358,18.67735294117647),
(54.358,18.69676470588235),
(54.358,18.716176470588234),
(54.358,18.735588235294117),
(54.346666666666664,18.425),
(54.346666666666664,18.444411764705883),
(54.346666666666664,18.463823529411766),
(54.346666666666664,18.483235294117648),
(54.346666666666664,18.50264705882353),
(54.346666666666664,18.522058823529413),
(54.346666666666664,18.541470588235295),
(54.346666666666664,18.560882352941178),
(54.346666666666664,18.58029411764706),
(54.346666666666664,18.59970588235294),
(54.346666666666664,18.61911764705882),
(54.346666666666664,18.638529411764704),
(54.346666666666664,18.657941176470587),
(54.346666666666664,18.67735294117647),
(54.346666666666664,18.69676470588235),
(54.346666666666664,18.716176470588234),
(54.346666666666664,18.735588235294117),
(54.33533333333333,18.425),
(54.33533333333333,18.444411764705883),
(54.33533333333333,18.463823529411766),
(54.33533333333333,18.483235294117648),
(54.33533333333333,18.50264705882353),
(54.33533333333333,18.522058823529413),
(54.33533333333333,18.541470588235295),
(54.33533333333333,18.560882352941178),
(54.33533333333333,18.58029411764706),
(54.33533333333333,18.59970588235294),
(54.33533333333333,18.61911764705882),
(54.33533333333333,18.638529411764704),
(54.33533333333333,18.657941176470587),
(54.33533333333333,18.67735294117647),
(54.33533333333333,18.69676470588235),
(54.33533333333333,18.716176470588234),
(54.33533333333333,18.735588235294117),
(54.324,18.425),
(54.324,18.444411764705883),
(54.324,18.463823529411766),
(54.324,18.483235294117648),
(54.324,18.50264705882353),
(54.324,18.522058823529413),
(54.324,18.541470588235295),
(54.324,18.560882352941178),
(54.324,18.58029411764706),
(54.324,18.59970588235294),
(54.324,18.61911764705882),
(54.324,18.638529411764704),
(54.324,18.657941176470587),
(54.324,18.67735294117647),
(54.324,18.69676470588235),
(54.324,18.716176470588234),
(54.324,18.735588235294117),
(54.312666666666665,18.425),
(54.312666666666665,18.444411764705883),
(54.312666666666665,18.463823529411766),
(54.312666666666665,18.483235294117648),
(54.312666666666665,18.50264705882353),
(54.312666666666665,18.522058823529413),
(54.312666666666665,18.541470588235295),
(54.312666666666665,18.560882352941178),
(54.312666666666665,18.58029411764706),
(54.312666666666665,18.59970588235294),
(54.312666666666665,18.61911764705882),
(54.312666666666665,18.638529411764704),
(54.312666666666665,18.657941176470587),
(54.312666666666665,18.67735294117647),
(54.312666666666665,18.69676470588235),
(54.312666666666665,18.716176470588234),
(54.312666666666665,18.735588235294117),
(54.30133333333333,18.425),
(54.30133333333333,18.444411764705883),
(54.30133333333333,18.463823529411766),
(54.30133333333333,18.483235294117648),
(54.30133333333333,18.50264705882353),
(54.30133333333333,18.522058823529413),
(54.30133333333333,18.541470588235295),
(54.30133333333333,18.560882352941178),
(54.30133333333333,18.58029411764706),
(54.30133333333333,18.59970588235294),
(54.30133333333333,18.61911764705882),
(54.30133333333333,18.638529411764704),
(54.30133333333333,18.657941176470587),
(54.30133333333333,18.67735294117647),
(54.30133333333333,18.69676470588235),
(54.30133333333333,18.716176470588234),
(54.30133333333333,18.735588235294117),
)

db = database.connect(SOURCE_DIR + DB_FILENAME)
cursor = db.cursor() 
lock = threading.Lock()


def beforeExit():
    try:
        database.close(cursor, db)
    except sqlite3.ProgrammingError:
        pass

atexit.register(beforeExit)

# https://stackoverflow.com/a/12997900
def calculateDerivedPosition(point, range, bearing):
        EarthRadius = 6371000

        latA = math.radians(point[0])
        lonA = math.radians(point[1])
        angularDistance = range / EarthRadius
        trueCourse = math.radians(bearing)

        lat = math.asin(
                math.sin(latA) * math.cos(angularDistance) +
                        math.cos(latA) * math.sin(angularDistance)
                        * math.cos(trueCourse))

        dlon = math.atan2(
                math.sin(trueCourse) * math.sin(angularDistance)
                        * math.cos(latA),
                math.cos(angularDistance) - math.sin(latA) * math.sin(lat))

        lon = ((lonA + dlon + math.pi) % (math.pi * 2)) - math.pi

        lat = math.degrees(lat)
        lon = math.degrees(lon)

        newPoint = (lat, lon)

        return newPoint

def getDistanceBetweenTwoPoints(p1, p2):
        R = 6371000 # earth radius
        dLat = math.radians(p2[0] - p1[0])
        dLon = math.radians(p2[1] - p1[1])
        lat1 = math.radians(p1[0])
        lat2 = math.radians(p2[0])

        a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(lat2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c

        return d

def pointIsInCircle(pointForCheck, center, radius):
        if (getDistanceBetweenTwoPoints(pointForCheck, center) <= radius):
            return True
        else:
            return False

# center: places are queried around center by radius
# radius: radius from center in meters
def queryPlacesWithinCategories(center, radius):
    mult = 1.1 # to be sure each place is considered
   
    # calculate rectangle which will be used to filter places 
    p1 = calculateDerivedPosition(center, mult * radius, 0) # top
    p2 = calculateDerivedPosition(center, mult * radius, 90); # right
    p3 = calculateDerivedPosition(center, mult * radius, 180); # down
    p4 = calculateDerivedPosition(center, mult * radius, 270); # left
 
    inRectangleCondition =  " WHERE " + \
        "lat" + " > " + str(p3[0]) + " AND " + \
        "lat" + " < " + str(p1[0]) + " AND " + \
        "lon" + " < " + str(p2[1]) + " AND " + \
        "lon" + " > " + str(p4[1])

    placesByCategories = {category: [] for category in CATEGORIES}
    for category in CATEGORIES:
        selectString = f"SELECT * FROM {category}" + inRectangleCondition

        try:
            lock.acquire(True)
            cursor.execute(selectString)
            rows = cursor.fetchall()
        finally:
            lock.release()

        placesWithDistance = [] 
        for row in rows:
            placeCoords = (row[0], row[1])
            distance = getDistanceBetweenTwoPoints(placeCoords, center)
            if distance < radius:
                placesWithDistance.append(row + (distance,)) # adding distance as last element of row
        
        placesByCategories[category] = sorted(placesWithDistance, key=lambda x: x[-1])

    return placesByCategories

def getPrecalculatedPoints(wages = {category: 1.0 for category in CATEGORIES}):
    results = []
    try:
        with open(SOURCE_DIR + RESULTS_FILENAME, 'r') as savedResults:
            results = json.load(savedResults)
    except FileNotFoundError:
        # calculate results
        for coords in PRECALCULATED_COORDS:
            placesWithinCategories = queryPlacesWithinCategories(coords, RADIUS)
            result = 0.0
            for category, places in placesWithinCategories.items():
                if len(places) > 0:
                    result += wages[category]
            results.append({"coordinates": coords[::-1], "value": result})

        with open(SOURCE_DIR + RESULTS_FILENAME, 'w') as saveResults:
            json.dump(results, saveResults)

    return results



def getPlacesAroundLocation(coords):
    placesAroundLocation = queryPlacesWithinCategories(coords, RADIUS)
    result = {
            "coordinates": coords, 
            "places": placesAroundLocation
             }
    return result


if __name__ == "__main__":
    # DIRTY TESTING
    # print(getDistanceBetweenTwoPoints((54.370892, 18.6132158), (54.3893330823781, 18.609979311308994)))

    # res = cursor.execute("SELECT name FROM sqlite_master")
    # print(cursor.fetchall())

    # x = queryPlacesWithinCategories((54.39014837271083, 18.52922941548349), 1000)
    # print(x)
    
    # print(getPrecalculatedPoints())

    # y = getPlacesAroundLocation((54.39014837271083, 18.52922941548349))
    # print(y)

    x = queryPlacesWithinCategories((54.39014837271083, 18.52922941548349), 1000)
    for y, z in x.items():
        print(y, z, end="\n\n")
    
    #print(getPrecalculatedPoints())
