/*
    Intended to store all main functions
*/

$(function() {

    $("#lang_nav li a").on('click', function() {
        var lang = $(this).data('lang');
        var lang_url = $('#lang_nav').data('setlang-url');
        // console.log("Set language", lang);
        $.ajax({
            url: lang_url,
            type: 'POST',
            dataType: 'html',
            data: {language: lang},
            success: function(data){
                window.location.reload();
            },
            error: function(){
               console.error("Failed to switch language: ", arguments);
            }
        });
        return false;
    });

});
