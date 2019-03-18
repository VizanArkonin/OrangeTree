'use strict';

$(document).ready(function () {
    /**
     * Opens the logout modal window.
     */
    $(modal.logout.button.open).click(function () {
        openModalAnimation();
        $(modal.logout.window).css(DISPLAY_FLEX);
    });

    /**
     * Close the logout modal window
     */
    $(modal.logout.button.close).click(function () {
        closeModalAnimation();
        setTimeout(function () {
            $(modal.logout.window).css(DISPLAY_NONE);
        }, 400);
    });
});