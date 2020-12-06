"use strict";
const urlParams = new URLSearchParams(window.location.search);
const recallid = urlParams.get('recallid');
const Toast_2 = Swal.mixin({
    toast: true,
    title: 'Änderung speichern?',
    position: 'bottom-end',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Speichern',
    cancelButtonText: 'Verwerfen'
});
const cons = new Constraints(recallid);

jQuery(document).ready(function ($) {
    if(recallid == "new"){
        $('.new-hide').hide();
    }
    badge('initial');
    $('.badge').click(function(){
        var id = $(this).data('con')
        var type = $(this).data('contype')
        $(this).toggleClass('badge-success')
        $(this).toggleClass('badge-secondary')
        badge();
    });
    $('.input-con-form').change(function(){
        var index = $(this).data('index');
        var field = $(this).data('field');
        var val = $(this).val();
        if(val==""){
            val = null;
        };
        cons.change(index,field,val);
        cons.print();
        Toast_2.fire().then((result) => {
            if(result.value==true){
                cons.save();
            }else{
                window.location.reload();
            }
        });
    });
    $('.uncol-con').click(function(){
        $(this).parents('.row-div').toggleClass('collapse-cons');
        $(this).toggleClass('uncol-con');
        $(this).toggleClass('coll-con');
    });
    $('.btn-new-constraint').click(function(){
        var url = window.location.protocol + "//" + window.location.host + '/api/v1/constraint/' + recallid;
        ajax_call(url, {}, 'POST');
    });
    $('.delete-con').click(function(){
        var id = $(this).data('con');
        var url = window.location.protocol + "//" + window.location.host + '/api/v1/constraint/' + recallid + '?Constraint_ID=' + id;
        Swal.fire({
            title: 'Datensatz löschen',
            text: 'Soll der ausgewählte Datensatz wirklich gelöscht werden',
            showCancelButton: true,
            confirmButtonText: `Ja`,
            cancelButtonText: `Abbrechen`,
        }).then((result) => {
            if (result.value == true) {
               ajax_call(url,{},'DELETE');
            }
        });
    })
    $('.form-recall-detail').change(function () {
        $('.delete-btn').addClass('hide');
        $('.cancel-btn').removeClass('hide');
        $('.save-btn').removeClass('hide');
        $('.new-btn').addClass('hide');
    });
    $('.cancel-btn').click(function () {
        $('.form-recall-detail').trigger('reset');
        $('.delete-btn').removeClass('hide');
        $('.cancel-btn').addClass('hide');
        $('.save-btn').addClass('hide');
        $('.new-btn').removeClass('hide');
    });
    $('.new-btn').click(function(){

    });
    $('.btn-create-vlist').click(function(){
        blur();
        var url = window.location.protocol + "//" + window.location.host + '/api/v1/run_rules/' + recallid;
        $.ajax({
            headers: { "X-CSRFToken": jQuery("[name=csrfmiddlewaretoken]").val() },
            type: 'GET',
            url: url,
            success: function (result, status, xhr) {
                unblur();
                fill_vr_table();
                $('.div-vrt').removeClass('hide');
                Toast.fire({
                    icon: 'success',
                    title: 'Fahrzeugliste wurde angelegt'
                });
            },
            error: function (result, status, xhr) {
                unblur();
                Toast.fire({
                    icon: 'error',
                    title: 'Fehler'
                });
            },
            timeout: 120000,
        });
    });
    $('.save-btn').click(function(){
        var url = window.location.protocol + "//" + window.location.host + '/api/v1/recall/' + recallid
        if(recallid=='new'){
            ajax_call(url, collect(), 'POST', back() );
        }else{
            ajax_call(url, collect(), 'PUT');
        }
    })
    $('.asbtn-delete-doc').click(function(){
        var url = window.location.protocol + "//" + window.location.host + '/api/v1/recalldoc/' + $(this).attr('data-doc_id')
        ajax_call(url,{},'DELETE');
    })
});

function badge(mode=null){
    if(mode!=null){
        $('.badge-success').each(function () {
            var id = $(this).data('con')
            var type = $(this).data('contype')
            $('form[data-con="' + id + '"]').find('#' + type).removeClass('hide');
        })
        $('.badge-secondary').each(function () {
            var id = $(this).data('con')
            var type = $(this).data('contype')
            $('form[data-con="' + id + '"]').find('#' + type).addClass('hide');
        })
    }else{
        $('.badge-success').each(function () {
            var id = $(this).data('con')
            var type = $(this).data('contype')
            $('form[data-con="' + id + '"]').find('#' + type).removeClass('hide');
        })
        $('.badge-secondary').each(function () {
            var id = $(this).data('con')
            var type = $(this).data('contype')
            var index = $(this).data('index');
            cons.delete_group(index, type);
            Toast_2.fire().then((result) => {
                if (result.value == true) {
                    cons.save();
                } else {
                    window.location.reload();
                }
            });
            $('form[data-con="' + id + '"]').find('#' + type).addClass('hide');
            $('form[data-con="' + id + '"]').find('#' + type).find('input').val('');
        });
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
            }).then(function () {
                window.location.reload();
            });
            if (callback) callback();
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

function collect(){
    var data = {
        "Recall_ID": recallid,
        "Recall_CODE": $('#id_Recall_CODE').val(),
        "Recall_NAME": $('#id_Recall_NAME').val(),
        "Recall_DESCRIPTION": $('#id_Recall_DESCRIPTION').val(),
        "Recall_START_DATE": $('#id_Recall_START_DATE').val(),
        "Recall_PLANNED_COMPLETATION_DATE": $('#id_Recall_PLANNED_COMPLETATION_DATE').val(),
        "Recall_STATUS": $('#id_Recall_STATUS').val(),
        "Recall_DATE_COMPLETED": $('#id_Recall_DATE_COMPLETED').val()
    }
    return data
}

function fill_vr_table(){
    "use strict";
    var rtbl = null;
    rtbl = $('#vehicle_recall_tbl').DataTable({
        responsive: true,
        stateSave: false,
        select: 'single',
        ajax: {
            url: '/api/v1/vehiclelist_per_recall/' + recallid,
            dataSrc: 'data',
        },
        "info": true,
        "processing": true,
        "ordering": true,
        "searching": true,
        "language": {
            "emptyTable": "Keine Daten verfügbar",
            "info": "Angezeigt werden _START_ bis _END_ von _TOTAL_ Einträge",
            "infoEmpty": "Keine Daten verfügbar",
            "infoFiltered": "(gefiltert von _MAX_ Einträgen)",
            "thousands": ".",
            "lengthMenu": "_MENU_ Einträge pro Seite",
            "search": "Suche",
            "paginate": {
                "first": "Erste",
                "last": "Letzte",
                "next": "Vor",
                "previous": "Zurück"
            },
        },
        "columns": [
            {
                "data": 'Vehicle_Recall_ID',
                "title": "ID"
            },
            {
                "data": 'Vehicle.Vehicle_VIN',
                "title": "FIN"
            },
            {
                "data": 'Vehicle.Vehicle_PLATE',
                "title": "Kennzeichen"
            },
            {
                "data": 'Vehicle.Vehicle_MAKE',
                "title": "Hersteller"
            },
            {
                "data": 'Vehicle.Vehicle_MODEL',
                "title": "Modell"
            },
            {
                "data": 'Vehicle.Vehicle_FIRST_REGISTRATION_DATE',
                "title": "EZ",
                "render": function (value) {
                    if (value === null) return "";
                    return moment(value).format('DD.MM.YYYY');
                }
            },
            {
                "data": 'VR_STATUS',
                "title": "Status",
                "render": function (value) {
                    if (value === 0) return "Offen";
                    if (value === 1) return "Vorbelegt";
                    if (value === 2) return "Abgeschlossen";
                }
            },
            {
                "data": 'VR_DATE_CREATED',
                "title": "Anlagedatum",
                "render": function (value) {
                    if (value === null) return "";
                    return moment(value).format('DD.MM.YYYY');
                }
            },
            {
                "data": 'VR_DATE_COMPLETED',
                "title": "Fertigstellungsdatum",
                "render": function (value) {
                    if (value === null) return "";
                    return moment(value).format('DD.MM.YYYY');
                }
            },
        ]
    });
}

function blur(){
    var $markup = $("<div class='blur'>" + 
                        "<div class='blur-loader'" +
                        "</div>" +
                    "</div>"
    );
    $('body').append($markup);
    $markup.find('.blur-loader').append(Loader);
};
function unblur() {
    $('body').find('.blur').remove();
};
function back(){
    window.location.href = '/stammdaten/';
}

