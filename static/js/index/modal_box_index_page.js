"use strict";
const MODAL_ADD_DEVICE = ".modal-add-device";
const MODAL_EDIT_DEVICE = ".modal-edit-device";
const MODAL_CLOSE_ADD_DEVICE = ".modal-close-add-deviсe";
const MODAL_CLOSE_EDIT_DEVICE = ".modal-close-edit-deviсe";
const CONTAINER_DEVICE_ADD = ".container-device-add";
const CONTAINER_DEVICE_EDIT = ".container-device-edit";
const MODAL = ".modal";
let setTime = 500;

$(document).ready(function () {

    function openModalAnimation () {
        $(MODAL).removeClass("modal-animation-close");
        $(MODAL).addClass("modal-animation-open");
    }

    function closeModalAnimation () {
        $(MODAL).removeClass("modal-animation-open");
        $(MODAL).addClass("modal-animation-close");
    }

    /*
     * Script for modal window new/edit device
     */
    // Open modal window (add new device)
    $(MODAL_ADD_DEVICE).click(function () {
        openModalAnimation();
        $(CONTAINER_DEVICE_ADD).css(DISPLAY_FLEX);
    });
    // Open modal window (edit new device)
    $(MODAL_EDIT_DEVICE).click(function () {
       openModalAnimation();
        $(CONTAINER_DEVICE_EDIT).css(DISPLAY_FLEX);
    });
    // Close modal window (add new device)
    $(MODAL_CLOSE_ADD_DEVICE).click(function () {
        closeModalAnimation();
        setTimeout(function () {
            $(CONTAINER_DEVICE_ADD).css(DISPLAY_NONE);
            $("#device_id").val('');
            $("#device_key").val('');
            $("#device_type").val('1');
        },setTime);
    });
    // Close modal window (add new device)
    $(MODAL_CLOSE_EDIT_DEVICE).click(function () {
        closeModalAnimation();
        setTimeout(function () {
            $(CONTAINER_DEVICE_EDIT).css(DISPLAY_NONE);
            // $("#device_id").val('');
            // $("#device_key").val('');
            // $("#device_type").val('1');
        },setTime);
    });
    // Closes modal window when pressed outside the form.

});
