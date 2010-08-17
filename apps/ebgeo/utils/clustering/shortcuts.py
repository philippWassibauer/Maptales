from ebgeo.utils import clustering

def cluster_all_geoitems(qs, zoom, radius=32):
    return clustering.cluster_by_zoom(
        dict([(ni, (ni.bbox.extent[0], ni.bbox.extent[1]))
              for ni in qs if ni.bbox]), radius, zoom)
