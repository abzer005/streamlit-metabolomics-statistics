import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.cluster.hierarchy import dendrogram, linkage
import plotly.figure_factory as ff


@st.cache_data
def order_df_for_heatmap(data):
    # SORT DATA TO CREATE HEATMAP

    # Compute linkage matrix from distances for hierarchical clustering
    linkage_data_ft = linkage(data, method="complete", metric="euclidean")
    linkage_data_samples = linkage(data.T, method="complete", metric="euclidean")

    # Create a dictionary of data structures computed to render the dendrogram.
    # We will use dict['leaves']
    cluster_samples = dendrogram(linkage_data_ft, no_plot=True)
    cluster_ft = dendrogram(linkage_data_samples, no_plot=True)

    # Create dataframe with sorted samples
    ord_samp = data.copy()
    ord_samp.reset_index(inplace=True)
    ord_samp = ord_samp.reindex(cluster_samples["leaves"])
    ord_samp.rename(columns={"index": "Filename"}, inplace=True)
    ord_samp.set_index("Filename", inplace=True)

    # Create dataframe with sorted features
    ord_ft = ord_samp.T.reset_index()
    ord_ft = ord_ft.reindex(cluster_ft["leaves"])
    ord_ft.rename(columns={"index": "metabolite"}, inplace=True)
    ord_ft.set_index("metabolite", inplace=True)
    return ord_ft


@st.cache_resource
def get_dendrogram(data, label_pos="bottom"):
    fig = ff.create_dendrogram(data, labels=list(data.index))
    fig.update_layout(template="plotly_white")
    fig.update_xaxes(side=label_pos)
    return fig


@st.cache_resource
def get_heatmap(ord_ft):
    # Heatmap
    fig = px.imshow(
        ord_ft,
        y=list(ord_ft.index),
        x=list(ord_ft.columns),
        text_auto=True,
        aspect="auto",
        color_continuous_scale="PuOr_r",
        range_color=[-3, 3],
    )

    fig.update_layout(
        autosize=False, width=700, height=1200, xaxis_title="", yaxis_title=""
    )

    # fig.update_yaxes(visible=False)
    fig.update_xaxes(tickangle=35)
    return fig