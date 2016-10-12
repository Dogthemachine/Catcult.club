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


$(document).ready(function() {
    //---?---
    $('#cs-contact-form-submit').on('click', function(e) {
        e.preventDefault();
        if ($('#cs-contact-form').is_valid()) {$('#cs-contact-form').submit();}
    });

    // Order item
    $('.cc-order-confirm').on('click', function() {
        //alert($(this).data('id'))
        $.ajax({
            url: '/order/' + $(this).data('id') + '/',
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

    $('#cs-cart-modal').on('hide', function() {
       location.reload();
    });

    $('#cs-photo-modal').on('hide', function() {
       location.reload();
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

    $('#cc-cart-link').on('click', function() {
        $.ajax({
            url: '/cart/',
            type: 'get',
            success: function(data) {
                $('#cc-cart-content').html(data.html);
            }
        });
    });

    $('#cc-cart-checkout').on('click', function() {
        console.log($(this).data('ready'));
        if ($(this).data('ready') == 1) {
            var type = 'post';
            var data = $('#cc-checkout-form').serialize();
        } else {
            var type = 'get';
            var data = {};
        }

        $.ajax({
            url: '/cart/checkout/',
            type: type,
            data: data,
            success: function(data) {
                if (data.form) {
                    $('#cc-cart-content').html(data.html);
                    $('#cc-cart-checkout').html(data.button_text);
                    $('#cc-cart-checkout').data('ready', 1);
                } else {
                    if (data.html) {
                        $('#cc-cart-content').html(data.html);
                    } else {
                        location.reload();
                    }
                }
            }
        });
    });

    $('#cc-cart-cancel').on('click', function() {
        location.reload();
    });

    $('body').on('DOMNodeInserted',function(e){
        $('.cc-cart-remove').on('click', function(e) {
            e.preventDefault();

            $.ajax({
                url: '/cart/' + $(this).data('id') + '/remove/',
                type: 'post',
                success: function(data) {
                    $('#cc-cart-content').html(data.html);
                    $('#cc-cart-total').html(data.count);
                },
            });
        });
    });

    var sourceSwap = function () {
        var $this = $(this);
        var newSource = $this.data('hover-src');
        $this.data('hover-src', $this.attr('src'));
        $this.attr('src', newSource);
    }

    $('.cc-cat-image').hover(sourceSwap, sourceSwap);

    $('#cc-pics').flexslider({
        animation: "slide"
    });

    $('.cc-zoom img').elevateZoom({
        responsive: true,
        easing: true,
        zoomType: 'inner',
        cursor: 'crosshair',
        gallery: 'cc-product-photos',
        galleryActiveClass: 'cc-product-active-photo',
        imageCrossfade: true,
        loadingIcon: 'http://www.elevateweb.co.uk/spinner.gif'
    });

});
