"use strict";

jQuery(document).ready(function ($) {
    $('.recall-tr').click(function(){
        var recall_id = "recall-" + $(this).attr("id");
        $('.recall-detail-wrapper').removeClass('hide');
        $('.recall-detail-div').addClass('hide');
        $('#' + recall_id).toggleClass('hide');
        scroll_down();
    });
    $('.fa-times-circle').click(function(){
        $(this).parents('.recall-detail-wrapper').addClass('hide');
    })
    $('.recall-update-btn').click(function(){
        var recall_id = $(this).attr("data-recall-id");
        var url = window.location.protocol + "//" + window.location.host + '/api/v1/vehicle_recall/' + recall_id
        ajax_call(url, { 'VR_STATUS': 1},'PATCH',close_modal());
    });
    $('.recall-reject-btn').click(function () {
        var recall_id = $(this).attr("data-recall-id");
        var url = window.location.protocol + "//" + window.location.host + '/api/v1/vehicle_recall/' + recall_id
        ajax_call(url, { 'VR_STATUS': 0 }, 'PATCH', close_modal());
    });
    $('.btn-submit-note').click(function () {
        var url = window.location.protocol + "//" + window.location.host + '/api/v1/note/new'
        ajax_call(url, compose_note(), 'POST', close_modal());
    });
    $('.btn-delete-note').click(function () {
        var note_id = ntbl.rows({ selected: true }).data()[0][0];
        var url = window.location.protocol + "//" + window.location.host + '/api/v1/note/' + note_id
        ajax_call(url, {}, 'DELETE', close_modal());
    });
});

function scroll_down(){
    $('.main-content').animate({
        scrollTop: $(document).height() +200
    },'slow');
    return false
}

function close_modal(){
    $('.modal').modal('hide');
}

function compose_note(){
    var content = $('#new-note-content').val()
    var odo = $('#new-note-odometer').val()
    var veh = $('.btn-submit-note').data('vehicle')

    odo = odo.replace('.', '')
    odo = odo.replace(',','')

    return { 
        "Note_TEXT": content,
        "Note_ODOMETER": odo,
        "Vehicle": veh
    }

}


function ajax_call(api_url = "", api_data, api_method, callback) {
        $.ajax({
            headers: { "X-CSRFToken": jQuery("[name=csrfmiddlewaretoken]").val() },
            type: api_method,
            data: api_data,
            url: api_url,
            success: function (result, status, xhr) {
                Toast.fire({
                    icon: 'success',
                    title: 'Änderung gespeichert'
                }).then(function(){
                    window.location.reload();
                });
                if(callback) callback();
            },
            error: function (result, status, xhr) {
                Toast.fire({
                    icon: 'error',
                    title: 'Änderung konnte nicht gespeichert werden'
                });
            },
            timeout: 120000,
        });
    }