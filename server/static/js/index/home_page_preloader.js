"use strict";
const DEVICE_PRELOADER = '#table_device_preloader';
const USERS_PRELOADER = '#table_users_preloader';

// The function is intended to execute the script when sending an AJAX request.
function beforeLoadTableDevice () {
    $(TABLE_DEVICES).css(DISPLAY_NONE);
    $(DEVICE_PRELOADER).css(DISPLAY_FLEX);
}

// The function is designed to run the script when the AJAX request is completed (displays a preloader, smoothly displays the table data)
function afterLoadTableDevice () {
    setTimeout(function () {
        $(DEVICE_PRELOADER).css(DISPLAY_NONE);
        $(TABLE_DEVICES).fadeIn(600);
    }, 400);
}

// The function is intended to execute the script when sending an AJAX request.
function beforeLoadTableUsers () {
    $(TABLE_USERS).css(DISPLAY_NONE);
    $(USERS_PRELOADER).css(DISPLAY_FLEX);
}

// The function is designed to run the script when the AJAX request is completed (displays a preloader, smoothly displays the table data)
function afterLoadTableUsers () {
    setTimeout(function () {
        $(USERS_PRELOADER).css(DISPLAY_NONE);
        $(TABLE_USERS).fadeIn(600);
    }, 400);
}
