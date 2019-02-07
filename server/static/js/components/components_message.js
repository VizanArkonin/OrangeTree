'use strict';

/**
 * Function (plugin) сhanges message color to error color
 */
$.fn.useClassErrorMessage = function () {
    $(this).removeClass('success-message');
    $(this).addClass('error-message');
};

/**
 * Function (plugin) сhanges message color to success color
 */
$.fn.useClassSuccessMessage = function () {
    $(this).removeClass('error-message');
    $(this).addClass('success-message');
};