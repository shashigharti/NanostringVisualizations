import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash
from dash.dependencies import Input, Output, State

from data import available_datasets,TerraScan,df_to_anndata
import figures

attribution = 'Nanostring DSP'
base_url = "https://scantilesserver.herokuapp.com"

##Raster data
print("Loading inmunofluorescence raster data")
datasets_ids = available_datasets(base_url)
datasets = {data_id:TerraScan(base_url,data_id) for data_id in datasets_ids}

##Gene expression data
print("Loading gene expression data")
#ROIS annotations
rois_df = pd.read_csv("GeneExpressionData/sample_anotations.txt",sep='\t')
rois_df = rois_df.loc[:,'SlideName':'NormalizationFactor']
rois_df = rois_df.set_index("SegmentDisplayName")

#Raw gene count
gene_raw_count_df = pd.read_csv("GeneExpressionData/Kidney_Raw_TargetCountMatrix.txt",sep='\t')
gene_raw_count_df = gene_raw_count_df.set_index("TargetName").T

adata = df_to_anndata(gene_raw_count_df,rois_df)

#Precomputed figures:
#Volcano
volcano_figure = figures.volcano_plot(adata)

map_preview = dbc.Card([
                dcc.Graph(id='preview-graph',config = {'displayModeBar': False})
                ],className='col-md-5')

map_dropdown =  dbc.Card([
                    dbc.FormGroup([
                        dbc.Label("Tissue slice id",className='card-header'),
                        dbc.Select(
                                id='map-dropdown',
                                options=[{'label': scan_id, 'value': scan_id} 
                                           for scan_id,_ in datasets.items()],
                                value=list(datasets.keys())[0]),
                    ]),
                    dbc.Tabs(
                        id='aggregation-tab',
                        active_tab='global',
                        children=[
                                dbc.Tab(label="Global", tab_id="global"),
                                dbc.Tab(label="ROI", tab_id="roi")
                    ])
                ],className='col-md-7')
    
top_right = html.Div([map_preview,map_dropdown],className='row')

# Layout
app = dash.Dash(external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server
app.layout = html.Div([
    
    #Left
    html.Div([
        dl.Map(id='map',zoom=11,minZoom=6,
               style={'width': '100%', 'height': '100vh'}
              ),
    ],className='col-md-8'),
    
    #Right
    html.Div([
        top_right,
        html.Br(),
        html.Div(id='tab-content')
        ],className='col-md-4'),
    
    ],className='row')

@app.callback(
    [Output(component_id='map', component_property='children'),
     Output(component_id='map', component_property='center'),
     Output(component_id='preview-graph',component_property='figure')],
    Input(component_id='map-dropdown', component_property='value')
)
def switch_scan(scan_id):
    scan = datasets[scan_id]
    
    children = [dl.TileLayer(url=scan.png_tile, maxZoom=20, attribution=attribution)]
    x0,y0,x1,y1 = scan.metadata["bounds"]
    center = ( (y1-y0)/2 , (x1-x0)/2 )
    
    #Update map preview
    fig = figures.map_scatter_nav(scan.preview)
    
    return children,center,fig

@app.callback(
    Output('tab-content', 'children'),
    Input('aggregation-tab', 'active_tab'))
def switch_tabs(tab_value):

    if tab_value=='roi':
        return "Selected ROI"

    if tab_value=='global':
        volcano =  dcc.Graph(figure=volcano_figure,
                             config = {'displayModeBar': False},
                             style = {'width': '100%','height':'60vh'})
        return volcano
    

@app.callback(
    [Output('map', 'center'),
    Output('map','zoom')],
    Input('preview-graph', 'clickData'),
    State('map-dropdown','value'))
def navigate_scatter(clickData,scan_id):
    if not clickData:
        return dash.no_update
    
    lon0,lat0,lon1,lat1 = datasets[scan_id].metadata["bounds"]
    lon_range = lon1-lon0
    lat_range = lat1-lat0
    
    coordinates = clickData["points"][0]
    x,y = coordinates["x"],coordinates["y"]
    lon = (x/128)*lon_range
    lat = (y/128)*lat_range
    center = (lat,lon)
    zoom = 14
    return center,zoom


if __name__ == '__main__':
    app.run_server()
