from ebgeo.maps.utils import get_resolution, lnglat_from_px, px_from_lnglat
from ebgeo.utils.clustering.cluster import buffer_cluster
from django.conf import settings

def cluster_by_zoom(objs, radius, zoom, extent=(-180, -90, 180, 90),
                     cluster_fn=buffer_cluster):
    """
    Required parameters:

        + objs: dict, keys to ID objects, values are point 2-tuples
        + radius: in pixels
        + scale: 'n' in '1/n', eg., 19200
    """
    scale = from_zoom_to_scale(zoom)
    resolution = get_resolution(scale)

    # Translate from lng/lat into coordinate system of the display.
    objs = dict([(k, px_from_lnglat(v, resolution, extent)) for k, v in objs.iteritems()])

    bunches = []
    for bunch in cluster_fn(objs, radius):
        # Translate back into lng/lat.
        bunch.center = lnglat_from_px(bunch.center, resolution, extent)
        bunches.append(bunch)

    return bunches

def cluster_scales(objs, radius, scales=settings.MAP_SCALES, extent=(-180, -90, 180, 90),
                   cluster_fn=buffer_cluster):
    return dict([(scale, cluster_by_scale(objs, radius, scale, extent, cluster_fn)) for scale in scales])

def from_zoom_to_scale(zoom):
    resolution = 2933 # approximate scale on 21 zoom
    return resolution*(2**(21-zoom))
    
