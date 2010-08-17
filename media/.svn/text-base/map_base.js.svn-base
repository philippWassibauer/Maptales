

function getLengthInKm(line){
    return (Math.round(line.getLength() / 10) / 100)
}

function onResize(is_initial){
    /*var dimensions = {};
    dimensions.width = $(window).width()
    dimensions.height = $(window).height()

    if($('#adaptingContainer')){
        var height_num = dimensions.height-($('#adaptingContainer')[0].offsetTop);
        height_num = height_num - $('#adaptingContainer').margin().top - $('#adaptingContainer').margin().bottom
        if($('.story-top-bar')&&$('.story-top-bar')[0]){
           height_num = height_num-$('.story-top-bar').height()
        }
        
        var height = height_num+"px"
        $('#adaptingContainer').height(height_num);

        if($('#map_canvas')){
            if($('#innerAdaptingContainerBlock')&&$('#innerAdaptingContainerBlock')[0]){
                var top_height = 0
                
                $('#map_canvas').height(height_num-$('#innerAdaptingContainerBlock').height()-top_height);
            }else{
                $('#map_canvas').height(height_num)
            }

            if($('#info-panel')&&$('#info-panel')[0]){
                $('#map_canvas').width(dimensions.width-$('#info-panel')[0].offsetWidth);
            }else{
                $('#map_canvas').width(dimensions.width);
            }
        }

        if($('#info-panel')&&$('#info-panel')[0]){
           $('#info-panel')[0].style.height = height;
        }
        if(is_initial){
           maptales.map.initialResize()
        }else{
           maptales.map.checkResize();
        }
    }*/

    try{
        if($('#storylinecontainer')){
            var offsetTop = $('#storylinecontainer')[0].offsetTop;
            var infoHeight = $('#mapview-option-panel')[0].offsetHeight;
            var height = $('#info-panel')[0].offsetHeight - offsetTop - infoHeight;
            $('#storylinecontainer')[0].style.height = height+"px";
        }
    }catch(e){
        
    }
}

var line_list = []


var lineTemplateString = "<div id='line_${index}' class='line'> " +
                            "<div class='options'><a href='#' line-index='${index}' class='edit-line'>edit</a> " +
                            "| <a href='#' onclick='removeLineFromStory(${index})'>delete</a>" +
                         "</div>"+
                         "<a href='#' class='line-link' onclick='maptales.map.zoomToLine(${index}); return false;'>${name}</a> ${km}"

function addLineToList(index){
    try{
        var line_template = $.template(lineTemplateString)
        var line = maptales.map.getLine(index)
        line_list.push(line)
        $('#line-list').append( line_template , {
             name: 'Line '+index,
             km:  getLengthInKm(line) + "km",
             index: index
        });
        initLineEdit();
    }catch(e){
        alert("addLineToList "+e)
    }
}

function initLineEdit(){
    $('.edit-line').click(function(){
        toggleEditingLine($(this), $(this).attr("line-index"))
        return false;
    })
    $('#line-list>div').removeClass('ui-corner-bl');
    $('#line-list>div:last').addClass('ui-corner-bl');
}
function toggleEditingLine(dom, index){
    if($(dom).hasClass("stop-editing")){
        stopEditingLine()
    }else{
        $(dom).addClass("stop-editing")
        $(dom).html("Stop Editing")
        $(dom).click(stopEditingLine)
        maptales.map.editLine(index)
    }
}

function stopEditingLine(){
    updateLine(maptales.map.getEditedLine(), function(){
        successMessage("Line has been updated.")
    })
    maptales.map.stopEditingLine()
    redrawLineList()
}

function redrawLineList(){
   var line_template = $.template(lineTemplateString)
   $('#line-list')[0].innerHTML = "";
   for(index in line_list){
        var real_index = parseInt(index)+1;
        $('#line-list').append( line_template , {
             name: 'Line '+real_index,
             km: getLengthInKm(maptales.map.getLine(real_index)) + " km",
             index: real_index
        });
   }
   initLineEdit();
}

function storeLine(line, callback){
     var points = []
     for(var i=0; i<line.getVertexCount(); i++){
        var point = line.getVertex(i);
        points[i] = point.lng()+" "+point.lat();
     }
     var pointsString = points.join(", ")
     post(STORE_LINE_URL, {content_object_id:CURRENT_STORY_ID, content_type:"story.story", points: pointsString, title: "Line", description: "Hand drawn line"}, "text", function(data){
         if (callback){
             data = json_parse(data)
             data.line = json_parse(data.line)
             return callback(data.line)
         }
     })
}

function updateLine(line, callback){
     var points = []
     for(var i=0; i<line.getVertexCount(); i++){
        var point = line.getVertex(i);
        points[i] = point.lng()+" "+point.lat();
     }
     var pointsString = points.join(", ")
     post(UPDATE_LINE_URL, {id:line.id, points: pointsString}, "text", function(data){
         if (callback){
             data = json_parse(data)
             data.line = json_parse(data.line)
             return callback(data.line)
         }
     })
    
}

function updateLineEditingArea(){

}

function displaySuccessMessage(text){

}

function displayErrorMessage(text){
    
}

function storePosition(objectId, contentType, latlng, callback){
     post(PLACE_MARKER_URL, {content_object_id:objectId, content_type:contentType, lat: latlng.lat(), lng: latlng.lng()}, "text", function(data){
         if (callback){
             data = json_parse(data)
             data.item = json_parse(data.item)
             return callback(data.item)
         }
     })
}
