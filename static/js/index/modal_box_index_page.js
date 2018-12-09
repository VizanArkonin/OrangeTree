"use strict";
const MODAL_ADD_DEVICE = ".modal-add-device";
const MODAL_EDIT_DEVICE = ".modal-edit-device";
const MODAL_ADD_USER = ".modal-add-user";
const MODAL_EDIT_USER = ".modal-edit-user";
const MODAL_CLOSE_ADD_DEVICE = ".modal-close-add-deviсe";
const MODAL_CLOSE_EDIT_DEVICE = ".modal-close-edit-deviсe";
const MODAL_CLOSE_ADD_USER = ".modal-close-add-user";
const MODAL_CLOSE_EDIT_USER = ".modal-close-edit-user";
const CONTAINER_DEVICE_ADD = ".container-device-add";
const CONTAINER_DEVICE_EDIT = ".container-device-edit";
const CONTAINER_USER_ADD = ".container-user-add";
const CONTAINER_USER_EDIT = ".container-user-edit";
const MODAL = ".modal";

$(document).ready(function () {
    let setTime = 500;

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
    // Close modal window (edit device)
    $(MODAL_CLOSE_EDIT_DEVICE).click(function () {
        closeModalAnimation();
        setTimeout(function () {
            $(CONTAINER_DEVICE_EDIT).css(DISPLAY_NONE);
            // $("#device_id").val('');
            // $("#device_key").val('');
            // $("#device_type").val('1');
        },setTime);
    });

    /*
     * Script for modal window new/edit user
     */
    // Open modal window (add new user)
    $(MODAL_ADD_USER).click(function () {
        openModalAnimation();
        $(CONTAINER_USER_ADD).css(DISPLAY_FLEX);
    });
    // Open modal window (edit user)
    $(MODAL_EDIT_USER).click(function () {
       openModalAnimation();
        $(CONTAINER_USER_EDIT).css(DISPLAY_FLEX);
    });
    // Close modal window (add new user)
    $(MODAL_CLOSE_ADD_USER).click(function () {
        closeModalAnimation();
        setTimeout(function () {
            $(CONTAINER_USER_ADD).css(DISPLAY_NONE);
        },setTime);
    });
    // Close modal window (edit user)
    $(MODAL_CLOSE_EDIT_USER).click(function () {
        closeModalAnimation();
        setTimeout(function () {
            $(CONTAINER_USER_EDIT).css(DISPLAY_NONE);
        },setTime);
    });


});
