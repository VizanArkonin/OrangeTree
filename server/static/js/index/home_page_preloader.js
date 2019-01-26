"use strict";
const DEVICE_PRELOADER = '#table_device_preloader';
const USERS_PRELOADER = '#table_users_preloader';

/**
 * Preloader launch function (for devises)
 */
function showLoaderInDevicesTable () {
    $(TABLE_DEVICES).css(DISPLAY_NONE);
    $(DEVICE_PRELOADER).css(DISPLAY_FLEX);
}

/**
 * Preloader hide function (for devises)
 */
function hideLoaderInDevicesTable () {
    setTimeout(function () {
        $(DEVICE_PRELOADER).css(DISPLAY_NONE);
        $(TABLE_DEVICES).fadeIn(600);
    }, 400);
}

/**
 * Preloader launch function (for devises)
 */
function showLoaderInUsersTable () {
    $(TABLE_USERS).css(DISPLAY_NONE);
    $(USERS_PRELOADER).css(DISPLAY_FLEX);
}

/**
 * Preloader hide function (for devises)
 */
function hideLoaderInUsersTable () {
    setTimeout(function () {
        $(USERS_PRELOADER).css(DISPLAY_NONE);
        $(TABLE_USERS).fadeIn(600);
    }, 400);
}
