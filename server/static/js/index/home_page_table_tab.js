"use strict";
const TAB_LINK_DEVICES = ".tab-link-devices";
const TAB_LINK_USERS = ".tab-link-users";
const DEVICES = ".devices";
const USERS = ".users";
const DISPLAY_NONE = {"display":"none"};
const DISPLAY_FLEX = {"display":"flex"};
const BG_DARK_400 = {"background":"rgba(0, 0, 0, 0.4)"};
const BG_DARK_700 = {"background":"rgba(0, 0, 0, 0.7)"};
/**
 * The written script is used for auxiliary functions of the styles index page
 */
$(document).ready(function () {
    $(TAB_LINK_DEVICES).click(function () {
        $(USERS).css(DISPLAY_NONE);
        $(DEVICES).css(DISPLAY_FLEX);
        $(TAB_LINK_DEVICES).css(BG_DARK_400);
        $(TAB_LINK_USERS).css(BG_DARK_700);
    });

    $(TAB_LINK_USERS).click(function () {
        $(DEVICES).css(DISPLAY_NONE);
        $(USERS).css(DISPLAY_FLEX);
        $(TAB_LINK_USERS).css(BG_DARK_400);
        $(TAB_LINK_DEVICES).css(BG_DARK_700);
    });
});

