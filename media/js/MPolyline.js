var lineCounter = 0;
function MPolyline(points, color, thickness, segment) {
    this.container = document.createElement("DIV");
    this.overlay_label = document.createElement("DIV");
    this.overlay_label.style.position="absolute"
    //this.overlay_label.style.display="none"
    this.infoContainer = document.createElement("span");
    this.number = lineCounter++;
    this.containerId = "lineInfoContainer"+this.number;
    if(!segment){
        segment = {}
    }
    this.timestamps = segment.timestamps || [];
    this.altitudes = segment.altitudes || [];
    this.title = segment.title || "Line"
    this.description = segment.description || "";
    this.id = segment.id;
    this.type = segment.type;
    this.parentId = segment.parent_id;
    this.strokeOpacity = 1;
    this.map = null;
    this.mainPolyline = new GPolyline(points, "#ebf000", 2, this.strokeOpacity);
    this.shadowPolyline = new GPolyline(points, "#000000", 5, 0.6);
    this.startMarker = new HTMLMarker(points[0], "<div class='line-start-marker'></div>");
    this.endMarker = new HTMLMarker(points[(points.length-1)], "<div class='line-end-marker'></div>");
    this.currentPositionMarker = new HTMLMarker(points[0], "<div class='line-mouse-position-marker'></div>");

    var self = this;
    GEvent.addListener(this.mainPolyline, "mouseover", function(glatlng) {
        //$(self.infoContainer).addClassName("over");
       // $(self.infoContainer).setOpacity(1);
        //create current position
        /*self.map.addOverlay(self.currentPositionMarker)

        $(document).mousemove(function(event){
            var y = event.pageY - $(self.overlay_label).parent().offset().top;
            var x = event.pageX - $(self.overlay_label).parent().offset().left;
            $(self.overlay_label).css("top", y)
            $(self.overlay_label).css("left", x)

            var x = event.pageX - $("#map_canvas")[0].offsetLeft - $("#map_canvas")[0].parentNode.offsetLeft;
            var y = event.pageY - $("#map_canvas")[0].offsetTop -$("#map_canvas")[0].parentNode.offsetTop;
            var index = self.getIndexOfNearestPosition(self.map.fromContainerPixelToLatLng(new GPoint(x,y)))
            if(index==-1){
                //$(self.overlay_label).hide()
                $("#line_bubble").html("<h5>"+self.title+"</h5>")// <p>"+self.description+"</p>")
            }else{
                try{
                    var time = self.timestamps[index]
                    var altitude = self.altitudes[index]
                    time = new Date(time)
                    var hours = time.getHours();
                    var minutes = time.getMinutes();
                    var seconds = time.getMinutes();
                    var hours_str = ((hours < 10) ? "0" + hours : hours);
                    var minutes_str = ((minutes < 10) ? "0" + minutes : minutes);
                    var seconds_str = ((seconds < 10) ? "0" + seconds : seconds);
                    $("#line_bubble").html("<h5>"+self.title+"</h5> <p>"+self.description+"</p>"+"Position Index: <b>"+index+"</b><br />Time: "+hours_str+":"+minutes_str+":"+ seconds_str+" <br /> Elevation: "+altitude+" meters<br /> Speed: ")
                }catch(e){
                    
                }
            }
            //self.currentPositionMarker.location = self.mainPolyline.getVertex(index)
            //self.currentPositionMarker.redraw(true)
        })

        $(self.overlay_label).show()
        //$(self.overlay_label).animate({marginLeft: "0px"})
        var text = "<div class='map-bubble ui-corner-all' id='line_bubble'>\
                        <h5>"+self.title+"</h5> \
                    </div>"
        $(self.overlay_label).html(text)*/
    });

    GEvent.addListener(this.mainPolyline, "mouseout", function() {
        //$(self.infoContainer).removeClassName("over");
        //$(self.infoContainer).setOpacity(.6);
        /*$(self.overlay_label).hide()
        $(document).unbind("mousemove")
        self.map.removeOverlay(self.currentPositionMarker)*/
    });

    this.areaName = null;

    this.container.className = "maptales-line-overlay";
    this.infoContainer.style.color = color;
    this.infoContainer.className = "label";
    this.container.appendChild(this.infoContainer);
    this.container.style.position = "absolute";
    this.container.style.overflow = "visible";
}

MPolyline.prototype.initialize = function(map) {
    this.map = map;
    this.polyline_placed = false;
    this.map.getPane(G_MAP_FLOAT_PANE).appendChild(this.container);
    this.map.getPane(G_MAP_FLOAT_PANE).appendChild(this.overlay_label);
    //this.map.addOverlay(this.mainPolyline);
    //this.map.getPane(G_MAP_MARKER_SHADOW_PANE).appendChild(this.container);
    //if(this.mainPolyline.getBounds()){
        //$(this.infoContainer).setOpacity(.6);
    //}else{
         //$(this.infoContainer).setOpacity(0);
    //}
    self = this;
    self.redraw(true)

}


MPolyline.prototype.getLengthInKm = function(){
    return (Math.round(this.getLength() / 10) / 100) + "km";
}

MPolyline.prototype.setStrokeStyle = function(style){
   this.mainPolyline.setStrokeStyle(style);
   var obj = Object.extend({}, style);
   obj.opacity = this.fillOpacity;
   this.mainPolyline.setFillStyle(obj);
   this.infoContainer.style.color = style.color;
}

MPolyline.prototype.enableEditing = function(){
   var bounds = this.mainPolyline.getBounds();
   this.map.setCenter(bounds.getCenter(), this.map.getBoundsZoomLevel(bounds));
   this.mainPolyline.enableEditing();
   this.shadowPolyline.remove();
}

MPolyline.prototype.disableEditing = function(){
   this.mainPolyline.disableEditing();
}

MPolyline.prototype.getIndexOfNearestPosition = function(latlng){
    //todo: this can be improved a lot
    if(this.mainPolyline.getBounds().contains(latlng)){
        var index = 0;
        var previousDistance = 0;
        for(var i=0; i<this.mainPolyline.getVertexCount()-1;i++){
            var vertex = this.mainPolyline.getVertex(i);
            var distance = vertex.distanceFrom(latlng)
            if(!previousDistance||distance<previousDistance){
               previousDistance = distance
               index = i;
            }
        }
        return index;
    }
    return -1;
}

MPolyline.prototype.enableDrawing = function(){
   this.mainPolyline.enableDrawing();
}


MPolyline.prototype.getVertexCount = function(){
   return this.mainPolyline.getVertexCount();
}

MPolyline.prototype.getVertex = function(i){
   return this.mainPolyline.getVertex(i);
}

MPolyline.prototype.remove = function() {
    try {
         this.map.removeOverlay(this.mainPolyline);
        this.map.removeOverlay(this.shadowPolyline);
        this.map.removeOverlay(this.startMarker)
        this.map.removeOverlay(this.endMarker)
    }
    catch(e){
    }
    this.map = null;
}

MPolyline.prototype.getInfoLocation = function(){
    return this.mainPolyline.getBounds().getCenter();
    //for(var i=0; i<this.mainPolyline.getVertexCount(); i++){
    //    var pixel = thig.map.fromLatLngToPixel(this.mainPolyline.getVertex(i));

    //}
}

MPolyline.prototype.redraw = function(force) {
    if(this.map){
        var dimensions = maptales.map.getDimensionsOnScreen(this.mainPolyline)
        if(dimensions.width>10||dimensions.height>10){
            if(!this.polyline_placed){
               this.polyline_placed = true;
               this.map.addOverlay(this.shadowPolyline);
               this.map.addOverlay(this.mainPolyline);
               //this.map.addOverlay(this.startMarker);
               //this.map.addOverlay(this.endMarker);
               $(this.container).html("")
            }
        }else{
            if(this.polyline_placed){
                this.polyline_placed = false;
                this.map.removeOverlay(this.shadowPolyline);
                this.map.removeOverlay(this.mainPolyline);
                //this.map.removeOverlay(this.endMarker);
                //this.map.removeOverlay(this.startMarker);
               $(this.container).html("<div class='line-marker' onclick='maptales.map.gotoLineId("+this.id+")'><span class='info-text'>Click to zoom to Line</span></div>")
            }
        }
        if(this.mainPolyline.getBounds()){
            //var pixelPos = this.map.fromLatLngToDivPixel(this.mainPolyline.getBounds().getCenter());
            //this.container.style.top = pixelPos.y + "px";
            //this.container.style.left = pixelPos.x + "px";
        }
    }
}

MPolyline.prototype.copy  = function(){ }

MPolyline.prototype.setLineName = function(areaName){
    this.areaName = areaName;
    this.infoContainer.innerHTML = "<NOBR>"+areaName+"</NOBR>";
}

MPolyline.prototype.getPolyline = function(){
    return this.mainPolyline;
}

MPolyline.prototype.getContainer = function(){
    return this.container;
}

MPolyline.prototype.getLength = function(){
    return this.mainPolyline.getLength();
}



