'use strict';

/**
 * Function (plugin) activation button
 */
$.fn.activeButton = function () {
    $(this).prop('disabled', false).addClass('button-active');
};

/**
 * Function (plugin) button deactivation
 */
$.fn.disabledButton = function () {
    $(this).prop('disabled', true).removeClass('button-active');
};