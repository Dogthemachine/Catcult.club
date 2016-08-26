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

});