### Tile server

[Terracotta](https://terracotta-python.readthedocs.io/en/latest/)
*Python API based on flask to serve large images as tiles.*

### Running server
If innactive first request is slow due to wake up of heroku
URL: https://scantilesserver.herokuapp.com/apidoc

### Setup

* Put the images inside the folder ROI reports, only those with format {name}_scan.png will be processed and served.
* Convert,georeference and optimize the images: `source optimize.sh`

### Launch the tile server
```bash
source serve_tiles.sh
```

### Request tiles

#### Using terracotta test client
Launch the client
`source connect.sh`
Access the web demo app at `http://127.0.0.1:5100/`

#### Using an external client(ej: leaflet)

Configure your application to do requests in the following format: 
`http://127.0.0.1:5000/rgb/normal3/scan/{z}/{x}/{y}.png?r=band2&g=band1&b=band0`








