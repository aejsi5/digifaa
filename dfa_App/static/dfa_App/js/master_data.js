"use strict";
var $markup = null;
var robj = null;
var iknowyou = null;

jQuery(document).ready(function ($) {
    $('.fa-times-circle').click(function(){
        $('.slider-right').addClass('slider-collapse');
        $('.slider-content-wrapper').children().remove();
        iknowyou = null;
    })
    $('#btn-detail-recall').click(function () {
        window.location = '/produktverbesserung/?recallid=' + rid;
    });
    $('#btn-overview-recall').click(function(){
        if (iknowyou == null) {
            $('.slider-right').removeClass('slider-collapse');
            $('.slider-content-wrapper').append(Loader);
            slider_handler('recall', 'GET', rid)
        }
        if (iknowyou != rid){
            $('.slider-right').addClass('slider-collapse');
            $('.slider-content-wrapper').children().remove();
            window.setTimeout(function(){
                $('.slider-right').removeClass('slider-collapse');
            },200);
            $('.slider-content-wrapper').append(Loader);
            slider_handler('recall', 'GET', rid)
        }
    });
});

function slider_handler(resource, method, pk = null){
    if(resource=="recall"){
        ajax_call('/api/v1/recall/' + pk, '', method, recall_template);
        iknowyou = rid;
    }
}

function ajax_call(api_url = "", api_data, api_method, callback) {
    console.log(api_url);
    $.ajax({
        headers: { "X-CSRFToken": jQuery("[name=csrfmiddlewaretoken]").val() },
        type: api_method,
        data: api_data,
        url: api_url,
        success: function (result, status, xhr) {
            console.log(result)
            robj = result;   
            callback();       
        },
        complete: function (data) {
            $('.loader').remove();
            slider_vr_datatbl();
        },
        error: function (result, status, xhr) {
            Toast.fire({
                icon: 'error',
                title: 'Fehler'
            });
        },
        timeout: 120000,
    });
}

function recall_template(){
    $markup = $(
        '<h2 style="padding:15px;">Maßnahmenübersicht</h2>'+
        '<div class="container">' +
            '<form>' +
                '<div class="form-row">' +
                    '<div class="form-group col-md-6">' +  
                        '<label for="inputRecallCode">Code</label>' +
                        '<input type="text" class="form-control" id="inputRecallCode" placeholder="Code" disabled>' +
                    '</div>' +
                    '<div class="form-group col-md-6">' +
                        '<label for="inputRecallName">Name</label>' +
                        '<input type="text" class="form-control" id="inputRecallName" placeholder="Name" disabled>' +
                    '</div>' +
                '</div>' +
                '<div class="form-group">' +
                    '<label for="inputRecallDescription">Beschreibung</label>' +
                    '<textarea class="form-control" id="inputRecallDescription" placeholder="Beschreibung" disabled></textarea>' +
                '</div>' +
                '<div class="form-row">' +
                    '<div class="form-group col-md-4">' +
                        '<label for="inputRecallStartDate">Startdatum</label>' +
                        '<input type="date" class="form-control" id="inputRecallStartDate" placeholder="Startdatum" disabled>' +
                    '</div>' +
                    '<div class="form-group col-md-4">' +
                        '<label for="inputRecallPlannendCompletionDate">Abschlussdatum Soll</label>' +
                        '<input type="date" class="form-control" id="inputRecallPlannendCompletionDate" placeholder="Fertigstellungstermin Soll" disabled>' +
                    '</div>' +
                    '<div class="form-group col-md-4">' +
                        '<label for="inputRecallCompletionDate">Abschlussdatum Ist</label>' +
                        '<input type="date" class="form-control" id="inputRecallCompletionDate" placeholder="Fertigstellungstermin Ist" disabled>' +
                    '</div>' +
                '</div>' +
            '</form>' +
        '</div>'+
        '<div class="container slider-tbl-container">'+
        '<h4>Betroffene Fahrzeuge</h4>' +
            '<table class="data-tbl hover stripe row-border" id="slider_vehicle_recall_tbl">'+
                '<thead>' +
                    '<tr>' +
                        '<th>Vehicle_Recall_ID</th>'+
                        '<th>Vehicle_VIN</th>' +
                        '<th>Vehicle_MAKE</th>' +
                        '<th>Vehicle_MODEL</th>' +
                        '<th>VR_DATE_CREATED</th>' +
                        '<th>VR_DATE_COMPLETED</th>' +
                        '<th>VR_STATUS</th>' +
                    '</tr>' +
                '</thead>' +
            '</table>' +
        '</div>'

    );
    $('.slider-content-wrapper').append($markup);
    fill_recall();
};

function fill_recall(){
    $markup.find("#inputRecallCode").val(robj.Recall_CODE);
    $markup.find("#inputRecallName").val(robj.Recall_NAME);
    $markup.find("#inputRecallDescription").val(robj['Recall_DESCRIPTION']);
    $markup.find("#inputRecallStartDate").val(robj['Recall_START_DATE']);
    $markup.find("#inputRecallPlannendCompletionDate").val(robj['Recall_PLANNED_COMPLETATION_DATE']);
    $markup.find("#inputRecallCompletionDate").val(robj['Recall_DATE_COMPLETED']);
};

function slider_vr_datatbl(){
    var slider_vr_tbl = $('#slider_vehicle_recall_tbl').DataTable({
        responsive: true,
        stateSave: false,
        select: 'single',
        ajax: {
            url: '/api/v1/vehiclelist_per_recall/' + rid,
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
                "visible": false
            },
            {
                "data": 'Vehicle.Vehicle_VIN',
                "title": "FIN"
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
                "data": 'VR_DATE_CREATED',
                "title": "Anlagedatum",
                "render": function (value) {
                    if (value === null) return "";
                    return moment(value).format('DD.MM.YYYY');
                }
            },
            {
                "data": 'VR_DATE_COMPLETED',
                "title": "Abschlussdatum",
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
        ]
    });
};

