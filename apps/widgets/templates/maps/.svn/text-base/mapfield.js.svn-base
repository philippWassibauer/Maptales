{% load object_to_content_type %}

PLACE_MARKER_URL = "{% url place_item %}"

function onLocationSearchComplete(lat, lng){
    if(FIELD_INPUT_MARKER){
       field_map.removeOverlay(FIELD_INPUT_MARKER)
    }
    field_map.setCenter(new GLatLng(lat, lng), 11);
    initial_drop_zoom = 11
    placeMarker(new GLatLng(lat, lng))
}

function storeLocationFieldValue(){
    storePosition('{{item_to_place.id}}', '{{item_to_place|object_to_model_name}}', FIELD_INPUT_MARKER.getLatLng(), function(reply){
         $('#placement-text').html("Stored")
        window.setTimeout(function(){
           $('#location-submit-text').fadeOut()
        }, 2000)
    });
}

var FIELD_INPUT_MARKER = null;
if (GBrowserIsCompatible()) {

    {% if value %}
        var center = new GLatLng({{value}});
        var zoom = 13;
         var initial_drop_zoom = 13;
    {% else %}
        var center = new GLatLng({{default_center}});
        var zoom = 1;
         var initial_drop_zoom = 5;
    {% endif %}

    field_map = new GMap2(document.getElementById("field_map"));
    field_map.addControl(new GSmallMapControl());
    field_map.addControl(new GMapTypeControl());
    field_map.setMapType(G_HYBRID_MAP);
    field_map.setCenter(center, zoom);
    GEvent.addListener(field_map, "zoomend", function() {
        calculatePrecision()
    });

   
     function set_value(marker){
         $("#id_{{field_name}}")[0].value = "POINT("+marker.getLatLng().lat()+" "+marker.getLatLng().lng()+")";
     }


    var increment = 2;
    function endDrag(event){
       var pos = [event.pageX,event.pageY];
       var x = event.pageX - $("#field_map")[0].offsetLeft;
       var y = event.pageY - $("#field_map")[0].offsetTop;
       if(x>0&&y>0){
           $('#field_map_submit').show()
           var latlng = field_map.fromContainerPixelToLatLng({x:x, y:y});

           placeMarker(latlng)
           set_value(FIELD_INPUT_MARKER);

           if(field_map.getZoom()<initial_drop_zoom){
               field_map.setCenter(FIELD_INPUT_MARKER.getLatLng(), initial_drop_zoom)
           }

       }
    }

    function calculatePrecision(){
        var precision = field_map.getZoom()
        if(precision<=5){
           $('#placement-text').html("Country Level - unprecise").addClass("low-precission")
        }else if(precision<=9){
           $('#placement-text').html("City Level - unprecise").addClass("medium-precission")
        }else if(precision<=13){
           $('#placement-text').html("Street Level").addClass("good-precission")
        }else if(precision<=17){
           $('#placement-text').html("Exact").addClass("perfect-precission")
        }
        $('#location-submit-text').show()
    }

    function placeMarker(latlng){
        FIELD_INPUT_MARKER = new GMarker(latlng, {draggable: true})
        field_map.addOverlay(FIELD_INPUT_MARKER);
        GEvent.addListener(FIELD_INPUT_MARKER, "dragend", function() {
            set_value(FIELD_INPUT_MARKER);
            if(field_map.getZoom()<17){
               initial_drop_zoom = initial_drop_zoom+increment;
               field_map.setCenter(FIELD_INPUT_MARKER.getLatLng(), initial_drop_zoom)
           }
            field_map.setCenter(FIELD_INPUT_MARKER.getLatLng(), field_map.getZoom());
        });
    }


    $(document).ready(function(){
         $('.draggable').draggable({
            stop: function(event, ui){
                $(ui.helper.context).hide()
                endDrag(event)
            }
        })
    })

     {% if value %}
        placeMarker(center)
    {% else %}
        var geocoder = new GClientGeocoder()

        $('#id_address, #id_city, #id_zip_code').blur(function(){
              var adress = ""
              if($('#id_address')[0].value){
                  adress = $('#id_address')[0].value;

                  if($('#id_zip_code')[0].value){
                      adress += " "+$('#id_zip_code')[0].value
                  }

                  if($('#id_city')[0].value){
                      adress += " "+$('#id_city')[0].value
                  }else{
                      adress += " , Salzburg"
                  }
                  showAddress(adress);
              }
        })


        function showAddress(address) {
              if (geocoder) {
                geocoder.getLatLng(address,
                  function(point) {
                        if (!point) {
                          //alert(address + " not found");
                        } else {
                          field_map.setCenter(point, 13);
                          if(FIELD_INPUT_MARKER==null){
                            //FIELD_INPUT_MARKER = new GMarker(point, {draggable: true});
                            //field_map.addOverlay(FIELD_INPUT_MARKER);
                          }else{
                             FIELD_INPUT_MARKER.setLatLng(point)
                          }
                          set_value(FIELD_INPUT_MARKER)
                        }
                  }
                );
              }
         }

    {% endif %}
}

