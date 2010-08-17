function MMap(id, pointOfInterest, zoom) {
    this.drawnLines = {}
    this.drawnLinesIndex = 1
    this.markers = {}
    this.contentObjectToMarker = {}
    this.markersIndex = 1;
    this.selectedMarker = null;

    this.id = id;
    this.pointOfInterest = pointOfInterest;
    this.zoom = zoom;
    
    this.div = document.getElementById(id);
    this.gmap = new GMap2(this.div);
    self = this;
    this.gmap.enableRotation();
    GEvent.addListener(this.gmap, "load", function(){
        self.gmap.checkResize()
        self.onLoaded()
    });
    this.gmap.addControl(new GSmallMapControl());
    if(this.pointOfInterest){
        //this.gmap.setCenter(this.pointOfInterest, this.zoom);
        this.gmap.setCenter(this.pointOfInterest, zoom); 
    }else{
       this.gmap.setCenter(new GLatLng(32.54681317351516, -6.328125), 2); 
    }
    this.gmap.setMapType(G_HYBRID_MAP);
};


$.extend( MMap.prototype, {
    onLoaded: function(){
        
    },
    setZoom: function(zoom){
        this.gmap.setZoom(zoom);
    },
    getZoom: function(){
        return this.gmap.getZoom();
    },
    setCenter: function(center, zoom){
        this.gmap.setCenter(center, zoom)
    },
    getCenter: function(){
        return this.gmap.getCenter()
    },
    panTo: function(center){
        this.gmap.panTo(center)
    },
    addMapType: function(mapType){
        this.gmap.addMapType(mapType)
    },
    setMapType: function(mapType){
        this.gmap.setMapType(mapType)
    },
    
    showLoading: function(){
        $(this.div).parent().append(LOADING_STRING)
    },
    
    hideLoading: function(){
        $(this.div).parent().children("#loading").remove()
    },
    
    showMouseOverHover: function(location, data){
        if(this.mouseOverHover==null){
            this.mouseOverHover = new HTMLMarker(location,
            "<div class='mouse-over-overlay ui-corner-all "+data.additionalClass+"' style='opacity: 0; margin-bottom: 20px; left: "+data.offsetLeft+"px; bottom: "+data.offsetBottom+"px;'>"+data.html+"</div>")
            this.gmap.addOverlay(this.mouseOverHover)
            $(this.mouseOverHover.div).find(".mouse-over-overlay").animate({marginBottom: 0, opacity: 1}, 500)
        }
    },
    
    hideMouseOverHover: function(){
        self = this;
        if(this.mouseOverHover){
            $(this.mouseOverHover.div).find(".mouse-over-overlay").animate({marginBottom: 20, opacity: 0}, 500, function(){
                if(self.mouseOverHover){ //asyncronous...so double check
                    self.gmap.removeOverlay(self.mouseOverHover)
                    self.mouseOverHover = null;
                }
            })
        }
    },
    
    isMouseOverHover: function(event){
        if(this.mouseOverHover){
            var element = $(this.mouseOverHover.div).find(".mouse-over-overlay")
            var maxX = element.offset().left+element.width()+10;
            var maxY = element.offset().top+element.height()+30;
            var left = element.offset().left-10;
            var top = element.offset().top-10;
            //console.log("x: "+event.pageX+": y: "+event.pageY+", tl: "+top+" "+left+", br: "+maxY+" "+maxX);
            if(event.pageX>left&&
               event.pageX<maxX&&
               event.pageY>top&&
               event.pageY<maxY){
                return true
            }else{
                return false;
            }
        }
    },
    
    startDrawingLine: function(callbackOnFinish){
        this.stopEditingLine();
        var line = new GPolyline([], "#ebf000", 2, 1);
        this.drawnLines[this.drawnLinesIndex] = line;
        this.gmap.addOverlay(line);
        line.enableDrawing();
        GEvent.addListener(line, "endline", function(){
            if(callbackOnFinish){
                callbackOnFinish();
            }
            storeLine(line, function(lineReply){
                line.id = lineReply.id;
                updateLineEditingArea();
            });
            line.disableEditing();
            redrawLineList()
        })
        updateLineEditingArea();
        addLineToList(this.drawnLinesIndex)
        this.drawnLinesIndex++;
    },

    getDimensionsOnScreen: function(polyline){
        var bounds = polyline.getBounds();
        if(bounds){
            var southwest = maptales.map.gmap.fromLatLngToDivPixel(bounds.getSouthWest())
            var northeast = maptales.map.gmap.fromLatLngToDivPixel(bounds.getNorthEast())
            var width = northeast.x-southwest.x;
            var height = southwest.y-northeast.y;
            return {height: height, width: width};
        }else{
            return {height: 0, width: 0};
        }
    },

    getLine: function(index){
        return this.drawnLines[index]
    },
    
    editLine: function(index){
        this.editedLineIndex = index;
        this.drawnLines[index].enableEditing()
        //GEvent.addListener(this.drawnLines[index].getPolyline(), "lineupdated", function(){
            //redrawLineList()
        //})
    },
    
    stopEditingLine: function(){
        getEditedLine().disableEditing()
        redrawLineList()
    },
    
    getEditedLine: function(){
        return this.drawnLines[this.editedLineIndex]
    },

    getLastLine: function(){
        return this.drawnLines[this.drawnLinesIndex]
    },
    
    getNumLines: function(){
        return this.drawnLinesIndex
    },

    placeGeoJsonTrack: function(track){
        for (segment in track.segments){
            this.placeGeoJsonSegment(track.segments[segment])
        }
    },

    placeGeoJsonSegment: function(segment){
        var points = [];
        var coordinates = segment.track.coordinates;
        for(var i=0; i<coordinates.length; i++){
           points[i] = new GLatLng(coordinates[i][1], coordinates[i][0])
        }
        segment.title = "Line "+this.drawnLinesIndex;
        var line = new MPolyline(points, "#ff0000", 5, segment);
        this.addLine(line)
        addLineToList(this.drawnLinesIndex-1)
    },

    addLine: function(line){
        this.drawnLines[this.drawnLinesIndex] = line;
        this.drawnLinesIndex++;
        this.gmap.addOverlay(line);
    },

    placeGeoJsonMarker: function(geojsonitem, draggable){
        var location = geojsonitem.location
        if(location && location.coordinates){
            var marker = new MMarker(new GLatLng(location.coordinates[1], location.coordinates[0]), geojsonitem, draggable)
            this.addMarker(marker)
        }
    },

    placePosition: function(objectId, contentType, latlng){
        marker = new MMarker(latlng, {}, true)
        this.addMarker(marker);
        return marker;
    },
    
    placeCluster: function(data){
        
        if(data){
            cluster = new MCluster(data)
            this.addCluster(cluster);
            return cluster;
        }
        return true;
    },
    
    dumpData: function(){
        var bounds = this.gmap.getBounds()
        return {zoom:this.gmap.getZoom(),
                x1:bounds.getSouthWest().lng(),
                y1:bounds.getSouthWest().lat(),
                x2:bounds.getNorthEast().lng(),
                y2:bounds.getNorthEast().lat()
            }    
    },
    
    addCluster: function(cluster){
        this.gmap.addOverlay(cluster);
    },
    
    addMarker: function(marker){
        this.markers[this.markersIndex] = marker;
        this.markersIndex++;
        this.contentObjectToMarker[marker.originalData.type+"_"+marker.originalData.id] = marker;
        this.gmap.addOverlay(marker);
    },

    gotoContentObject: function(type, id){
        var marker = this.contentObjectToMarker[type+"_"+id]
        if(marker){
            this.gotoMarker(marker)
        }
    },
    
    selectContentObject: function(type, id){
        var marker = this.contentObjectToMarker[type+"_"+id]
        this.deselectContentObject()
        if(marker){
            marker.select()
            this.selectedMarker = marker;
        }
    },
    
    deselectContentObject: function(){
        if(this.selectedMarker){
            this.selectedMarker.deselect()
        }
    },
    
    
    gotoMarker: function(marker){
        if(false){
            var location = marker.getLatLng();
            var zoomLevel = this.gmap.getZoom();
            //this.gmap.setCenter(location, zoomLevel);
            var point = this.gmap.fromLatLngToDivPixel(location);
            point.x += 200;
            point.y -= 0;
            var offsetlocation = this.gmap.fromDivPixelToLatLng(point);
            this.gmap.panTo(offsetlocation);
            
        }else{
            this.gmap.panTo(marker.getLatLng())
        }
        
    },

    gotoMarkerIndex: function(index){
        if(this.markers[index]){
            this.gmap.panTo(this.markers[index].getLatLng())
        }
    },
    
    markerClick: function(marker){
        this.gmap.panTo(marker.getLatLng())
        this.onMarkerClick(marker)
    },
    
    onMarkerClick: function(marker){
        
    },

    zoomToShowAllOverlays: function(){
        var bounds = this.getBoundsOfAllOverlays()
        if(bounds){
            var zoom = this.gmap.getBoundsZoomLevel(bounds)
            if(zoom>13){
                zoom=13;
            }
            this.gmap.setCenter(bounds.getCenter(), zoom);
        }
    },
    
    gotoStorylineItem: function(index){
        var zoom = 16;
        this.setZoom(zoom)
        this.gotoMarkerIndex((index+1))
        this.selectMarker(index+1);
        //this.gotoContentObject($('#storyline_index_'+index).attr("contenttype"), $('#storyline_index_'+index).attr("objectid"))    
    },
    
    lastMarkerSelectIndex: null,
    selectMarker: function(index){
        if(this.lastMarkerSelectIndex){
            this.markers[this.lastMarkerSelectIndex].deselect()
        }
        this.markers[index].select()
        this.lastMarkerSelectIndex = index;
    },
    
    getZoomContainingAllOverlays: function(){
        var bounds = this.getBoundsOfAllOverlays()
        if(bounds){
            var zoom = this.gmap.getBoundsZoomLevel(bounds)
            return zoom;
        }
    },

    getBoundsOfAllOverlays: function(){
        var bounds = null;
        for(lineIndex in this.drawnLines){
            if(this.drawnLines[lineIndex]){
                var tempBounds = this.drawnLines[lineIndex].getPolyline().getBounds();
                if(bounds){
                   bounds.extend(tempBounds.getSouthWest())
                   bounds.extend(tempBounds.getNorthEast())
                }else{
                   bounds = tempBounds;
                }
            }
        }

       for(markerIndex in this.markers){
           if(this.markers[markerIndex]){
                var position = this.markers[markerIndex].location;
                if(bounds){
                   bounds.extend(position)
                }else{
                   bounds = new GLatLngBounds(position, position);
                }
           }
       }
        return bounds;
    },

    zoomToLine: function(index){
        bounds = this.drawnLines[index].getPolyline().getBounds();
        zoom = this.gmap.getBoundsZoomLevel(bounds)
        this.gmap.setCenter(bounds.getCenter(), zoom);
    },

    deleteLine: function(index){
        this.drawnLines[index].remove()
        delete this.drawnLines[index]
        $('#line_'+index)[0].parentNode.removeChild($('#line_'+index)[0])
    },

    stopEditingLine: function(){
        if (this.drawnLines[this.drawnLinesIndex-1]){
            this.drawnLines[this.drawnLinesIndex-1].disableEditing();
        }
    },

    checkResize: function(){
        this.gmap.checkResize()

    },

    initialResize: function(){
       this.checkResize()
       if(this.pointOfInterest){
            //this.gmap.setCenter(this.pointOfInterest, this.gmap.getZoom())
       }
    }
})