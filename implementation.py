from convex_cluster import convex_cluster


# example 1:
prob = 0.7
size = 63
filename = "layers\example_boston.shp"
output = 'output\output_boston'
convex_cluster(filename, output, size, prob)


# example 2:
prob = 0.8
size = 60
filename = "layers\example_dc.shp"
output = 'output\output_dc'
df, shp = convex_cluster(filename, output, size, prob)


# example 3:
prob = 0.75
size = 50
filename = "layers\example_nyc.shp"
output = 'output\output_nyc'
print(convex_cluster(filename, output, size, prob)[1])


