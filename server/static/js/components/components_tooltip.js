"use strict";

$(document).ready(function () {
    /**
     * The function opens a tooltip, and closes after 3 seconds
     */
    $('.tooltip-desktop-on').on('click', function () {
        let tooltipLocator = $(this);

        $(tooltipLocator).prev().css('visibility','visible');
        setTimeout(function () {
            $(tooltipLocator).prev().css('visibility','hidden');
        }, 3000);
    });
});

