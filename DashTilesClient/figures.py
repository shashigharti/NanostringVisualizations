import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from data import rank_genes

__figures__ = ['map_scatter_nav','volcano_plot']

#Figure
def map_scatter_nav(preview):
    """
    Interactive preview of the map to ease navigation
    through clickable ROIS
    """
    #TODO:incorporate roi coordinates from data
    #currently scatter dots are randomly positioned

    # Create figure
    fig = go.Figure()
    x_dots = preview.width*np.random.rand(15)*0.8
    y_dots = preview.height*np.random.rand(15)*0.8
    # Add trace
    fig.add_trace(
        go.Scatter(x=x_dots, y=y_dots,mode='markers',
                  opacity=0.6,
                  hoverinfo='none',
                  marker=dict(color=np.random.randn(15),
                              colorscale='ylorbr',
                              line_width=1,
                              size=10))
    )

    # Add images
    fig.add_layout_image(
            dict(
                source=preview,
                xref="x",
                yref="y",
                x=0,
                y=preview.height,
                sizex=preview.width,
                sizey=preview.height,
                layer="below")
    )

    # Set templates

    fig.update_layout(
        template="plotly_white",
        autosize=False,
        height=preview.height,
        width=preview.width,
        margin=dict(r=0, l=0, b=0, t=0))
    fig.update_xaxes(showgrid=False,visible=False,range=[0, preview.width])
    fig.update_yaxes(showgrid=False,visible=False,range=[0, preview.height])

    return fig


#Figure
def volcano_plot(adata):
    ranked_genes = rank_genes(adata,groupby='disease_status',treat='DKD',n_samples=500)
    
    fig = px.scatter(
               ranked_genes,
               x='logfoldchanges',
               y="-log_padj",
               color='logfoldchanges',
               color_continuous_scale='IceFire',
               opacity=0.6,
               hover_name='names',
               hover_data={'hue':False,
                          'logfoldchanges':False,
                          '-log_padj':False},
              )
    fig.update(layout_coloraxis_showscale=False)
    fig.update_layout(
        autosize=True,
        margin=dict(r=20, l=20, b=0, t=0))
    return fig
