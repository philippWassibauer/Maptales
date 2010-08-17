function MCluster(data) {
  this.location = new GLatLng(data.center.lat, data.center.lng);
  this.data = data
  this.size = data.size
  this.html = "<div class='cluster cluster-"+this.cssRule()+"'><span>"+data.size+"</span></div>"
  this.hoverHTML = data.html
}

MCluster.prototype = new GOverlay();

MCluster.prototype.initialize = function(map) {
  this.map = map;
  this.div = document.createElement("div");
  this.div.marker = this;
  this.div.style.zIndex = GOverlay.getZIndex(this.location.lat())

  this.div.className = "maptales-marker-wrapper"
  this.map.getPane(G_MAP_MAP_PANE).appendChild(this.div);
  $(this.div).html(this.html);
  this.div.cluster = this
  $(this.div).click(function(){
        this.cluster.map.setCenter(this.cluster.getLatLng(), this.cluster.map.getZoom()+2)
  })
  
  this.ismouseover = false
  $(this.div).mouseover(function(){
        if(this.cluster.ismouseover==false){
            //console.log("show")
            this.cluster.ismouseover = true;
            var rule = this.cluster.cssRule()
            var offset = 8;
            if(rule>16){
                offset = 16
            }
            data = {additionalClass: "cluster-overlay", offsetLeft: "-50%", offsetBottom: offset, html: this.cluster.hoverHTML}
            maptales.map.showMouseOverHover(this.cluster.getLatLng(), data);
            self = this.cluster
            $(window).bind("mousemove", this.cluster.moveDelegate)
            $("body").data("currentCluster", this.cluster)
        }
  })
  
  $(this.div).mouseout(function(event){
        //this.cluster.possiblyCloseOverlay(event)
  })
}

MCluster.prototype.cssRule = function() {
   if(this.size<2){
        return 1;
   }else if(this.size<4){
        return 2;
   }else if(this.size<8){
        return 4;
   }else if(this.size<16){
        return 8;
   }else if(this.size<32){
        return 16;
   }else if(this.size<64){
        return 32;
   }
   return 64;
}

MCluster.prototype.possiblyCloseOverlay = function(event) {
    if(!maptales.map.isMouseOverHover(event)){
        $("body").data("currentCluster").ismouseover = false;
        maptales.map.hideMouseOverHover();
        $(window).unbind("mousemove", this.moveDelegate)
    }
}

MCluster.prototype.moveDelegate = function(event_move){
    throttle(function(){
        var element = $($("body").data("currentCluster").div).find(".cluster")
        var maxX = element.offset().left+element.width()+10;
        var maxY = element.offset().top+element.height()+10;
        var left = element.offset().left-10;
        var top = element.offset().top-10;
        //console.log("x: "+event_move.pageX+": y: "+event_move.pageY+", tl: "+top+" "+left+", br: "+maxY+" "+maxX);
        if(event_move.pageX>left&&
           event_move.pageX<maxX&&
           event_move.pageY>top&&
           event_move.pageY<maxY){
            return true
        }else{
            //console.log("close")
            $("body").data("currentCluster").possiblyCloseOverlay(event_move)
        }
        return false
    }, window);
}

MCluster.prototype.remove = function() {
  this.div.parentNode.removeChild(this.div);
}

MCluster.prototype.getLatLng = function() {
  return this.location;
}


MCluster.prototype.copy = function() {
  return new MMarker(this.location, this.html);
}

MCluster.prototype.onClick =function(){

    
}

MCluster.prototype.select = function() {
  $(this.div).addClass("selected")
    this.selected = true;
}

MCluster.prototype.deselect = function() {
  $(this.div).removeClass("selected")
    this.selected = false;
}


MCluster.prototype.redraw = function(force) {
  if (!force) return;
  var location = this.map.fromLatLngToDivPixel(this.location);
  this.div.style.left = location.x + "px";
  this.div.style.top = location.y + "px";
  this.div.innerHTML = this.html
  $(this.contentDiv).append( this.html , this.data);
}
