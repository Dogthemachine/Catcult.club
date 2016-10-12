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

    $('#cs-balances').DataTable();

    $('.cc-save-balance').on('click', function() {
        var balance = $(this).data('balance-id');
        var balance_amount = $('#cc-sizes-' + balance).val();
        $.ajax({
            url: 'update/',
            type: 'post',
            data: {'id': balance, 'amount': balance_amount},
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

        location.search = '?date_from=' + date_from + '&date_to=' + date_to;
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


    function doPoll(){
        $.get('/orders/check/', function(data) {
            if (data.new) {
                $('#cc-orders-link').html(
                    '<b><span class="icon-star"></span> ' + data.count + '</b>'
                );
            }
            setTimeout(doPoll, 15000);
        });
    }

    doPoll();

});
