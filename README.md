# generate-Convex-Hull-SHP-from-HDBSCAN-clustering-probabilities
Defines a boundary around cluster centers in a given point-layer shapefile.

## introduction
When we want to make a division into clusters of geographical coordinates, we often get inaccurate results. This is because the clustering algorithm often assigns points to a some cluster that do not necessarily have to be associated with it. This outcome creates a situation in which it is more difficult to define the boundaries of the cluster. In order to create a solution to this gap, the code ["**convex_cluster.py**"](https://github.com/EtzionData/generate-Convex-Hull-SHP-from-HDBSCAN-clustering-probabilities/blob/master/convex_cluster.py) was developed.

The code receives in the first step a esri shapefile (**SHP**), and extracts the X and Y coordinates from it. Another information he produces from the SHP is the **Geographic Coordinate System** of the layer, which will be used to save the code output as a new SHP.

Based on the given coordinates, the code performs clustering using the **HDBSCAN** algorithm which returns two attributes to each point in space: **label** and **probability**. The label determines which cluster each point is associated with, and the probability defines each point belonging to its cluster. This data can be plot as a heat-map, such as in this example:

![probability](https://github.com/EtzionData/generate-Convex-Hull-SHP-from-HDBSCAN-clustering-probabilities/blob/master/Picture/example%20-%20cluster%20probability%20values.png)

As can be seen in the example, the closer a point is to the cluster center, the higher its probability, and closer to the value 1. In contrast, points farther from the center approach to 0. Every cluster can have a different density, based on its distribution characteristics. As you can see, different clusters can have a completely different density (the code used to generate the plot and documentation is available here: [**multi-smooth-density-plot**](https://github.com/EtzionData/create-multi-smooth-density-plot)):

![density](https://github.com/EtzionData/generate-Convex-Hull-SHP-from-HDBSCAN-clustering-probabilities/blob/master/Picture/example%20-%20smooth%20density%20of%20cluster%20probabilities.png)

Based on these data, we can choose a threshold condition (**"prob"**) from which only we selected to analyze points from the cluster. The code create a boundary around the choosen point using the **Convex Hull** algorithm. Now we get a polygon that defines the cluster boundaries, based on the threshold conditions we have defined. This ploygon focus the cluster boundary to the core so that they include only the point fit the defined threshold.

The all process can describe through using the following steps (for **prob=0.5**):

![steps](https://github.com/EtzionData/generate-Convex-Hull-SHP-from-HDBSCAN-clustering-probabilities/blob/master/Picture/steps.png)

As you can see, the cluster density take major rule in the definition of the boundary. It can be seen that **cluster 2** is so dense that its boundary is small and very focused. In contrast, **cluster 1** has a lower density, and therefore, its boundary is much larger and wider.

The boundary generated will be saved as a new SHP file. When we save the data, we will use the **Geographic Coordinate System** that we imported from the SHP file at the beginning of the process. In addition to the geographical boundary, we will add the following data to each row in the new layer:
-	The number of points belonging to the cluster according to the threshold conditions we set (**"count"**)
-	Coordinates of the cluster center (**"center_x"** and **"center_y"**)
-	Name and number of the cluster (**"id"** and **"name"**)

An example of one of the SHP file created using the code can be seen in the **Boston** area:

![Boston](https://github.com/EtzionData/generate-Convex-Hull-SHP-from-HDBSCAN-clustering-probabilities/blob/master/Picture/boston_example.jpg)

The code will returned the data about each of the original points as a new pandas dataframe, along with their probability and label data. In addition, the code will also return the records that composed the SHP that created, also as dataframe.

All the layers that used as examples in this repository, are also accessible: 

[**original layers**](https://github.com/EtzionData/generate-Convex-Hull-SHP-from-HDBSCAN-clustering-probabilities/tree/master/layers)

[**output layers**](https://github.com/EtzionData/generate-Convex-Hull-SHP-from-HDBSCAN-clustering-probabilities/tree/master/output)



## libraries
The code uses the following libraries in Python:

**shapefile**

**hdbscan**

**pandas**

**scipy**

**numpy**


## application
An application of the code is attached to this page under the name: 

[**"implementation.py"** ](https://github.com/EtzionData/generate-Convex-Hull-SHP-from-HDBSCAN-clustering-probabilities/blob/master/implementation.py)
the examples outputs are also attached here.

## example for using the code
To use this code, you just need to import it as follows:
``` sh
# import
from convex_cluster import convex_cluster

# define variables
filename = (r'path\file.shp')
output = 'outputname'
size = 63
prob = 0.7

# application
convex_cluster(filename, output, size, prob)
```

When the variables displayed are:

**filename:** the given shapefile path

**output:** name for the output shapefile

**size:** min_cluster_size value for HDBSCAN clustering 

**prob:** threshold condition for cluster probability value (default: 0, must be between 0 to 1)

## License
MIT © [Etzion Harari](https://github.com/EtzionData)


