import pandas as pd
import tablemaster as tm
import re

def sku_get_brand(sku):
    return sku[:2]

def sku_get_model(sku):
    return sku.split("-")[1]

def sku_get_sku_code(sku):
    return sku.split("-")[1][:2]

def sku_get_product_line(sku, map_sku_code):
    sku_code = sku_get_sku_code(sku)
    try:
        product_line = map_sku_code.loc[map_sku_code['code']==sku_code, 'product_line'].iloc[0]
    except:
        product_line = ""
        print(f'product line of {sku} not found, please update!')
    return product_line

def sku_get_product_type(sku, map_sku_code):
    sku_code = sku_get_sku_code(sku)
    try:
        product_type = map_sku_code.loc[map_sku_code['code']==sku_code, 'product_type'].iloc[0]
    except:
        product_type = ""
        print(f'product line of {sku} not found, please update!')
    return product_type

def sku_get_scu(sku, map_scu):
    if(sku in map_scu['SKU'].astype(str).to_list()):
        scu = map_scu.loc[map_scu['SKU']==sku, 'SCU'].iloc[0]
    else:
        scu = sku_get_model(sku)
    return scu

def sku_get_app_product(sku, map_app_product):
    if(sku in map_app_product['Smart Products List'].astype(str).to_list()):
        return "Y"
    else:
        return "N"
    
def sku_get_series(sku, map_series):
    model = sku_get_model(sku)
    try:
        series = map_series.loc[map_series['Model']==model, 'Series'].iloc[0]
    except:
        series = ""
        print(f'series of {sku} not found, please update!')
    return series

def get_sku_extra(df_ori, list):
    df = df_ori.copy()
    print('loading mapping info...')
    if "product_line" in list or "product_type" in list :
        df_map_sku_code = tm.gs_read_df(('Datalibro Mapping Master', 'sku_code'))
        if "product_line" in list:
            df["product_line"] = df['sku'].apply(sku_get_product_line, map_sku_code = df_map_sku_code)
        if "product_type" in list:
            df["product_type"] = df['sku'].apply(sku_get_product_type, map_sku_code = df_map_sku_code)
    if "scu" in list:
        df_map_scu = tm.gs_read_df(('Datalibro Mapping Master', 'scu'))
        df['scu'] = df['sku'].apply(sku_get_scu, map_scu=df_map_scu)
    if "app_supported" in list:
        df_map_app_product = tm.gs_read_df(('Datalibro Mapping Master', 'app_product'))
        df['app_supported'] = df['sku'].apply(sku_get_app_product, map_app_product=df_map_app_product)
    if "series" in list:
        df_map_series = tm.gs_read_df(('Datalibro Mapping Master', 'series'))
        df['series'] = df['sku'].apply(sku_get_series, map_series=df_map_series)
    if "brand" in list:
        df['brand'] = df['sku'].apply(sku_get_brand)
    if "model" in list:
        df['model'] = df['sku'].apply(sku_get_model)
    if "sku_code" in list:
        df['sku_code'] = df['sku'].apply(sku_get_sku_code)
    return df
