from pykml import parser
from shapely import LineString
import pandas as pd


with open('filename_input.kml') as f:
    doc = parser.parse(f)

root = doc.getroot()
folder = root.Document.Folder

linestrings = []

for pm in folder.Placemark:
    data = {'name': None, 'linestring': None}
    try:
        coords = pm.LineString.coordinates.text

        lat_lon = []
        coords = coords.replace('\n', '').replace('\t', '')
        for coord in coords.split(" "):  # split coordinates based on commas (excluding preceding 0's)
            if coord != "":
                lat = coord.split(",")[0]
                lon = coord.split(",")[1]
                lat = round(float(lat), 5)
                lon = round(float(lon), 5)
                lat_lon.append([lat, lon])

        data['name'] = pm.name
        ls = str(LineString(lat_lon))
        data['linestring'] = ls

    except Exception as e:
        data['linestring'] = str(e)

    linestrings.append(data)

df = pd.DataFrame(linestrings)
df.to_csv('filename_output.csv', sep=";")
