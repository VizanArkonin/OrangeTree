"use strict";
const COLOR_WHITE = {"color":"rgb(255, 255, 255)"};
const COLOR_YELLOW = {"color":"rgba(255, 195, 31, 1)"};
/**
 * The written script is used for auxiliary functions of the styles index page
 */
$(document).ready(function () {
    $(table.device.tab).click(function () {
        $(table.user.window).css(DISPLAY_NONE);
        $(table.device.window).css(DISPLAY_FLEX);
        $(table.device.tab).css(COLOR_YELLOW);
        $(table.user.tab).css(COLOR_WHITE);
    });

    $(table.user.tab).click(function () {
        $(table.device.window).css(DISPLAY_NONE);
        $(table.user.window).css(DISPLAY_FLEX);
        $(table.user.tab).css(COLOR_YELLOW);
        $(table.device.tab).css(COLOR_WHITE);
    });
});

