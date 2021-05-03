# Spatial Data Analysis for NanoString-GeoMx-Digital-Spatial-Profiler 
This project was initiated as the part of the competition hosted by Nanostring(https://nanostring.devpost.com/). Spatial transcriptomics has already proved to be a powerful method to profile gene expression across tissue sections  without loss of spatial information. This technology reveals the complex composition of cellular structures and previously undervalued heterogeneity of tissues. Unlike conventional RNA-seq methods spatial transcriptomics technologies, e.g. NanoString Digital Spatial Profiler, results in much more data that should be aggregated and analysed together to gain deeper insights about biological processes.

Our approach makes use of spatial features extracted from the IF images by the pre-trained neural network resnet50 and the ssGSEA enrichment scores. ssGSEA can be considered as the procedure for dimension reduction of gene expression data that successfully keeps biologically meaningful information about molecular processes in specific tissue regions. The neural network results in more than 2,000 features that are redundant and require some filtering. We decided to filter special features by coefficient of variation, as the most variable features should represent the heterogeneity of tissue and the difference between DKD and healthy samples. The selected spatial features made us able to map the correlated enriched gene sets onto the image and to see the tissue regions with elevated activity of specific biological processes.


## Team Member
Anna Valyaeva
Daniel Last
Theressa Lalanne
Shashi Gharti

## How to use the application
### First Georeference IF images and serve images as tiles (Map Server)
To georeference and service the IF images we have used terracota server.
Link:

### Install flask server to serve interactive plots using bokeh library (Plot Server)
The steps to install and run the flask server
Link: https://github.com/shashigharti/NanostringVisualizations/tree/main/DKD-VIZ/backend

### Frontend (Reactjs and Leaflet)
We used reactjs and leaflet to load and display the images and plots. 
Link: https://github.com/shashigharti/NanostringVisualizations/tree/main/DKD-VIZ/frontend



