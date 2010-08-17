function HTMLMarker(location, html) {
  this.location = location;
  this.html = html
}

HTMLMarker.prototype = new GOverlay();

HTMLMarker.prototype.initialize = function(map) {
  this.map = map;
  this.div = document.createElement("div");
  this.div.marker = this;
    $(this.div).mousedown(function(event){ event.cancelBubble=true; return false;});
  this.div.style.zIndex = GOverlay.getZIndex(this.location.lat())

  this.div.className = "maptales-marker-wrapper"
  this.map.getPane(G_MAP_MARKER_PANE).appendChild(this.div);
  $(this.div).html(this.html);

}


HTMLMarker.prototype.remove = function() {
  this.div.parentNode.removeChild(this.div);
}

HTMLMarker.prototype.getLatLng = function() {
  return this.location;
}


HTMLMarker.prototype.copy = function() {
  return new MMarker(this.location, this.html);
}

HTMLMarker.prototype.onClick =function(){
    maptales.map.onMarkerClick(this)
}

HTMLMarker.prototype.select = function() {
  $(this.div).addClass("selected")
    this.selected = true;
}

HTMLMarker.prototype.deselect = function() {
  $(this.div).removeClass("selected")
    this.selected = false;
}


HTMLMarker.prototype.redraw = function(force) {
  if (!force) return;
  var location = this.map.fromLatLngToDivPixel(this.location);
  this.div.style.left = location.x + "px";
  this.div.style.top = location.y + "px";
  this.div.innerHTML = this.html
  $(this.contentDiv).append( this.html , this.data);
}
