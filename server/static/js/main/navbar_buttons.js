'use strict';

$(document).ready(function () {

    /**
     * Opens the logout modal window.
     */
    $('.button-logout').click(function () {
        openModalAnimation();
        $('#modal_window_logout').css(DISPLAY_FLEX);
    });

    /**
     * Close the logout modal window
     */
    $('#modal_window_logout_button_close').click(function () {
        closeModalAnimation();
        setTimeout(function () {
            $('#modal_window_logout').css(DISPLAY_NONE);
        }, 400);

    });
});