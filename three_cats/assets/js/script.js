// Google maps
function initialize() {
    if (document.location.pathname == '/contacts/') {
        var map_zoom = 14;
        locations = [[46.416153, 30.7109794]];
    } else {
        var map_zoom = 11;
    }
    var mapOptions = {
        center: new google.maps.LatLng(46.416153, 30.7109794),
        zoom: map_zoom,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);

    var marker, i;

    for (i = 0; i < locations.length; i++) {
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(locations[i][0], locations[i][1]),
            map: map
        });

        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                infowindow.setContent(locations[i][0]);
                infowindow.open(map, marker);
            }
        })(marker, i));
    }
}

$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

    // Cabinets tooptips
    //$('.cs-tooltip').tooltip();


$(document).ready(function() {

    $('#myCarousel').carousel()

    $('#mainCarousel').carousel()

    $('#cs-contact-form-submit').on('click', function(e) {
        e.preventDefault();
        if ($('#cs-contact-form').is_valid()) {$('#cs-contact-form').submit();}
    });
    
    $('#cs-button-order').on('click', function(e) {
        e.preventDefault();
        e_id = $(this).attr('el_id');
        $.ajax({
            url: '/order/',
            data: JSON.stringify({'id': e_id}),
            type: 'post',
            success: function(response, textStatus, jqXHR) {
                $('#cs-cart').replaceWith(response['cart']);
            }
        });
    });

    // Order item
    $('.cs-elephant-order-confirm').on('click', function() {
        //alert($(this).data('id'))
        $.ajax({
            url: '/order/' + $(this).data('id') + '/1/',
            type: 'post',
            success: function(data) {
                if (data.success) {
                    location.reload();
                }
            }
        });
    });

    $('.cs-cart-order').on('click', function(e) {
        $('.cs-cart-confirm').data();
        e.preventDefault();
        $.ajax({
            url: '/cart/',
            type: 'get',
            success: function(data) {
                $('#cs-cart-content').html(data.html);
            }
        });
    });


    $('.cs-photo-simple').on('click', function(e) {
        $('.cs-cart-confirm').data();
        id = $(this).data('id');
        e.preventDefault();
        $.ajax({
            url: '/simple_photo/'+id+'/',
            type: 'get',
            success: function(data) {
                $('#cs-photo-content').html(data.html);
            }
        });
    });

    $('#cs-cart-modal .modal-body').on('click', '.cs-cart-remove', function() {
        $.ajax({
            url: '/cart_remove/' + $(this).data('id') + '/',
            type: 'post',
            success: function(data) {
                if (data.success) {
                    //location.reload();
                    $.ajax({
                        url: '/cart/',
                        type: 'get',
                        success: function(data) {
                            $('#cs-cart-content').html(data.html);
                        }
                    });
                }
            }
        });
    });

    $('#cs-cart-modal').on('hide', function() {
       location.reload();
    });

    $('#cs-photo-modal').on('hide', function() {
       location.reload();
    });

    $("#cs-vk")
        .mouseover(function() {
            var src = $(this).attr("src").match(/[^\.]+/) + "-1.png";
            $(this).attr("src", src);
        })
        .mouseout(function() {
            var src = $(this).attr("src").replace("vk-icon-1.png", "vk-icon.png");
            $(this).attr("src", src);
    });

    $("#cs-facebook")
        .mouseover(function() {
            var src = $(this).attr("src").match(/[^\.]+/) + "-1.png";
            $(this).attr("src", src);
        })
        .mouseout(function() {
            var src = $(this).attr("src").replace("facebook-icon-1.png", "facebook-icon.png");
            $(this).attr("src", src);
    });

    $("#cs-instagram")
        .mouseover(function() {
            var src = $(this).attr("src").match(/[^\.]+/) + "-1.png";
            $(this).attr("src", src);
        })
        .mouseout(function() {
            var src = $(this).attr("src").replace("instagram-icon-1.png", "instagram-icon.png");
            $(this).attr("src", src);
    });

    $(window).load(function () {
        if ($("div").is("#elephant-1")) {

          var x0 = $('#elephant-1').position().top;
          var x =new Array(x0, x0, x0);
          var el_width = parseInt($('#elephant-1').outerWidth());
          var el_left = parseInt($('#elephant-1').offset().left);
          var el_delta = parseInt($('#elephant-2').offset().left)-parseInt($('#elephant-1').offset().left)-el_width;
          //$('#elephant-1').remove();
          //$('#elephant-2').remove();
          var el_top = nmin = el_y = n = i = 0;
          var elephants = $('.elephant');
          //alert('---+iIi+---');

          for (i = 0; i<elephants.length; i++) {
                elephant = elephants[i];
                var arrX = new Array(x[0], x[1], x[2]);
                //alert('x='+String(x[0])+' '+String(x[1])+' '+String(x[2])+' '+String(x[3]));
                el_top = arrX[0]; nmin = 0;
                for (n = 0; n<arrX.length; n++) {if (arrX[n]<el_top) {el_top=arrX[n]; nmin=n;}};
                el_top = el_top+el_delta;
                el_y = el_left + nmin*(el_width+el_delta);
                $(elephant).offset({top:el_top, left:el_y});
                x[nmin]=el_top + parseInt($(elephant).outerHeight());
          };

        };
    });

    $(window).load(function () {
        if ($("div").is("#stores-1")) {

          var elephants = $('.stores');
          el_max_h = 0;
          for (i = 0; i<elephants.length; i++) {
                elephant = elephants[i];
                el_h = parseInt($(elephant).outerHeight());
                if (el_h>el_max_h) {el_max_h = el_h;}
          };
          for (i = 0; i<elephants.length; i++) {
              elephant = elephants[i];
              $(elephant).height(el_max_h);
          }
          var x0 = $('#stores-1').position().top;
          var x =new Array(x0, x0, x0);
          var el_width = parseInt($('#stores-1').outerWidth());
          var el_left = parseInt($('#stores-1').offset().left);
          var el_delta = parseInt($('#stores-2').offset().left)-parseInt($('#stores-1').offset().left)-el_width;
          var el_top = nmin = el_y = n = i = 0;
          var elephants = $('.stores');
          for (i = 0; i<elephants.length; i++) {
                elephant = elephants[i];
                var arrX = new Array(x[0], x[1], x[2]);
                //alert('x='+String(x[0])+' '+String(x[1])+' '+String(x[2])+' '+String(x[3]));
                el_top = arrX[0]; nmin = 0;
                for (n = 0; n<arrX.length; n++) {if (arrX[n]<el_top) {el_top=arrX[n]; nmin=n;}};
                el_top = el_top+el_delta;
                el_y = el_left + nmin*(el_width+el_delta);
                $(elephant).offset({top:el_top, left:el_y});
                x[nmin]=el_top + parseInt($(elephant).outerHeight());
          };

        };
    });

    // Orders
    $('.cs-order-position').on('click', function(e) {
        e.preventDefault();

        var order_id = $(this).data('id');

        if ($('#cs-order-position-'+order_id).html() == '') {
          $.ajax({
              url: '/order_position/',
              data: 'order_id=' + order_id,
              type: 'get',
              success: function(data) {
                  $('#cs-order-position-'+order_id).html(data.html);
              },
              error: function() {
                  // In case of unpredictable error show this message to the user
              }
          });
        } else {$('#cs-order-position-'+order_id).html('');};
    });

    // Translate
    $('#cs-locate-ru').on('click', function(e) {
          $.ajax({
              url: '/i18n/setlang/',
              data: 'language=ru',
              type: 'post',
              success: function() {
                  location.reload();
              },
              error: function() {
              }
          });

    });

    // Перевод
    $('#cs-locate-en').on('click', function(e) {
        e.preventDefault();
          alert('===');
          $.ajax({
              url: '/i18n/setlang/',
              data: 'language=en',
              type: 'post',
              success: function() {
                  alert('+++');
                  location.reload();
              },
              error: function() {
                  alert('---');
              }
          });

    });

    // Orders
    $('#cs-order-select-btn').on('click', function(e) {
        if ($('#cs-order-select').val() == 4) {
            window.location.href = '/orders/';
            window.location.load();
        } else {
            window.location.href = '/orders/'+$('#cs-order-select').val()+'/';
            window.location.load();
        };

    });

    // Call to Google Maps
    initialize();

});