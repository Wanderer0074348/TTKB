# Extracting Data
This repo is for recording the progress for creating a dataset for a set of latitudes and longitudes as described [here](https://drive.google.com/file/d/1QPhcLANBwB0gjdIHsv5ohU-mcAwClh9j/view?usp=sharing)

## Viz1.py
In this code, we are just visualising the Brazilian Amazon. We do this using a file called Limites_Amazonia_Legal_2022.shp, which I downloaded from [IBGE](https://www.ibge.gov.br/geociencias/organizacao-do-territorio/estrutura-territorial/15819-amazonia-legal.html), which is the primary provider for statistical and geographical information for Brazil. So in this code, we just print the head of the .shp file, the CRS(Coordinate Reference System) and we plot the points.

### Results:
```
NOME     AREA_KM2                                           geometry
0  Amazônia Legal  5015145.999  MULTIPOLYGON (((-45.61083 -1.27461, -45.60796 ...
````
As you can see. this file only consists of one value with the entire geometry of Brazilian Amazon

EPSG:4674  --->  This is the coordinaate reference system of the downloaded file, it basically tells geopandas how to associate the points in this file to actual places on earth.

![image](https://github.com/user-attachments/assets/0d89eca2-d79e-41e5-b603-495191f3c6de)


## Griddy.py
This file takes the entire map from the Limites_Amazonia_Legal_2022.shp file, and divides it into smaller box grids, each of area 36 sq.km (6000 m X 6000 m squares). It finally writes the new boxes to a file called amazon_grid.shp, which will be visualised in viz2.py. A total of 142401 boxes were generated.
To divide the file into grids of equal size (area = 36sq. km), we change the CRS from EPSG:4674 to EPSG:5880
Why are we reprojecting to EPSG:5880?
The original file was in A geographic CRS (EPSG:4674) where the coordinates are in decimal degrees. This makes the distance and area calculations non uniform and distorted. EPSG:5880 is a Brazilian equal area projection CRS (unit in metres), so if we say we want to travel 500 metres, it actually helps us travel 500 metres. The calculations become more accurate. It helps us build a perfectly regular grid in metric units. 


## viz2.py

same thing as viz1.py, prints the head and plots the points. The CRS is different here (EPSG:5880), as it was changed by the griddy.py file. 

### Results:
             NOME     AREA_KM2                                           geometry
0  Amazônia Legal  5015145.999  POLYGON ((2800536 9114218, 2800536 9108883.768...
1  Amazônia Legal  5015145.999  POLYGON ((2800536 9120218, 2800536 9114218, 27...
2  Amazônia Legal  5015145.999  POLYGON ((2800536 9120218, 2800238.293 9120218...
3  Amazônia Legal  5015145.999  POLYGON ((2800536 9132218, 2800536 9129555.408...
4  Amazônia Legal  5015145.999  POLYGON ((2800536 9132218, 2798766.37 9132218,...


![image](https://github.com/user-attachments/assets/6f881e5f-33e3-4908-94d9-9aabdcab4b95)


## finding_centroids.py

As the name describes, this code is for finding the centroids of each of the 142401 grids generated before. We will be extracting the data for these points. These points are stored into a new file called amazon_centroids.shp. Here, the coordinates are in EPSG:5880
I checked the crs of the tif files that I obtained from WorldClim (the ones I showed yall on meet - the world maps), it was EPSG:4326, which is actual latitudes and longitude format that we are aware of. So, I will be converting this new file into another one with coordinates in latitude and longitude form
