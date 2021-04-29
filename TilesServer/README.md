### Tile server

[Terracotta](https://terracotta-python.readthedocs.io/en/latest/)
*Python API based on flask to serve large images as tiles.*

### Running server
If inactive first request is slow due to wake up of heroku
URL: https://scantilesserver.herokuapp.com/apidoc

### Setup

* Put the images inside the folder ROI reports, only those with format {name}_scan.png will be processed and served.
* Convert, georeference and optimize the images: `source optimize.sh`

The files are converted in 3 bands (0=>R, 1=>G, 2=>B separated images) and images are 
geotagged using (epsg:3857) CRS system(Reference: https://en.wikipedia.org/wiki/EPSG_Geodetic_Parameter_Dataset).

### Launch the tile server
```bash
source serve_local_tiles.sh
```
The tiles are served with above command and the api doc file can be referenced here:
https://scantilesserver.herokuapp.com/apidoc

### Request tiles

#### Using terracotta test client
Launch the client
`source connect.sh`
Access the web demo app at `http://127.0.0.1:5100/`

### Using an external client(e.g. leaflet)

Configure your application to do requests in the following format: 
`http://localhost:5000/rgb/disease1B/scan/{z}/{x}/{y}.png?r=band2&g=band1&b=band0`

Js code to link to the terracote server end point:

```
L.tileLayer('http://localhost:5000/rgb/disease1B/scan/{z}/{x}/{y}.png?r=band2&g=band1&b=band0', {
		attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
```
Center and zoom params

```
center = [0.5, 0.5], 
zoom = 11
```










