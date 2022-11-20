// Google maps
//function initialize() {
//
//    if (document.location.pathname == '/en/contacts/' || document.location.pathname == '/ru/contacts/' || document.location.pathname == '/uk/contacts/') {
//        var map_zoom = 14;
//        locations = [[46.481049, 30.744456]];
//    } else {
//        var map_zoom = 11;
//    }
//
//    var mapOptions = {
//        center: new google.maps.LatLng(46.481049,30.744456),
//        zoom: map_zoom,
//        mapTypeId: google.maps.MapTypeId.ROADMAP
//    };
//
//    var map = new google.maps.Map(document.getElementById("map_canvas_contacts"), mapOptions);
//
//    var marker, i;
//
//    for (i = 0; i < locations.length; i++) {
//        marker = new google.maps.Marker({
//            position: new google.maps.LatLng(locations[i][0], locations[i][1]),
//            map: map
//        });
//
//        google.maps.event.addListener(marker, 'click', (function(marker, i) {
//            return function() {
//                infowindow.setContent(locations[i][0]);
//                infowindow.open(map, marker);
//            }
//        })(marker, i));
//    }
//}

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
        var loc_lang = get_loc_lang();
        //alert($(this).data('id'))
        $.ajax({
            url: loc_lang + '/order/' + $(this).data('id') + '/',
            type: 'post',
            success: function(data) {
                if (data.success) {
                    location.reload();
                }
            }
        });
    });

    $('#cs-photo-modal').on('hide', function() {
       location.reload();
    });

    // Orders
    $('.cs-order-position').on('click', function(e) {
        e.preventDefault();

        var order_id = $(this).data('id');

        if ($('#cs-order-position-'+order_id).html() == '') {
        var loc_lang = get_loc_lang();
          $.ajax({
              url: loc_lang + '/order_position/',
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
          e.preventDefault();

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

    $('#cs-locate-en').on('click', function(e) {
        e.preventDefault();
          $.ajax({
              url: '/i18n/setlang/',
              data: 'language=en',
              type: 'post',
              success: function() {
                  location.reload();
              },
              error: function() {
              }
          });

    });

    $('#cs-locate-uk').on('click', function(e) {
        e.preventDefault();
          $.ajax({
              url: '/i18n/setlang/',
              data: 'language=uk',
              type: 'post',
              success: function() {
                  location.reload();
              },
              error: function() {
              }
          });

    });

    $('#cc-language').on('change', function(e) {
        var lang = $("#cc-language").val();

        n_lang = '/' + lang + '/';
        if (lang=='uk') { n_lang = '/';}
        pathname = window.location.pathname.substr(1);

        if (window.location.pathname.indexOf('/ru/')==0)
        {
            pathname = window.location.pathname.substr(4);
        };

        if (window.location.pathname.indexOf('/en/')==0)
        {
            pathname = window.location.pathname.substr(4);
        };

        loc = window.location.protocol + '//' + window.location.host + n_lang + pathname;

        window.location = loc;
    });

    $('#cc-valuta').on('change', function(e) {
        var valuta = $("#cc-valuta").val();
        var loc_lang = get_loc_lang();
        e.preventDefault();
          $.ajax({
              url: loc_lang + '/cart/valuta/',
              data: 'valuta=' + valuta,
              type: 'post',
              success: function() {
                  location.reload();
              },
              error: function() {
              }
          });

    });

    //Comments
    $('#cc-comment-confirm').on('click', function() {
        var loc_lang = get_loc_lang();
        $.ajax({
            url: loc_lang + '/comment/',
            type: 'post',
            data: $('#cc-add-comment-form').serializeArray(),
            success: function(data) {
                if (data.success) {
                    location.reload();
                } else {
                    $('#cc-comment-modal .modal-body').html(data.form_html);
                }
            }
        });
    });

    $('.cc-replay-link').on('click', function() {
        var comment_id = $(this).data('comment-id');
        $('#cc-add-replay-form #id_comment_id').val(comment_id);
    });

    $('.cc-comment-link').on('click', function() {
        var item_id = $(this).data('item-id');
        $('#cc-add-comment-form #id_item_id').val(item_id);
        $('#cc-add-comment-form #id_set_id').val('0');
    });

    $('#cc-replay-confirm').on('click', function() {
        var loc_lang = get_loc_lang();
        $.ajax({
            url: loc_lang + '/replay/',
            type: 'post',
            data: $('#cc-add-replay-form').serializeArray(),
            success: function(data) {
                if (data.success) {
                    location.reload();
                } else {
                    $('#cc-replay-modal .modal-body').html(data.form_html);
                }
            }
        });
    });

    $('.cc-comment-activate').on('click', function() {
        var loc_lang = get_loc_lang();
        var id_com = $(this).data('comment-id');
        $.ajax({
            url: loc_lang + '/comment-activate/' + id_com + '/',
            type: 'post',
            success: function(data) {
                if (data.success) {
                    location.reload();
                } else {
                }
            }
        });
    });

    $('.cc-comment-deactivate').on('click', function() {
        var loc_lang = get_loc_lang();
        var id_com = $(this).data('comment-id');
        $.ajax({
            url: loc_lang + '/comment-deactivate/' + id_com + '/',
            type: 'post',
            success: function(data) {
                if (data.success) {
                    location.reload();
                } else {
                }
            }
        });
    });

    $('.cc-comment-delete').on('click', function() {
        var loc_lang = get_loc_lang();
        var id_com = $(this).data('comment-id');
        $.ajax({
            url: loc_lang + '/comment-delete/' + id_com + '/',
            type: 'post',
            success: function(data) {
                if (data.success) {
                    location.reload();
                } else {
                }
            }
        });
    });

    $('.cc-reply-activate').on('click', function() {
        var loc_lang = get_loc_lang();
        var id_com = $(this).data('reply-id');
        $.ajax({
            url: loc_lang + '/replay-activate/' + id_com + '/',
            type: 'post',
            success: function(data) {
                if (data.success) {
                    location.reload();
                } else {
                }
            }
        });
    });

    $('.cc-reply-deactivate').on('click', function() {
        var loc_lang = get_loc_lang();
        var id_com = $(this).data('reply-id');
        $.ajax({
            url: loc_lang + '/replay-deactivate/' + id_com + '/',
            type: 'post',
            success: function(data) {
                if (data.success) {
                    location.reload();
                } else {
                }
            }
        });
    });

    function get_loc_lang() {
        var lang = window.location.pathname.toString().substr(0,2);
        if (lang=='en') {return '/' + lang};
        if (lang=='ru') {return '/' + lang};
        return ''
    };

    $('.cc-reply-delete').on('click', function() {
        var loc_lang = get_loc_lang();
        var id_com = $(this).data('reply-id');
        $.ajax({
            url: loc_lang + '/replay-delete/' + id_com + '/',
            type: 'post',
            success: function(data) {
                if (data.success) {
                    location.reload();
                } else {
                }
            }
        });
    });

    //Tooltips
    $('.cc-tooltip').tooltip();

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

    $('.cc-cart-link').on('click', function() {
        var loc_lang = get_loc_lang();
        $.ajax({
            url: loc_lang + '/cart/',
            type: 'get',
            success: function(data) {
                $('#cc-cart-content').html(data.html);
                $('#cc-cart-cancel').show();
            }
        });
    });

    $('.cc-gallery-link').on('click', function() {
        var loc_lang = get_loc_lang();
        $.ajax({
            url: loc_lang + '/gallery/photo/' + $(this).data('id') + '/',
            type: 'get',
            success: function(data) {
                $('#cc-gallery-content').html(data.html);
            }
        });
        $.ajax({
            url: loc_lang + '/gallery/photo_buy/' + $(this).data('id') + '/',
            type: 'get',
            success: function(data) {
                $('#cc-gallery-buy').html(data.html);
            }
        });
    });

    var open_form = 0;
    var region_id = 0;
    var city_id = 0;
    var warehouse_id = 0;

    $('#cc-cart-checkout').on('click', function() {
        if ($(this).data('ready') == 1) {
            var type = 'post';
            var data = $('#cc-checkout-form').serialize();
        } else {
            var type = 'get';
            var data = {};
        }

        var loc_lang = get_loc_lang();

        $.ajax({
            url: loc_lang + '/cart/checkout/',
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
                        if (data.payment) {
                            // $('#payment-form').html(data.payment_form);
                            // $('#payment-form form').submit();
                            $('#cc-cart-modal').modal('hide');
                            var wayforpay = new Wayforpay();
                            var pay = function () {
                                wayforpay.run({
                                        merchantAccount : data.payment.account,
                                        merchantDomainName : data.payment.domain,
                                        merchantTransactionType: data.payment.tr_type,
                                        authorizationType : data.payment.auth_type,
                                        merchantSignature : data.payment.sign,
                                        serviceUrl: data.payment.url,
                                        orderReference : data.payment.order_id,
                                        orderDate : data.payment.order_date,
                                        amount : data.payment.amount,
                                        currency : data.payment.currency,
                                        productName : data.payment.products,
                                        productPrice : data.payment.prices,
                                        productCount : data.payment.counts,
                                        clientFirstName : data.payment.first_name,
                                        clientLastName : data.payment.last_name,
                                        clientPhone: data.payment.phone,
                                        language: data.payment.lang,
                                        straightWidget: true
                                    },
                                    function (response) {

                                    },
                                    function (response) {

                                    },
                                    function (response) {

                                    }
                                );
                            }
                            pay();
                        } else {
                            location.reload();
                        }
                    }
                };
                if (open_form == 0) {
                    open_form = 1;
                    checkoutform(0);
                };
                if ($('#id_delivery_1').prop('checked')) {checkoutform(1); set_cities(); set_warehouses(); set_comment();};
                if ($('#id_delivery_2').prop('checked')) {checkoutform(2);};
                if ($('#id_delivery_3').prop('checked')) {checkoutform(3);};
                if ($('#id_delivery_4').prop('checked')) {checkoutform(4);};
                if ($('#id_delivery_5').prop('checked')) {checkoutform(5);};
                $('#cc-cart-cancel').hide();
            }
        });

    });

    $('#cc-cart-cancel').on('click', function() {
        location.reload();
    });

    $('body').on('click', '.cc-cart-remove', function(e) {
        e.preventDefault();
        var loc_lang = get_loc_lang();

        $.ajax({
            url: loc_lang + '/cart/' + $(this).data('id') + '/remove/',
            type: 'post',
            success: function(data) {
                $('#cc-cart-content').html(data.html);
                $('#cc-cart-total').html(data.count);
                $('#cc-cart-cancel').show();
            },
        });
    });

    $('body').on('click', '.cc-cart-amount-plus', function(e) {
        e.preventDefault();
        var loc_lang = get_loc_lang();

        $.ajax({
            url: loc_lang + '/cart/' + $(this).data('id') + '/plus/',
            type: 'post',
            success: function(data) {
                $('#cc-cart-content').html(data.html);
                $('#cc-cart-total').html(data.count);
                $('#cc-cart-cancel').show();
            },
        });
    });

    $('body').on('click', '.cc-cart-amount-minus', function(e) {
        e.preventDefault();
        var loc_lang = get_loc_lang();

        $.ajax({
            url: loc_lang + '/cart/' + $(this).data('id') + '/minus/',
            type: 'post',
            success: function(data) {
                $('#cc-cart-content').html(data.html);
                $('#cc-cart-total').html(data.count);
                $('#cc-cart-cancel').show();
            },
        });
    });

    $('body').on('click', '.cc-cart-remove-set', function(e) {
        e.preventDefault();
        var loc_lang = get_loc_lang();

        $.ajax({
            url: loc_lang + '/cart/' + $(this).data('id') + '/remove_set/',
            type: 'post',
            success: function(data) {
                $('#cc-cart-content').html(data.html);
                $('#cc-cart-total').html(data.count);
                $('#cc-cart-cancel').show();
            },
        });
    });

    var sourceSwap = function () {
        var $this = $(this);
        var newSource = $this.data('hover-src');
        $this.data('hover-src', $this.attr('src'));
        $this.attr('src', newSource);
    }

    $('.cc-cat-image').hover(sourceSwap, sourceSwap);
    $('.cc-cat-image0').hover(sourceSwap, sourceSwap);
    $('.cc-gallery').hover(sourceSwap, sourceSwap);

    var showcaseSwap = function () {
        var $this = $(this);
        var newSource = $this.data('hover-src');
        $this.data('hover-src', $this.attr('src'));
        $this.attr('src', newSource);
    }

    $('.cc-logo-button').hover(showcaseSwap, showcaseSwap);

    $('#cc-pics').flexslider({
        animation: "slide",
        controlNav: false
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

    $(document).on('click', '#cc-unsubscribe', function(e) {
        e.preventDefault;

        $.ajax({
            url: $(this).attr('href'),
            type: 'post',
            success: function(data) {
                $('#cc-messages').html(data.message)
            }
        });
    });

    function set_comment() {
        $('#id_shipping').val($('#id_region_np  option:selected').text() + ' обл, ' + $('#id_city_np  option:selected').text() + ', ' + $('#id_warehouse_np  option:selected').text());
    };

    function set_warehouses() {
        var city_id = $('#id_city_np').val();
        var loc_lang = get_loc_lang();
        if (city_id != '') {
            $.ajax({
                url: loc_lang + '/cart/' + city_id + '/' + warehouse_id + '/warehouses/',
                type: 'post',
                success: function(ajax_data) {
                    $('#id_warehouse_np').empty();
                    for (i = 0; i < ajax_data.warehouses.length; i++) {
                        var data = {id: ajax_data.warehouses[i][0], text: ajax_data.warehouses[i][1], active: ajax_data.warehouses[i][2]};
                        var newOption = new Option(data.text, data.id, data.active, data.active);
                        $('#id_warehouse_np').append(newOption).trigger('change');
                    };
                    set_comment();
                    warehouse_id = $('#id_warehouse_np').val();
                },
            });
        };
    };

    function set_cities() {
        var region_id = $('#id_region_np').val();
        var loc_lang = get_loc_lang();
        if (region_id != '') {
            $.ajax({
                url: loc_lang + '/cart/' + region_id + '/' +city_id + '/cities/',
                type: 'post',
                success: function(ajax_data) {
                    $('#id_city_np').empty();
                    for (i = 0; i < ajax_data.cities.length; i++) {
                        var data = {id: ajax_data.cities[i][0], text: ajax_data.cities[i][1], center: ajax_data.cities[i][2]};
                        var newOption = new Option(data.text, data.id, data.center, data.center);
                        $('#id_city_np').append(newOption).trigger('change');
                    };
                     set_comment();
                    city_id = $('#id_city_np').val();
                },
            });
            set_warehouses();

        }
    };

    $(document).on('change', '#id_region_np', function(e) {
        city_id = 0;
        warehouse_id = 0;
        set_cities();
    });

    $(document).on('change', '#id_city_np', function(e) {
        if (city_id != $('#id_city_np').val()) {
            city_id = $('#id_city_np').val();
            set_warehouses();
        };
    });

    $(document).on('change', '#id_warehouse_np', function(e) {
        if (warehouse_id != $('#id_warehouse_np').val()) {
            set_comment();
            warehouse_id = $('#id_warehouse_np').val();
        };
    });

    checkoutform_hide = [['#div_id_shipping', '#div_id_country', '#div_id_email', '#div_id_region_np', '#div_id_city_np', '#div_id_warehouse_np'],
                         ['#div_id_shipping', '#div_id_country', '#div_id_email'],
                         ['#div_id_country', '#div_id_email', '#div_id_region_np', '#div_id_city_np', '#div_id_warehouse_np'],
                         ['#div_id_region_np', '#div_id_city_np', '#div_id_warehouse_np'],
                         ['#div_id_shipping', '#div_id_country', '#div_id_email', '#div_id_region_np', '#div_id_city_np', '#div_id_warehouse_np'],
                         ['#div_id_shipping', '#div_id_country', '#div_id_email', '#div_id_region_np', '#div_id_city_np', '#div_id_warehouse_np']
                        ];

    checkoutform_show = [[],
                         ['#div_id_region_np', '#div_id_city_np', '#div_id_warehouse_np'],
                         ['#div_id_shipping'],
                         ['#div_id_country', '#div_id_email', '#div_id_shipping'],
                         [],
                         ['#div_id_shipping']
                        ];

    function checkoutform(i) {
        for (j = 0; j < checkoutform_hide[i].length; j++) {
            $(checkoutform_hide[i][j]).hide();
        };
        for (j = 0; j < checkoutform_show[i].length; j++) {
            $(checkoutform_show[i][j]).show();
        };
        if (i<3) {
            $('#id_payment_3').parent().show();
            $('#id_payment_4').parent().show();
        } else {
            $('#id_payment_3').parent().hide();
            $('#id_payment_4').parent().hide();
        };

    }

    $(document).on('click', '#id_delivery_1', function(e) {
        checkoutform(1);
        set_warehouses();
        set_comment();
    });

    $(document).on('click', '#id_delivery_2', function(e) {
        checkoutform(2);
        $('#id_shipping').val('');
    });

    $(document).on('click', '#id_delivery_3', function(e) {
        checkoutform(3);
        $('#id_shipping').val('');
    });

    $(document).on('click', '#id_delivery_4', function(e) {
        checkoutform(4);
        $('#id_shipping').val('Из магазина');
    });

     $(document).on('click', '#id_delivery_5', function(e) {
        checkoutform(5);
        $('#id_shipping').attr("placeholder", "Укажите город и номер отделения Justin");
    });

    window.addEventListener('message', function (e) {
      if (e.data == 'WfpWidgetEventClose') {
        location.reload();
      }
    }, false);

  const page_lang = document.documentElement.lang;
  var cookie_message = 'Этот веб-сайт использует файлы cookie. Используя этот веб-сайт, вы соглашаетесь на использование этих файлов cookie.';
  var cookie_consentMessage = 'Я понимаю';

  if (page_lang === 'uk') {
    cookie_message = 'Цей веб -сайт використовує файли cookie. Використовуючи цей веб -сайт, ви даєте згоду на використання нами цих файлів cookie.';
    cookie_consentMessage = 'Я розумію';
  };

  if (page_lang === 'en') {
    cookie_message = 'This website uses cookies. By using this website, you agree to the use of these cookies.';
    cookie_consentMessage = 'I accept';
  };

  $('#cookieConsent').cookieConsent({
    message: cookie_message,
    consentMessage: cookie_consentMessage,
//    style: 'color:Tomato;',
    consentStyle: 'font-weight:bold;'
  });

//    initialize();
});
