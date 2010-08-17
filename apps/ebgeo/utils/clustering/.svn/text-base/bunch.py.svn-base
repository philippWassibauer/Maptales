from django.template import Context, Template
from story.models import Story
from django.template.loader import render_to_string
        
class Bunch(object):
    """
    A bunch is a list of objects which knows its center point,
    determined as the average of its objects' points. It's a useful
    data structure for clustering.
    """
    __slots__ = ["objects", "center", "points", "overlay_html", "minx", "maxx", "miny", "maxy"]

    def __init__(self, obj, point):
        self.objects = []
        self.points = []
        self.center = (0, 0)
        self.overlay_html = ""
        self.minx = None
        self.miny = None
        self.maxy = None
        self.maxx = None
        self.add_obj(obj, point)

    def add_obj(self, obj, point):
        #try:
        #    if self.minx == None or self.minx > obj.bbox.centroid.x:
        #        self.minx = obj.bbox.centroid.x
        #    if self.maxx == None or self.maxx < obj.bbox.centroid.x:
        #        self.maxx = obj.bbox.centroid.x
        #    if self.miny == None or self.miny > obj.bbox.centroid.y:
        #        self.miny = obj.bbox.centroid.y
        #    if self.maxy == None or self.maxy < obj.bbox.centroid.y:
        #        self.maxy = obj.bbox.centroid.y
        #except:
        #    import pdb; pdb.set_trace()
        self.objects.append(obj)
        self.points.append(point)
        self.update_center(point)
    
    def size(self):
        return len(self.objects)
    
    def get_json(self):
        items = []
        try:
            for item in self.objects[:4]:
                items.append(item.downcast().get_geojson())
            items_string = "["+"], [".join(items)+"]"
            
            c = Context({"self": self, "items_string":items_string})
            t = Template("""{"type": "Cluster",\
                    "objects": "",\
                    "size": "{{self.size}}",\
                    "center": {"lat":{{self.y}}, "lng":{{self.x}} } }""")
            
            return t.render(c)
        except:
            print "Error"
    
    def get_data(self):
        return {
            "type": "Cluster",
            "objects": "",
            "size": self.size(),
            "html": self.html(),
            "overlay_html": self.get_overlay_html(),
            "center": {"lat":self.y, "lng":self.x}
        }
    
    def html(self):
        stories = Story.objects.nearby(self.x, self.y)[0:3]
        return render_to_string("geo/cluster_hover.html", {"stories":stories})
    
    def set_overlay_html(self, html):
        self.overlay_html = html
    
    def get_overlay_html(self):
        return self.overlay_html
    
    def update_center(self, point):
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        self.center = (sum(xs) * 1.0 / len(self.objects), sum(ys) * 1.0 / len(self.objects))

    def x(self):
        return self.center[0]
    x = property(x)

    def y(self):
        return self.center[1]
    y = property(y)
        
    def __repr__(self):
        objs = list.__repr__(self.objects[:3])
        if len(self.objects) > 3:
            objs = objs[:-1] + ", ...]"
        return u"<Bunch: %s, center: (%.3f, %.3f)>" % (objs, self.x, self.y)
