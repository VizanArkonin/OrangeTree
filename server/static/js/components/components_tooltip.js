"use strict";

$(document).ready(function () {
    /**
     * The function opens a tooltip, and closes after 3 seconds
     */
    $('.tooltip-desktop-on').on('click', function () {
        let tooltipLocator = $(this);

        $(tooltipLocator).prev().children('.tooltip-content').css('visibility','visible');
        setTimeout(function () {
            $(tooltipLocator).prev().children('.tooltip-content').css('visibility','hidden');
        }, 3000);
    });

    $('.tooltip-mobile-on').on('click', function () {
        let tooltipLocator = $(this);

        $(tooltipLocator).parent().prev().css(DISPLAY_BLOCK);
        setTimeout(function () {
            $(tooltipLocator).parent().prev().css(DISPLAY_NONE);
        }, 3000);
    });
});

