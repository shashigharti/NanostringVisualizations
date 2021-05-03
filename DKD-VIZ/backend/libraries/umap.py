from math import pi
import pandas as pd
import numpy as np

import os, json
from sklearn.decomposition import PCA
import plotly.express as px

from bokeh.models import Legend, LegendItem, HoverTool, TapTool
from bokeh.resources import CDN
from bokeh.transform import factor_cmap, factor_mark
from bokeh.embed import json_item, file_html
from bokeh.plotting import figure
from bokeh.palettes import Category10_3
from bokeh.io import show
from bokeh.palettes import magma
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.embed import components
from flask import Flask, render_template
from bokeh.events import Tap
from pyproj import Transformer
import umap


def pixel_to_latlng(x, y):
    transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
    pxToMeter = 10  # Constanpixel_to_latlngt,defined when preprocessing the TIF image
    x_coord = x  # Variable, your coordinates in pixel units
    y_coord = y  # Variable, your coordinates in pixel units
    lon, lat = transformer.transform(x_coord * pxToMeter, y_coord * pxToMeter)
    return ("{},{}").format(lat, lon)


def process_data_for_umap():
    spatial_count = pd.read_csv("libraries/data/ROI_spatial_features_pretrained.csv")
    gene_count = pd.read_csv(
        "libraries/data/Kidney_Raw_TargetCountMatrix.txt", delimiter="\t"
    )
    roi_meta = pd.read_csv("libraries/data/Kidney_Sample_Annotations.csv")

    gene_count = gene_count.set_index("TargetName").T.reset_index()
    gene_count["ROI"] = (
        gene_count["index"].str.split("|").apply(lambda p: "-".join(p[:-1])).str.strip()
        + ".png"
    )

    # Aggregate gene count for biomarkers in same roi
    gene_count = gene_count.groupby("ROI").sum().reset_index()

    # Normalization as each ROI had the same total amount of genes count
    gene_count = (
        gene_count.set_index("ROI")
        .apply(lambda p: p * 10000 / p.sum(), axis=1)
        .reset_index()
    )

    # Roi_metadata
    roi_meta["ROI"] = (
        roi_meta["SegmentDisplayName"]
        .str.split("|")
        .apply(lambda p: "-".join(p[:-1]))
        .str.strip()
        + ".png"
    )
    # roi_meta = roi_meta.groupby("ROI").disease_status.first()
    roi_meta = roi_meta.groupby("ROI").agg(
        {
            "disease_status": "first",
            "region": "first",
            "RoiReportX": "first",
            "RoiReportY": "first",
        }
    )
    roi_meta["coordinates"] = roi_meta.apply(
        lambda row: pixel_to_latlng(row["RoiReportX"], row["RoiReportY"]), axis=1
    )
    roi_meta = roi_meta.drop(["RoiReportX", "RoiReportY"], axis=1)

    all_features = pd.merge(
        gene_count.set_index("ROI").T.sample(10000).T,
        spatial_count.set_index("ROI").T.sample(2000).T,
        left_index=True,
        right_index=True,
    )

    all_features /= all_features.to_numpy().max()
    pca_reducer = PCA(n_components=50)
    umap_reducer = umap.UMAP()

    low_dim = pca_reducer.fit_transform(all_features)
    low_dim = umap_reducer.fit_transform(low_dim)

    low_df = pd.DataFrame(data=low_dim, columns=["x", "y"])
    low_df = low_df.set_index(all_features.index)

    df = low_df.merge(roi_meta, left_index=True, right_index=True)
    df.to_csv(r"libraries/data/tmp/umap.csv", index=True, header=True)
    return df


def umap_plot():
    if os.path.exists(r"libraries/data/tmp/umap.csv"):
        df = pd.read_csv(r"libraries/data/tmp/umap.csv")
        print("Reading file")
    else:
        df = process_data_for_umap()
    colors = list(Category10_3)[:-1]
    disease_status = ["DKD", "normal"]
    markers = ["x", "circle"]
    region = ["glomerulus", "tubule"]

    source = ColumnDataSource(df)
    on_change = CustomJS(
        args=dict(source=source),
        code="""
        var inds = source.selected.indices;
        var all_images = ['disease1B', 'disease2B', 'disease3', 'disease4', 'normal2B', 'normal3', 'normal4'];
       
        var selected_values = [];
        for (var i = 0; i < inds.length; i++) {
            var coordinates = source.data['coordinates'][i].split(",");
            var roi = source.data['ROI'][i].split("_");
            var str = `${roi[0]},${coordinates[0]},${coordinates[1]}`;
            selected_values.push(str);  
        }
        var response = {'images':all_images,'selected_values':selected_values};
        window.top.postMessage(response,'*'); 
        """,
    )

    tooltips = [
        ("index", "$index"),
        ("(x,y)", "($x, $y)"),
        ("disease_status", "@disease_status"),
        ("region", "@region"),
        ("(lng,lat)", "@coordinates"),
    ]

    p = figure(
        plot_width=700,
        plot_height=600,
        tools="hover, tap, pan, box_select, box_zoom, reset",
        title="DKD vs Normal",
        tooltips=tooltips,
        toolbar_location="above",
    )
    r = p.scatter(
        "x",
        "y",
        source=source,
        fill_alpha=0.4,
        size=12,
        marker=factor_mark("region", markers, region),
        color=factor_cmap("disease_status", colors, disease_status),
    )

    p.xaxis.axis_label = "x"
    p.yaxis.axis_label = "y"

    # we are going to add "dummy" renderers for the legends, restrict auto-ranging
    # to only the "real" renderer above
    p.x_range.renderers = [r]
    p.y_range.renderers = [r]

    # create an invisible renderer to drive color legend
    rc = p.rect(x=0, y=0, height=1, width=1, color=colors)
    rc.visible = False

    # add a color legend with explicit index, set labels to fit your need
    legend = Legend(
        items=[
            LegendItem(label=disease_status[i], renderers=[rc], index=i)
            for i, c in enumerate(colors)
        ],
        location="top_right",
    )
    p.add_layout(legend)
    # create an invisible renderer to drive shape legend
    rs = p.scatter(x=0, y=0, color="grey", marker=markers)
    rs.visible = False

    # add a shape legend with explicit index, set labels to fit your needs
    legend = Legend(
        items=[
            LegendItem(label=region[i], renderers=[rs], index=i)
            for i, s in enumerate(markers)
        ],
        location="top_left",
    )
    p.add_layout(legend)
    source.selected.js_on_change("indices", on_change)

    script, div = components(p)
    return render_template(
        "plot.html", title="DKD vs Normal(Umap)", script=script, div=div
    )
