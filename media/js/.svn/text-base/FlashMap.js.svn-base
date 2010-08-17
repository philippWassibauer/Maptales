function FlashMap(id, swfFile, pointOfInterest, zoom, parameters) {
	if(!parameters)parameters = {}
	parameters.debug = true;
    this.id = id;
    $('#'+id).flash(
        {
			src: swfFile+"?debug=true&version=123",
			debug: true,
			name: id,
			width: "100%",
			height: "100%",
			wmode: "opaque",
			flashvars: parameters
		}, 
        { expressInstall: true }
    );
};


$.extend( FlashMap.prototype, {
    
    setZoom: function(zoom){
        
    },
    getZoom: function(){
        
    },
    setCenter: function(center, zoom){
        
    },
    getCenter: function(){
        
    },
    panTo: function(center){
        
    },
    addMapType: function(mapType){
        
    },
    setMapType: function(mapType){
        
    },
	
	gotoStorylineItem: function(index){
		try{
			this.getFlexApp(this.id).gotoPosition(index);
		}catch(e){
			//alert(e)
		}
	},
    
    gotoPosition: function(index){
		try{
			this.getFlexApp(this.id).gotoPosition(index);
		}catch(e){
			//alert(e)
		}
	},
	
	getFlexApp: function()
	{
	  if (navigator.appName.indexOf ("Microsoft") !=-1)
	  {
	    return window[this.id];
	  }
	  else
	  {
	    return document[this.id];
	  }
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
           points[i] = [coordinates[i][1], coordinates[i][0]]
        }
        try{
			this.getFlexApp(this.id).addPolyline(points)
		}catch(e){
			//alert(e)
		}
    },

    addLine: function(line){
        this.drawnLines[this.drawnLinesIndex] = line;
        this.drawnLinesIndex++;
        this.gmap.addOverlay(line);
    },

    placeGeoJsonMarker: function(geojsonitem, draggable){
        var location = geojsonitem.location
        if(location && location.coordinates){
            this.addMarker(location.coordinates[1], location.coordinates[0], geojsonitem)
        }
    },

    addMarker: function(lat, lng, data){
		try{
			this.getFlexApp(this.id).addMarker(lat, lng)
		}catch(e){
			//alert(e)
		}
    },

    gotoContentObject: function(type, id){
		try{
			this.getFlexApp(this.id).addMarker(marker)
		}catch(e){
			//alert(e)
		}
    },
    
    selectContentObject: function(type, id){
		try{
			this.getFlexApp(this.id).addMarker(marker)
		}catch(e){
			//alert(e)
		}
    },
    
    deselectContentObject: function(){
		try{
			this.getFlexApp(this.id).addMarker(marker)
		}catch(e){
			//alert(e)
		}
    },
    
    
    gotoMarker: function(marker){
        this.gmap.panTo(marker.getLatLng())
    },

    gotoMarkerIndex: function(index){
        
    },
    
    markerClick: function(marker){
        
    },
    
    onMarkerClick: function(marker){
        
    },

    zoomToShowAllOverlays: function(){
		try{
			 this.getFlexApp(this.id).zoomToShowAllOverlays()
		}catch(e){
			
		}
    },

    zoomToLine: function(index){
        
    },

    checkResize: function(){
        //this.gmap.checkResize()
    }
})