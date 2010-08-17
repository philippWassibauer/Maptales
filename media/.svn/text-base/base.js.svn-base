
function post(url, parameters, type, callback){
    //display loading
    $.post(url, parameters, function(data){
         if (callback){
            callback(data);
         }
    }, type);
}


function get(url, type, callback){
    //display loading
    $.get(url, {}, function(data){
         if (callback){
            callback(data);
         }
    }, type);
}

function successMessage(message){
    $("#ajax-message").html("")
    $("#ajax-message").show()
    $("#ajax-message").append("<div>" + message + "</div>");
    window.setTimeout(function(){
       $("#ajax-message").fadeOut()  
    }, 2000)
}

$(document).ready(function(){
   $("#ajax-message").ajaxError(function(event, request, settings){
        $(this).append("<div class='error'>Error requesting page " + settings.url + "</div>");
    });
})

function throttle(method, scope) {
    clearTimeout(method._tId);
    method._tId= setTimeout(function(){
        method.call(scope);
    }, 100);
}


