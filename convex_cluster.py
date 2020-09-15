from scipy.spatial import ConvexHull
from hdbscan import HDBSCAN
import shapefile as shp
import pandas as pd
import numpy as np


def loadfile(file):
    """

    :param file:
    :return:
    """
    data = shp.Reader(file)
    proj = str(open(file.split('.')[0]+'.prj', 'r',encoding='utf-8').read())
    xy = [geo['geometry']['coordinates'] for geo in data.__geo_interface__['features']]
    return pd.DataFrame(xy, columns = ('x', 'y')), proj

def hdbscan_clustering(df,size):
    """

    :param df:
    :param size:
    :return:
    """
    cluster = HDBSCAN(min_cluster_size = size).fit(df)
    return cluster.labels_, cluster.probabilities_

def convex_hull(df):
    """

    :param df:
    :return:
    """
    rows = [df.iloc[i] for i in range(df.shape[0])]
    points = np.array([[r['x'], r['y']] for r in rows])
    hull = ConvexHull(points).vertices
    bound = [(x, y) for x, y in points[hull, :]]
    return bound+[bound[-1]]

def calculate_rows(data,prob):
    """

    :param data:
    :param prob:
    :return:
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

    :param output:
    :param proj:
    :return:
    """
    with open(output+'.prj', 'w+', encoding = 'utf-8') as prj:
        prj.write(proj)
        prj.close()

def create_shp(output,rows):
    """

    :param output:
    :param rows:
    :return:
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

    :param filename:
    :param output:
    :param size:
    :param prob:
    :return:
    """

    data, proj = loadfile(filename)
    data['label'], data['prob'] = hdbscan_clustering(data, size)
    rows = calculate_rows(data, prob)
    create_shp(output, rows)
    create_prj(output, proj)

    return data, pd.DataFrame(rows)

