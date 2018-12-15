"use strict";
// Variables with classes for buttons
const OPEN_MODAL_USER = ".open-modal-user";
const OPEN_MODAL_DEVICE = ".open-modal-device";
const CLOSE_MODAL = ".close-modal";
const TABLE_ROW = ".table-row";
//Other variables
const MODAL_ANIMATION_OPEN = "modal-animation-open";
const MODAL_ANIMATION_CLOSE = "modal-animation-close";
const MODAL = ".modal";
const MODAL_DEVICE = "#modal_device";
const MODAL_USER = "#modal_user";

$(document).ready(function () {

    let setTime = 500; // Set the delay time for the animation to work
    let rowSelected = false; // A helper variable to track the status of a row

    // Animation when opening a modal window
    function openModalAnimation () {
        $(MODAL).removeClass(MODAL_ANIMATION_CLOSE);
        $(MODAL).addClass(MODAL_ANIMATION_OPEN);
    }
    // Animation when closing a modal window
    function closeModalAnimation () {
        $(MODAL).removeClass(MODAL_ANIMATION_OPEN);
        $(MODAL).addClass(MODAL_ANIMATION_CLOSE);
    }

    // Opening modal windows to add a new / edit device
    $(OPEN_MODAL_DEVICE).click(function () {
        if ($(this).data("modal") === "add") {
            $("#modal_header_device").text("Add new device");
            $("#modal_device_id").attr("placeholder","Enter device ID");
            $("#modal_device_key").attr("placeholder","Enter device key");
            $("#modal_device_type").val("1");
            openModalAnimation();
            $(MODAL_DEVICE).css(DISPLAY_FLEX);
        }
        if ($(this).data("modal") === "edit" && rowSelected) {
            $("#modal_header_device").text("Edit device");
            $("#modal_device_id").attr("placeholder","Edit device ID");
            $("#modal_device_key").attr("placeholder","Edit device key");
            openModalAnimation();
            $(MODAL_DEVICE).css(DISPLAY_FLEX);
        }
    });

    // Opening modal windows to add a new / edit user
    $(OPEN_MODAL_USER).click(function () {
        if ($(this).data("modal") === "add") {
            $("#modal_header_user").text("Add new user");
            $("#modal_user_first_name").attr("placeholder","Enter First Name");
            $("#modal_user_last_name").attr("placeholder","Enter Last Name");
            $("#modal_user_email").attr("placeholder","Enter email");
            $("#modal_user_password").attr("placeholder","Enter password");
            $("#modal_user_confirm_password").attr("placeholder","Confirm password");
            openModalAnimation();
            $(MODAL_USER).css(DISPLAY_FLEX);
        }
        if ($(this).data("modal") === "edit" && rowSelected) {
            $("#modal_header_user").text("Edit user");
            $("#modal_user_first_name").attr("placeholder","Edit First Name");
            $("#modal_user_last_name").attr("placeholder","Edit Last Name");
            $("#modal_user_email").attr("placeholder","Edit email");
            $("#modal_user_password").attr("placeholder","Edit password");
            $("#modal_user_confirm_password").attr("placeholder","Confirm password");
            openModalAnimation();
            $(MODAL_USER).css(DISPLAY_FLEX);
        }
    });

    // Close all modal windows. With zeroing output
    $(CLOSE_MODAL).click(function () {
       if ($(this).data("modal") === "device") {
           closeModalAnimation();
           setTimeout(function () {
               $(MODAL_DEVICE).css(DISPLAY_NONE);
               $("#modal_device_id").val("");
               $("#modal_device_key").val("");
               $("#modal_device_type").val("1");
           }, setTime);
       } else {
           closeModalAnimation();
           setTimeout(function () {
               $(MODAL_USER).css(DISPLAY_NONE);
               $("#modal_user_first_name").val("");
               $("#modal_user_last_name").val("");
               $("#modal_user_email").val("");
               $("#modal_user_password").val("");
               $("#modal_user_confirm_password").val("");
           }, setTime);
       }
    });

    // Function to select a row
    $(TABLE_ROW).click(function () {
        $(TABLE_ROW).removeClass("row-active");
        $(this).addClass("row-active");
        $('[data-modal="edit"]').addClass("btn-active");
        $('[data-modal="debug"]').addClass("btn-active");
        rowSelected = true;
    });

    // Function to reset row status
    $(document).mouseup(function (e) {
        let element = $(".table-main-container");
        if (!element.is(e.target) && element.has(e.target).length === 0) {
            $('[data-modal="debug"]').removeClass("btn-active");
            $('[data-modal="edit"]').removeClass("btn-active");
            $(TABLE_ROW).removeClass("row-active");
            rowSelected = false;
        }
    });
});
