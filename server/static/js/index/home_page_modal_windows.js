"use strict";
// Variables with classes for buttons
const OPEN_MODAL_USER = ".open-modal-user";
const OPEN_MODAL_DEVICE = ".open-modal-device";
const CLOSE_MODAL = ".close-modal";
const TABLE_ROW = ".table-row";
const BTN_MODAL_DEVICE_EDIT = '#btn_modal_devise_edit';
const BTN_MODAL_DEVICE_ADD = '#btn_modal_device_add';
//Other variables
const MODAL_ANIMATION_OPEN = "modal-animation-open";
const MODAL_ANIMATION_CLOSE = "modal-animation-close";
const MODAL = ".modal";
const MODAL_DEVICE = "#modal_device";
const MODAL_USER = "#modal_user";

const MODAL_DEVICE_ID_HIDDEN = "#modal_device_id_hidden";
const MODAL_DEVICE_ID = "#modal_device_id";
const MODAL_DEVICE_TYPE = "#modal_device_type";
const MODAL_DEVICE_KEY = "#modal_device_key";

const DISPLAY_BLOCK = {"display":"block"};
// A helper variable to track the status of a row
let rowSelected = false;
let $activeRow;

// Function to select a row
function rowSelection () {
    $(TABLE_ROW).click(function () {
        $activeRow = $(this);
        $(TABLE_ROW).removeClass("row-active");
        $activeRow.addClass("row-active");
        $('[data-modal="edit"]').addClass("btn-active");
        $('[data-modal="debug"]').addClass("btn-active");
        rowSelected = true;
    });
}

// The function sets the values of the modal window fields in accordance with the selected line (for devices)
function settingModalValuesDevice () {
    let row = $activeRow;
    let $deviseType = row.children('[data-device-type]').attr("data-device-type");
    $(MODAL_DEVICE_ID_HIDDEN).val(row.children('[data-device-id]').val());
    $(MODAL_DEVICE_ID).val((row.children('[data-device-type-id]').text()));
    $(MODAL_DEVICE_TYPE).val($deviseType);
}

// The function of forming a JSON object by reading the data of the modal window
function updateDevice (payload) {
    payload.deviceData.id = $(MODAL_DEVICE_ID_HIDDEN).val();
    payload.deviceData.device_id = $(MODAL_DEVICE_ID).val();
    payload.deviceData.device_type = $(MODAL_DEVICE_TYPE).val();
    payload.deviceData.device_access_key = $(MODAL_DEVICE_KEY).val();

    return payload;
}

$(document).ready(function () {
    let setTime = 500; // Set the delay time for the animation to work

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
            $(MODAL_DEVICE_ID).attr("placeholder","Enter device ID");
            $(MODAL_DEVICE_KEY).attr("placeholder","Enter device key");
            $(MODAL_DEVICE_TYPE).val("1");
            openModalAnimation();
            $(BTN_MODAL_DEVICE_ADD).css(DISPLAY_BLOCK);
            $(MODAL_DEVICE).css(DISPLAY_FLEX);
        }
        if ($(this).data("modal") === "edit" && rowSelected) {
            settingModalValuesDevice();
            $("#modal_header_device").text("Edit device");
            $(MODAL_DEVICE_ID).attr("placeholder","Edit device ID");
            $(MODAL_DEVICE_KEY).attr("placeholder","Edit device key");
            openModalAnimation();
            $(BTN_MODAL_DEVICE_EDIT).css(DISPLAY_BLOCK);
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
            $('#btn_modal_user_add').css(DISPLAY_BLOCK);
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
            $('#btn_modal_user_edit').css(DISPLAY_BLOCK);
            $(MODAL_USER).css(DISPLAY_FLEX);
        }
    });

    // Close device modal windows. With zeroing output
    function closeModalDevice () {
        closeModalAnimation();
        setTimeout(function () {
           $(MODAL_DEVICE).css(DISPLAY_NONE);
           $(MODAL_DEVICE_ID).val("");
           $(MODAL_DEVICE_KEY).val("");
           $(MODAL_DEVICE_TYPE).val("1");
           $('[id *= btn_modal]').css(DISPLAY_NONE);
        }, setTime);
    }

    // Close user modal windows. With zeroing output
    function closeModalUser () {
        closeModalAnimation();
        setTimeout(function () {
           $(MODAL_USER).css(DISPLAY_NONE);
           $("#modal_user_first_name").val("");
           $("#modal_user_last_name").val("");
           $("#modal_user_email").val("");
           $("#modal_user_password").val("");
           $("#modal_user_confirm_password").val("");
           $('[id *= btn_modal]').css(DISPLAY_NONE);
        }, setTime);
    }

    $(CLOSE_MODAL).click(function () {
        if ($(this).data("modal") === "device") {
            closeModalDevice();
        } else {
            closeModalUser();
        }
    });

    // Device editing function followed by an AJAX request
    $(BTN_MODAL_DEVICE_EDIT).click(function () {
        let payload = {"deviceData": {}};
        closeModalDevice();
        sendJSONRequest("/home/device.svc", updateDevice(payload), RequestMethod.PUT, beforeLoadTableDevice,
                        renderTableDevices, debug_callback, process_failures);
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