"use strict";
/**
 * Preloader launch function (for devises)
 */
function showLoaderInDevicesTable () {
    $(table.device.content).css(DISPLAY_NONE);
    $(table.device.preloader).css(DISPLAY_FLEX);
}

/**
 * Preloader hide function (for devises)
 */
function hideLoaderInDevicesTable () {
    setTimeout(function () {
        $(table.device.preloader).css(DISPLAY_NONE);
        $(table.device.content).fadeIn(600);
    }, 400);
}

/**
 * Preloader launch function (for devises)
 */
function showLoaderInUsersTable () {
    $(table.user.content).css(DISPLAY_NONE);
    $(table.user.preloader).css(DISPLAY_FLEX);
}

/**
 * Preloader hide function (for devises)
 */
function hideLoaderInUsersTable () {
    setTimeout(function () {
        $(table.user.preloader).css(DISPLAY_NONE);
        $(table.user.content).fadeIn(600);
    }, 400);
}
