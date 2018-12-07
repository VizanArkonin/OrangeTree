"use strict";
const MODAL_ADD_DEVICE = "#modal-add-device";
const MODAL_DEVICE = "#modal-device";

$(document).ready(function () {
    $(MODAL_ADD_DEVICE).click(function () {
        $(MODAL_DEVICE).css(DISPLAY_FLEX);
    });
});
