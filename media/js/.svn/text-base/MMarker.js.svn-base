function MMarker(location, data, draggable) {
  this.location = location;
  this.html = ""
  this.setData(data || {})
  this.draggable = draggable || false;
}

MMarker.prototype = new GOverlay();

MMarker.prototype.initialize = function(map) {
  this.map = map;
  this.div = document.createElement("div");
  this.div.marker = this;
    $(this.div).mousedown(function(event){ event.cancelBubble=true; return false;});
  this.div.style.zIndex = GOverlay.getZIndex(this.location.lat())

  this.markerdiv = document.createElement("div");
  this.div.className = "maptales-marker-wrapper"
  this.markerdiv.className = "maptales-marker"
  this.map.getPane(G_MAP_MARKER_PANE).appendChild(this.div);
  this.div.appendChild(this.markerdiv);
  if (this.originalData.text && this.originalData.text.length>60){
    this.bubbleText = this.originalData.text.substr(0, 60)+"...";
  }else{
    this.bubbleText = this.originalData.text;
  }
  
  $(this.div).append("<div class='map-bubble ui-corner-all'>"+this.bubbleText+"</div>")
  this.contentDiv = document.createElement("div");
  this.contentDiv.className = "marker-content";
  self = this;
  
  if(this.bubbleText && this.bubbleText.length > 0){
    $(this.contentDiv).mouseover(function(){
      $(self.div).children(".map-bubble").show()
    })
  }
  
  
  $(this.contentDiv).mouseout(function(){
     $(self.div).children(".map-bubble").fadeOut()
  })
  
  this.div.appendChild(this.contentDiv);
  $(this.contentDiv).append( this.html , this.data);
    this.selected = false;
   var self = this
   $(this.div).click(function(){
       self.onClick(self.originalData)
   })
}

MMarker.prototype.setData = function(data) {
  this.originalData = $.extend( {}, data );
  if(data.type=="story.story_line_item"){
      var markerImage = STATIC_URL+"images/post-50-50.gif"
      if(data.marker_image){
         markerImage = data.marker_image;
      }
     this.data = {image: markerImage, location: this.location};
     this.html = $.template("<div><img src='${image}' width='25' height='25'/></div>");
  }else{
     this.data = {image: data.marker_image, location: this.location};
     if(data.marker_image){
        this.html = $.template("<div><img src='${image}' width='25' height='25' /></div>");
     }else{
        this.html = $.template("<div><img src='${image}' width='25' height='25' /></div>");
     }
  }
}

MMarker.prototype.onClick =function(){
    maptales.map.onMarkerClick(this)
}

MMarker.prototype.resetData = function() {
   this.setData(this.originalData);
}

MMarker.prototype.remove = function() {
  this.div.parentNode.removeChild(this.div);
}

MMarker.prototype.getLatLng = function() {
  return this.location;
}


MMarker.prototype.copy = function() {
  return new MMarker(this.location, this.html,this.data);
}

MMarker.prototype.select = function() {
  $(this.div).addClass("selected")
  this.selected = true;
  this.redraw()
}

MMarker.prototype.deselect = function() {
  $(this.div).removeClass("selected")
  this.selected = false;
  this.redraw()
}


MMarker.prototype.redraw = function(force) {
  if (!force) return;
  // get the size and position of our rectangle
  if(!this.map)return;
  
  var zIndex = GOverlay.getZIndex(this.location.lat())
  if(this.selected){
      zIndex = 9999999999999999999;
  }
  this.div.style.zIndex = zIndex;
  var location = this.map.fromLatLngToDivPixel(this.location);

  // Now position our DIV based on the DIV coordinates of our bounds
  this.div.style.left = location.x + "px";
  this.div.style.top = location.y + "px";
  this.contentDiv.innerHTML = "";
  this.resetData()
  $(this.contentDiv).append( this.html , this.data);
  if(this.draggable){
       //var handle_node = $("<div class='marker-drag-handle'>&nbsp;</div>")
       //$(this.contentDiv).append(handle_node)
       var self = this;
       $(this.div).draggable({ //handle: '.marker-drag-handle',
            start: function(event, ui){
                event.cancelBubble = true;
                return false; 
            },
            stop: function(event, ui){
                 //var self = ui.helper[0].marker
                 var position = $(self.div).offset();
                 var current_x = position.left - $("#map_canvas").offset().left;// - $("#map_canvas").offset().left;
                 var current_y = position.top - $("#map_canvas").offset().top; //ui.position.top;//  - $("#map_canvas")[0].offsetTop -$("#map_canvas")[0].parentNode.offsetTop;
                 self.location = maptales.map.gmap.fromContainerPixelToLatLng({x:current_x, y:current_y})
                 self.redraw(true)
                 var type = self.originalData.type;
                 var id = self.originalData.id;
                 try{
                    storePosition(id, type, self.location, function(reply){
                         successMessage("Successfully stored new Position")
                    });
                 }catch(e){
                  
                 }
                 
            }
        });
  }
}
