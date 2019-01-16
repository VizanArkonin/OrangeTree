"use strict";
const DISPLAY_TABLE = {"display":"table"};
const DEVICE_PRELOADER = '#table_device_preloader';
const USERS_PRELOADER = '#table_users_preloader';


function beforeLoadTableDevice () {
    $(TABLE_DEVICES).css(DISPLAY_NONE);
    $(DEVICE_PRELOADER).css(DISPLAY_FLEX);
}

function afterLoadTableDevice () {
    setTimeout(function () {
        $(DEVICE_PRELOADER).css(DISPLAY_NONE);
        $(TABLE_DEVICES).fadeIn(600);
    }, 400);
}

function beforeLoadTableUsers () {
    $(TABLE_USERS).css(DISPLAY_NONE);
    $(USERS_PRELOADER).css(DISPLAY_FLEX);
}

function afterLoadTableUsers () {
    setTimeout(function () {
        $(USERS_PRELOADER).css(DISPLAY_NONE);
        $(TABLE_USERS).fadeIn(600);
    }, 400);
}
