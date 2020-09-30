from scipy.spatial import ConvexHull
from hdbscan import HDBSCAN
import shapefile as shp
import pandas as pd
import numpy as np


def loadfile(file):
    """
    load the shapefile and convert the coordinates to new dataframe
    :param file: path to the shapefile
    :return: xy-dataframe and the spatial projection
    """
    data = shp.Reader(file)
    proj = str(open(file.split('.')[0]+'.prj', 'r',encoding='utf-8').read())
    xy = [geo['geometry']['coordinates'] for geo in data.__geo_interface__['features']]
    return pd.DataFrame(xy, columns = ('x', 'y')), proj

def hdbscan_clustering(df,size):
    """
    perform the HDBSCAN clustering proccess
    :param df: input xy-dataframe
    :param size: min_cluster_size for the clustering algorithm
    :return: clustering label and clustering probabilities
    """
    cluster = HDBSCAN(min_cluster_size = size).fit(df)
    return cluster.labels_, cluster.probabilities_

def convex_hull(df):
    """
    create convex hull boundary
    :param df: input xy-dataframe
    :return: convex hull coordinates boundary
    """
    rows = [df.iloc[i] for i in range(df.shape[0])]
    points = np.array([[r['x'], r['y']] for r in rows])
    hull = ConvexHull(points).vertices
    bound = [(x, y) for x, y in points[hull, :]]
    return bound+[bound[0]]

def calculate_rows(data,prob):
    """
    define the values cluster boundaries
    :param data: input dataframe
    :param prob: probability threshold
    :return: list of dictionaries,
    each one of them contain the data of specific boundary
    """
    prob = abs(prob%1) if prob>1 or prob<0 else prob
    cls, rows = np.unique(data['label']), []
    for i in cls[cls > -1]:
        df = data[(data['label'] == i) & (data['prob'] > prob)]
        length = df.shape[0]
        geo = convex_hull(df)
        rows.append({'name': 'cluster_' + str(i + 1),
                     'id': i+1,
                     'count': length,
                     'center_x': sum(df['x']) / length,
                     'center_y': sum(df['y']) / length,
                     'geometry': geo})
    return rows

def create_prj(output,proj):
    """
    create Geographic Coordinate System file (.prj)
    :param output: output filename
    :param proj: input prj of the original file
    """
    with open(output+'.prj', 'w+', encoding = 'utf-8') as prj:
        prj.write(proj)
        prj.close()

def create_shp(output,rows):
    """
    create output shapefile
    :param output: output filename
    :param rows: list of record to create the SHP
    """
    layer = shp.Writer(output)
    layer.field('name', 'C', 30)
    layer.field('id', 'N')
    layer.field('count', 'N')
    layer.field('center_x', 'N', decimal = 6)
    layer.field('center_y', 'N', decimal = 6)
    for row in rows:
        layer.poly([row['geometry']])
        layer.record(row['name'], row['id'], row['count'], row['center_x'], row['center_y'])
    layer.close()

def convex_cluster(filename, output, size, prob=0):
    """
    Defines a boundary around cluster centers in a given point shapefile.
    :param filename: the given shapefile path
    :param output: name for the output shapefile
    :param size: min_cluster_size value for HDBSCAN clustering
    :param prob: probability threshold for boundary (default: 0)
    :return: original points df, output shape df
    """

    data, proj = loadfile(filename)
    data['label'], data['prob'] = hdbscan_clustering(data, size)
    rows = calculate_rows(data, prob)
    create_shp(output, rows)
    create_prj(output, proj)

    return data, pd.DataFrame(rows)

