"use strict";

const Toast = Swal.mixin({
    toast: true,
    position: 'bottom-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    onOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
});
const Loader = $("<div class='loader'></div>");

jQuery(document).ready(function ($) {
    $('[data-toggle="tooltip"]').tooltip()
    $('a#logout').click(function(){
        window.location = '/logout'
    });
    $('a#login').click(function () {
        window.location = '/login'
    });
    $('.sidebar, .sidebar-ghost').mouseenter(function(){
        $('.sidebar').removeClass('sb-collapse');
        $('.icon-text').removeClass('sp-collapse');
    });
    $('.sidebar').mouseleave(function () {
        $('.sidebar').addClass('sb-collapse');
        $('.icon-text').addClass('sp-collapse');
        $('.sub-menu').addClass('ul-collapse');
        $('.sub-menu-arr').removeClass('active');
    });
    $('.sidebar-a').mouseenter(function(){
        $(this).children().addClass('hover-wh');
    })
    $('.sidebar-a').mouseleave(function () {
        $(this).children().removeClass('hover-wh');
    })
    $('.li-sub').click(function(){
        $(this).find('.sub-menu-arr').toggleClass('active');
        $(this).next('.sub-menu').toggleClass('ul-collapse');
    });
    $('#toggle-search-type').click(function(){
        $('.toggle-text').toggleClass('active disable');
        $('.vehicle-search-form-wrapper').slideUp('slow', function(){
            $('.form-vehicle-search').trigger('reset');
            $('.form-vehicle-search').toggleClass('active disable');
            $('.vehicle-search-form-wrapper').slideDown('slow')
        });
    });
    $('a#link-search').click(function(){
        window.location = '/search'
    });
    $('a#link-master-data').click(function(){
        window.location = '/stammdaten'
    });
    $('a#link-tsi').click(function(){
        window.location = '/tis'
    })
});


