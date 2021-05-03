# Spatial Data Analysis for NanoString-GeoMx-Digital-Spatial-Profiler 
This project was initiated as the part of the competition hosted by Nanostring(https://nanostring.devpost.com/). Spatial transcriptomics has already proved to be a powerful method to profile gene expression across tissue sections  without loss of spatial information. This technology reveals the complex composition of cellular structures and previously undervalued heterogeneity of tissues. Unlike conventional RNA-seq methods spatial transcriptomics technologies, e.g. NanoString Digital Spatial Profiler, results in much more data that should be aggregated and analysed together to gain deeper insights about biological processes.

Our approach makes use of spatial features extracted from the IF images by the pre-trained neural network resnet50 and the ssGSEA enrichment scores. ssGSEA can be considered as the procedure for dimension reduction of gene expression data that successfully keeps biologically meaningful information about molecular processes in specific tissue regions. The neural network results in more than 2,000 features that are redundant and require some filtering. We decided to filter special features by coefficient of variation, as the most variable features should represent the heterogeneity of tissue and the difference between DKD and healthy samples. The selected spatial features made us able to map the correlated enriched gene sets onto the image and to see the tissue regions with elevated activity of specific biological processes.

![application](https://user-images.githubusercontent.com/5582809/116894905-50555f00-ac52-11eb-9ac4-f74ec2cc82cc.png)
## Team Member
* Anna Valyaeva
* Daniel Last(https://github.com/D-A-C-S)
* Theressa Lalanne(https://github.com/Tlalanne)
* Shashi Gharti(https://github.com/shashigharti)

## How to use the application
### First Georeference IF images and serve images as tiles (Image Server)
To georeference and service the IF images we have used terracota server.

Link: https://github.com/shashigharti/NanostringVisualizations/tree/main/TilesServer

### Install flask server to serve interactive plots using bokeh library (Plot Server)
We used flask server to serve the bokeh plots as html file.

Link: https://github.com/shashigharti/NanostringVisualizations/tree/main/DKD-VIZ/backend

### Frontend (Reactjs and Leaflet)
We used reactjs and leaflet to load and display the images and plots. 

Link: https://github.com/shashigharti/NanostringVisualizations/tree/main/DKD-VIZ/frontend



