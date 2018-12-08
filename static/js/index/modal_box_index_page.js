"use strict";
const MODAL_ADD_DEVICE = ".modal-add-device";
const MODAL_CLOSE_DEVICE = ".modal-close-deviсe";
const MODAL_DEVICE = ".modal-device";
const MODAL = ".modal";

$(document).ready(function () {
    /*
     * On a click we open a modal window
    */
    $(MODAL_ADD_DEVICE).click(function () {
        $(MODAL).removeClass("modal-animation-close");
        $(MODAL).addClass("modal-animation-open");
        $(MODAL_DEVICE).css(DISPLAY_FLEX);
    });
    /*
     * By clicking the close button in the modal window we close the window
    */
    $(MODAL_CLOSE_DEVICE).click(function () {
        $(MODAL).removeClass("modal-animation-open");
        $(MODAL).addClass("modal-animation-close");
        setTimeout(function () {
            $(MODAL_DEVICE).css(DISPLAY_NONE);
        },500);
    });

});
