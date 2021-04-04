import requests
import io

import numpy as np
import pandas as pd
from PIL import Image
import scanpy as sc
from anndata import AnnData

##Raster data
def available_datasets(base_url):
    """
    Lists available urls to requests different scans
    input: root url pointing to the scan tiles provider
    output: datasets ids
    """    
    band_key = "band_id"
    response = requests.get(base_url+"/datasets") 
    
    datasets = response.json()["datasets"]
    datasets_df = pd.DataFrame.from_dict(datasets).drop(columns=band_key).drop_duplicates()
    datasets_ids = datasets_df.apply(lambda p:"/".join(p),axis=1)
    
    return datasets_ids

class TerraScan():
    "Manages requests to terracotta tiles server"
    def __init__(self,base_url,scan_id):
        
        self.scan_id = scan_id
        self.base_url = base_url
        self.rgb_suffix ="/{z}/{x}/{y}.png?r=band2&g=band1&b=band0"
        self.metadata = self._get_metadata()
        self.preview = self._get_preview()
    
    def _get_metadata(self):
        url = self.base_url+"/metadata/"+self.scan_id+"/band0"
        response = requests.get(url).json()
        return response
    
    def _get_preview(self):
        url = self.base_url+"/singleband/"+self.scan_id+"/band0/preview.png?tile_size=[128,128]"
        bytes_image = requests.get(url).content
        image = Image.open(io.BytesIO(bytes_image))
        return image
    
    @property
    def png_tile(self):
        url = self.base_url+"/rgb/"+self.scan_id+self.rgb_suffix
        return url
    def __repr__(self):
        return f"TerraScan({self.scan_id})"

##Gene expression data
def df_to_anndata(gene_raw_count_df,rois_df):
    """
    gene_raw_count_df:
        index: observation id
        columns: genes id
    rois_df:
        index:observation id
        columns: observation features
    """

    first_gene_id = gene_raw_count_df.columns[0]
    last_roi_var = rois_df.columns[-1]

    formated_data = pd.merge(rois_df,gene_raw_count_df,
                             left_index=True,right_index=True)

    #Matrix of observation*variables--ROI*gene
    X = formated_data.loc[:,first_gene_id:].to_numpy()

    #DataFrame indexed by genes id
    var = list(formated_data.head(1).loc[:,first_gene_id:].columns)
    var = pd.DataFrame(index=var)

    #DataFrame indexed by observations(ROI) identifiers
    obs = formated_data.loc[:,:last_roi_var]

    #Packaged data
    adata = AnnData(X,var=var,obs=obs)
    return adata

def rank_genes(adata,groupby=None,treat=None,n_samples=500):
    """
    input: anndata object
    """
    #Normalizing inside each roi
    sc.pp.normalize_total(adata, target_sum=1e4)
    #Natural log
    sc.pp.log1p(adata)
    
    #Hypothesis testing, samples: rois, control:normal,treat:dkd
    sc.tl.rank_genes_groups(adata,groupby=groupby,method='wilcoxon')
    
    #Formats conversion
    ranked_genes = pd.DataFrame()
    for var in ['pvals_adj','logfoldchanges','names']:
        ranked_genes[var] = adata.uns['rank_genes_groups'][var][treat]

    ranked_genes["-log_padj"] = -np.log10(ranked_genes.pvals_adj)

    #Under-sampling low scored genes
    ranked_genes["hue"] = ranked_genes["-log_padj"]*ranked_genes["logfoldchanges"]
    ranked_genes["weights"] = ranked_genes.hue**2
    ranked_genes = ranked_genes.sample(n=n_samples,weights='weights')
    
    return ranked_genes