"use strict";
const BG_DARK_400 = {"background":"rgba(0, 0, 0, 0.4)"};
const BG_DARK_700 = {"background":"rgba(0, 0, 0, 0.7)"};
/**
 * The written script is used for auxiliary functions of the styles index page
 */
$(document).ready(function () {
    $(table.device.tab).click(function () {
        $(table.user.window).css(DISPLAY_NONE);
        $(table.device.window).css(DISPLAY_FLEX);
        $(table.device.tab).css(BG_DARK_400);
        $(table.user.tab).css(BG_DARK_700);
    });

    $(table.user.tab).click(function () {
        $(table.device.window).css(DISPLAY_NONE);
        $(table.user.window).css(DISPLAY_FLEX);
        $(table.user.tab).css(BG_DARK_400);
        $(table.device.tab).css(BG_DARK_700);
    });
});

