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

    //Moderation


     $('#cs-correction').on('click', function(e) {
          e.preventDefault();

          date_from = $("#cs-correction-date").val();

          $.ajax({
              url: '/correction/?date_from=' + date_from,
              type: 'get',
              success: function(data) {
                  if (data.success) {
                      $('#cs-correction-result').html(data.html);
                  }
              }
          });
     });

    //$('#cs-correction-date').datepicker();

    $('.cc-save-balance').on('click', function() {
        var balance = $(this).data('balance-id');
        var balance_amount = $('#cc-sizes-' + balance).val();
        var arrival = $("#cc-arrival-cb").prop("checked");
        $.ajax({
            url: 'update/',
            type: 'post',
            data: {'id': balance, 'amount': balance_amount, 'arrival': arrival},
            success: function(data) {
                if(data.success) {
                    $('#cc-mod-messages').html(
                        '<div class="alert alert-success">' +
                        '<button type="button" class="close" data-dismiss="alert">×</button>' +
                        data.message +
                        '</div>'
                    );
                } else {
                    $('#cc-mod-messages').html(
                        '<div class="alert alert-danger">' +
                        '<button type="button" class="close" data-dismiss="alert">×</button>' +
                        data.message +
                        '</div>'
                    );
                }
            }
        });
    });

    $('#cc-date-from').datetimepicker({
        format: 'YYYY-MM-DD'
    });

    $('#cc-date-to').datetimepicker({
        format: 'YYYY-MM-DD'
    });

    $('#cc-log-filter').on('click', function(e) {
        e.preventDefault();

        var date_from = $('#cc-date-from').val();
        var date_to = $('#cc-date-to').val();
        var arrival = $('#cc-arrival-cb').prop('checked')
        alert(arrival)

        location.search = '?date_from=' + date_from + '&date_to=' + date_to + '&arrival=' + arrival;
    });

    $('#cc-iwant-filter').on('click', function(e) {
        e.preventDefault();

        var date_from = $('#cc-date-from').val();
        var date_to = $('#cc-date-to').val();
//        var arrival = $("#cc-status-cb").prop("checked");
        var status = $("#cc-status-cb").val();

        location.search = '?date_from=' + date_from + '&date_to=' + date_to + '&status=' + status;
    });

    $('#cc-comments-filter').on('click', function(e) {
        e.preventDefault();

        var date_from = $('#cc-date-from').val();
        var date_to = $('#cc-date-to').val();
        var status = $("#cc-status-cb").val();

        location.search = '?date_from=' + date_from + '&date_to=' + date_to + '&status=' + status;
    });

    $('#cc-stat-sale-filter').on('click', function(e) {
        e.preventDefault();

        var date_from = $('#cc-date-from').val();
        var date_to = $('#cc-date-to').val();
        var payment = $('#cc-payment-stat').val();

        var loc_lang = window.location.toString().substr(window.location.toString().indexOf(window.location.host)
                       + window.location.host.toString().length + 1,2);
        e.preventDefault();
          $.ajax({
              url: '/' + loc_lang + '/stat/payment/',
              data: 'payment=' + payment,
              type: 'post',
              success: function() {
                  location.search = '?date_from=' + date_from + '&date_to=' + date_to + '&payment=' + payment;
              },
              error: function() {
              }
          });
    });

    $('.cc-order-update').on('click', function(e) {
        var id = $(this).data('id');
        var ttn_form = $('#cc-ttn-form-' + id);
        var delete_form = $('#cc-delete-form-' + id);
        var comment_form = $('#cc-comment-form-' + id);
        var statuses_form = $('#cc-statuses-form-' + id);

        if ($('#id_confirm', delete_form).is(':checked')) {
            console.log('gotcha!');
        }
    });

    $(document).on('click', '.cc-order-item-delete', function(e) {
        e.preventDefault();

        $.post({
            url: 'delete/' + $(this).data('id') + '/',
            success: function(data) {
                if (data.success) {
                    location.reload();
                } else {
                    $('#cc-mod-messages').html(
                        '<div class="alert alert-danger">' +
                        '<button type="button" class="close" data-dismiss="alert">×</button>' +
                        data.message +
                        '</div>'
                    );

                }
            }
        });
    });

    $('.cc-order-item-add').on('click', function(e) {
        e.preventDefault();
        var balance = $(this).data('balance-id');
        var balance_amount = $('#cc-order-balance-' + balance).val();
        $.ajax({
            url: 'add/' + balance + '/',
            type: 'post',
            data: {'amount': balance_amount},
            success: function(data) {
                if(data.success) {
                    location.reload();
                } else {
                    $('#cc-mod-messages').html(
                        '<div class="alert alert-danger">' +
                        '<button type="button" class="close" data-dismiss="alert">×</button>' +
                        data.message +
                        '</div>'
                    );
                }
            }
        });
    });

    $('.cc-iwant-comment').on('click', function(e) {
        e.preventDefault();
        var order = $(this).data('order-id');
        var comment = $('#cc-iwant-comment-' + order).val();
        $.ajax({
            url: 'change-comment/' + order + '/',
            type: 'post',
            data: {'comment': comment},
            success: function(data) {
                if(data.success) {
                } else {
                    $('#cc-mod-messages').html(
                        '<div class="alert alert-danger">' +
                        '<button type="button" class="close" data-dismiss="alert">×</button>' +
                        data.message +
                        '</div>'
                    );
                }
            }
        });
    });

    $('.cc-iwant-change').on('click', function(e) {
        e.preventDefault();
        var order = $(this).data('order-id');
        var status = $('#cc-iwant-status-' + order).val();
        $.ajax({
            url: 'change/' + order + '/',
            type: 'post',
            data: {'status': status},
            success: function(data) {
                if(data.success) {
                    location.reload();
                } else {
                    $('#cc-mod-messages').html(
                        '<div class="alert alert-danger">' +
                        '<button type="button" class="close" data-dismiss="alert">×</button>' +
                        data.message +
                        '</div>'
                    );
                }
            }
        });
    });

    $('.cc-iwant-delete').on('click', function(e) {
        e.preventDefault();
        var order = $(this).data('order-id');
        $.ajax({
            url: 'delete/' + order + '/',
            type: 'post',
            data: {'status': status},
            success: function(data) {
                if(data.success) {
                    location.reload();
                } else {
                    $('#cc-mod-messages').html(
                        '<div class="alert alert-danger">' +
                        '<button type="button" class="close" data-dismiss="alert">×</button>' +
                        data.message +
                        '</div>'
                    );
                }
            }
        });
    });

    $('.cc-comments-change').on('click', function(e) {
        e.preventDefault();
        var comment = $(this).data('comment-id');
        var status = $('#cc-comments-status-' + comment).val();
        $.ajax({
            url: 'change/' + comment + '/',
            type: 'post',
            data: {'status': status},
            success: function(data) {
                if(data.success) {
                    location.reload();
                } else {
                    $('#cc-mod-messages').html(
                        '<div class="alert alert-danger">' +
                        '<button type="button" class="close" data-dismiss="alert">×</button>' +
                        data.message +
                        '</div>'
                    );
                }
            }
        });
    });

    function doPoll(){
        $.get('/orders/check/', function(data) {
            if (data.new) {
                $('#cc-orders-link').html(
                    '<b><span class="icon-star"></span> ' + data.count + '</b>'
                );
            };
            if (data.iwant) {
                $('#cc-iwant-link').html(
                    '<b><span class="icon-radio-checked"></span> ' + data.iwant_count + '</b>'
                );
            };
            if (data.comm) {
                $('#cc-comm-link').html(
                    '<b><span class="icon-flickr"></span> ' + data.comm_count + '</b>'
                );
            };
            setTimeout(doPoll, 15000);
        });
    }

    doPoll();

//----------------------------------------------------------------------------------------------------------------------

    $('.cc-order-link').on('click', function() {
        $.ajax({
            url: $(this).data('order-id') + '/info/',
            type: 'get',
            success: function(data) {
                $('#cc-order-modal .modal-title').html(data.title);
                $('#cc-order-modal .modal-body').html(data.html);
                $('#cc-order-buttons').html(data.buttons);
            }
        });
    });

    $(document).on('click', '#cc-order-delete', function() {
        if (confirm('Удалить?')) {
            var order_id = $(this).data('order-id')

            $.ajax({
                url: order_id + '/delete/',
                type: 'post',
                success: function(data) {
                    $('#cc-order-' + order_id).remove();
                    $('#cc-order-modal').hide();
                    $('.modal-backdrop').remove();
                }
            });
        }
    });

    $('.cc-comment-link').on('click', function() {
        $.ajax({
            url: $(this).data('order-id') + '/comment/',
            type: 'get',
            success: function(data) {
                $('#cc-order-modal .modal-title').html(data.title);
                $('#cc-order-modal .modal-body').html(data.html);
                $('#cc-order-buttons').html(data.buttons);
            }
        });
    });

    $(document).on('click', '#cc-order-comment-save', function() {
        var order_id = $(this).data('order-id')

        $.ajax({
            url: order_id + '/comment/',
            type: 'post',
            data: $('#cc-order-comment-form').serialize(),
            success: function(data) {
                $('#cc-order-comment-' + order_id).html(data.html)
                $('#cc-order-modal').hide();
                $('.modal-backdrop').remove();
            }
        });
    });

    $(document).on('click', '.cc-delivery-link', function() {
        $.ajax({
            url: $(this).data('order-id') + '/delivery/',
            type: 'get',
            success: function(data) {
                $('#cc-order-modal .modal-title').html(data.title);
                $('#cc-order-modal .modal-body').html(data.html);
                $('#cc-order-buttons').html(data.buttons);
                $('#cc-order-delivery-form #id_date').datetimepicker({
                    format: 'DD.MM.YYYY'
                });
            }
        });
    });

    $(document).on('click', '#cc-order-delivery-save', function() {
        var order_id = $(this).data('order-id')

        $.ajax({
            url: order_id + '/delivery/',
            type: 'post',
            data: $('#cc-order-delivery-form').serialize(),
            success: function(data) {
                if (data.success) {
                    $('#cc-order-delivery-' + order_id).html(data.html)
                    $('#cc-order-modal').hide();
                    $('.modal-backdrop').remove();
                } else {
                    $('#cc-order-modal .modal-body').html(data.html);
                }
            }
        });
    });

    $(document).on('click', '#cc-order-delivery-reset', function() {
        var order_id = $(this).data('order-id')

        $.ajax({
            url: order_id + '/delivery/reset/',
            type: 'post',
            success: function(data) {
		console.log(data);
                if (data.success) {
                    $('#cc-order-delivery-' + order_id).html(data.html)
                    $('#cc-order-modal').hide();
                    $('.modal-backdrop').remove();
                }
            }
        });
    });

    $(document).on('click', '#cc-order-packed-save', function() {
        var order_id = $(this).data('order-id')
        $.ajax({
            url: order_id + '/packed/',
            type: 'post',
            data: $('#cc-order-delivery-form').serialize(),
            success: function(data) {
                if (data.success) {
                    $('#cc-order-delivery-' + order_id).html(data.html)
                    $('#cc-order-modal').hide();
                    $('.modal-backdrop').remove();
                } else {
                    $('#cc-order-modal .modal-body').html(data.html);
                }
            }
        });
    });

    $(document).on('click', '.cc-payment-link', function() {
        $.ajax({
            url: $(this).data('order-id') + '/payment/',
            type: 'get',
            success: function(data) {
                $('#cc-order-modal .modal-title').html(data.title);
                $('#cc-order-modal .modal-body').html(data.html);
                $('#cc-order-buttons').html(data.buttons);
            }
        });
    });

    $(document).on('click', '#cc-order-payment-save', function() {
        var order_id = $(this).data('order-id')

        $.ajax({
            url: order_id + '/payment/',
            type: 'post',
            data: $('#cc-order-payment-form').serialize(),
            success: function(data) {
                if (data.success) {
                    $('#cc-order-payment-' + order_id).html(data.html)
                    $('#cc-order-modal').hide();
                    $('.modal-backdrop').remove();
                } else {
                    $('#cc-order-modal .modal-body').html(data.html);
                }
            }
        });
    });

    $(document).on('click', '.cc-order-payment-delete', function() {
        var order_id = $(this).data('order-id')
        var payment_id = $(this).data('payment-id')

        $.ajax({
            url: 'payment/' + payment_id + '/delete/',
            type: 'post',
            success: function(data) {
                if (data.success) {
                    $('#cc-order-payment-sum-' + payment_id).remove();
                    $('#cc-order-payment-' + order_id).html(data.html)
                    $('#cc-order-modal .modal-body').html(data.modal_html);
                    $('#cc-order-buttons').html(data.buttons);
                }
            }
        });
    });

    $('#cs-balances').DataTable();

});
