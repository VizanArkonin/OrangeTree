"use strict";
// Variables with classes for buttons
const OPEN_MODAL_USER = ".open-modal-user";
const OPEN_MODAL_DEVICE = ".open-modal-device";
const CLOSE_MODAL = ".close-modal";
const TABLE_ROW = ".table-row";
const BTN_MODAL_DEVICE_EDIT = '#btn_modal_devise_edit';
const BTN_MODAL_DEVICE_ADD = '#btn_modal_device_add';
const BTN_MODAL_USER_ADD = '#btn_modal_user_add';
const BTN_MODAL_USER_EDIT = '#btn_modal_user_edit';
//Other variables
const MODAL = ".modal";
const MODAL_ANIMATION_OPEN = "modal-animation-open";
const MODAL_ANIMATION_CLOSE = "modal-animation-close";

const MODAL_DEVICE = "#modal_device";
const MODAL_DEVICE_ID_HIDDEN = "#modal_device_id_hidden";
const MODAL_DEVICE_ID = "#modal_device_id";
const MODAL_DEVICE_TYPE = "#modal_device_type";
const MODAL_DEVICE_KEY = "#modal_device_key";

const MODAL_USER = "#modal_user";
const MODAL_USER_ID_HIDDEN = "#modal_device_id_hidden";
const MODAL_USER_FIRST_NAME = "#modal_user_first_name";
const MODAL_USER_LAST_NAME = "#modal_user_last_name";
const MODAL_USER_EMAIL = "#modal_user_email";
const MODAL_USER_PASSWORD = "#modal_user_password";
const MODAL_USER_CONFIRM_PASSWORD = "#modal_user_confirm_password";
const MODAL_USER_CHECKBOX = '.modal-user-checkbox';

const DISPLAY_BLOCK = {"display":"block"};

let rowSelected = false;
let $activeRow;


/**
 * Resets table row event listener, allowing it to be selected/deselected
 * @var $activeRow        - It contains selected row
 * @var rowSelected       - Active row indicator
 */
function resetRowSelection () {
    $(TABLE_ROW).click(function () {
        $activeRow = $(this);
        $(TABLE_ROW).removeClass("row-active");
        $activeRow.addClass("row-active");
        $('[data-modal="edit"]').addClass("btn-active");
        $('[data-modal="debug"]').addClass("btn-active");
        $('[data-modal="delete"]').addClass("btn-active");
        rowSelected = true;
    });
}

/**
 * The function sets the values of the modal window fields in accordance with the selected line (for devices)
 */
function setDeviceModalWindowValues () {
    let $deviseType = $activeRow.children('[data-device-type]').attr('data-device-type');
    let $deviceID = $activeRow.children('[data-device-type-id]').text();
    let $deviseIdHidden = $activeRow.children('[data-device-id]').val();

    $(MODAL_DEVICE_ID_HIDDEN).val($deviseIdHidden);
    $(MODAL_DEVICE_ID).val($deviceID);
    $(MODAL_DEVICE_TYPE).val($deviseType);
}

/**
 * The function of forming a JSON object by reading the data of the modal window
 * @returns         - Device data payload object
 */
function getDevicePayload () {
    let payload = {"deviceData": {}};

    payload.deviceData.id = $(MODAL_DEVICE_ID_HIDDEN).val();
    payload.deviceData.device_id = $(MODAL_DEVICE_ID).val();
    payload.deviceData.device_type = $(MODAL_DEVICE_TYPE).val();
    payload.deviceData.device_access_key = $(MODAL_DEVICE_KEY).val();

    return payload;
}

/**
 * The function sets the values of the modal window fields in accordance with the selected line (for users)
 */
function setUserModalWindowValues () {
    let $deviceIdHidden = $activeRow.children('[data-user-id]').val();
    let $userFirstName = $activeRow.children('[data-user-name]').attr('data-first-name');
    let $userLastName = $activeRow.children('[data-user-name]').attr('data-last-name');
    let $userEmail = $activeRow.children('[data-user-email]').text();
    let $userActive = $activeRow.children('[data-user-enabled]').attr('data-user-enabled');
    let $hiddenContainer = $activeRow.children('td:last-child').children('.user-roles-container').children('input');
    let userRolesList = [];

    $(MODAL_USER_ID_HIDDEN).val($deviceIdHidden);
    $(MODAL_USER_FIRST_NAME).val($userFirstName);
    $(MODAL_USER_LAST_NAME).val($userLastName);
    $(MODAL_USER_EMAIL).val($userEmail);

    if ($userActive === 'true') {
        $('#modal_user_active').prop("checked", true);
    }

    $hiddenContainer.each(function () {
        userRolesList.push($(this).val());
        for (let userRoleIndex = 0; userRoleIndex < userRolesList.length; userRoleIndex++) {
            let userRole = userRolesList[userRoleIndex];
            $(MODAL_USER_CHECKBOX).each(function () {
                if ($(this).val() === userRole) {
                    $(this).prop("checked", true);
                }
            });
        }
    });
}

/**
 * The function of forming a JSON object by reading the data of the modal window
 * @return          - User data payload object
 */
function getUserPayload () {
    let payload = {"userData": {"roles":[]}};

    payload.userData.id = $(MODAL_USER_ID_HIDDEN).val();
    payload.userData.email = $(MODAL_USER_EMAIL).val();
    payload.userData.first_name = $(MODAL_USER_FIRST_NAME).val();
    payload.userData.last_name = $(MODAL_USER_LAST_NAME).val();
    payload.userData.password = $(MODAL_USER_PASSWORD).val();
    payload.userData.active = $('#modal_user_active').prop('checked') === true;

    $(MODAL_USER_CHECKBOX).each(function () {
       if ($(this).prop('checked') === true) {
           payload.userData.roles.push({"role_name": $(this).val()});
       }
    });

    return payload;
}

$(document).ready(function () {
    // Set the delay time for the animation to work
    const setTimeAnimation = 400;

    /**
     * Animation when opening a modal window
     */
    function openModalAnimation () {
        $(MODAL).removeClass(MODAL_ANIMATION_CLOSE);
        $(MODAL).addClass(MODAL_ANIMATION_OPEN);
    }

    /**
     * Animation when closing a modal window
     */
    function closeModalAnimation () {
        $(MODAL).removeClass(MODAL_ANIMATION_OPEN);
        $(MODAL).addClass(MODAL_ANIMATION_CLOSE);
    }

    /**
     * Opening modal windows to add a new / edit device
     */
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
            setDeviceModalWindowValues();
            $("#modal_header_device").text("Edit device");
            $(MODAL_DEVICE_ID).attr("placeholder","Edit device ID");
            $(MODAL_DEVICE_KEY).attr("placeholder","Edit device key");
            openModalAnimation();
            $(BTN_MODAL_DEVICE_EDIT).css(DISPLAY_BLOCK);
            $(MODAL_DEVICE).css(DISPLAY_FLEX);
        }
    });

    /**
     * Opening modal windows to add a new / edit user
     */
    $(OPEN_MODAL_USER).click(function () {
        if ($(this).data("modal") === "add") {
            $("#modal_header_user").text("Add new user");
            $(MODAL_USER_FIRST_NAME).attr("placeholder","Enter First Name");
            $(MODAL_USER_LAST_NAME).attr("placeholder","Enter Last Name");
            $(MODAL_USER_EMAIL).attr("placeholder","Enter email");
            $(MODAL_USER_PASSWORD).attr("placeholder","Enter password");
            $(MODAL_USER_CONFIRM_PASSWORD).attr("placeholder","Confirm password");
            openModalAnimation();
            $('#btn_modal_user_add').css(DISPLAY_BLOCK);
            $(MODAL_USER).css(DISPLAY_FLEX);
        }
        if ($(this).data("modal") === "edit" && rowSelected) {
            setUserModalWindowValues();
            $("#modal_header_user").text("Edit user");
            $(MODAL_USER_FIRST_NAME).attr("placeholder","Edit First Name");
            $(MODAL_USER_LAST_NAME).attr("placeholder","Edit Last Name");
            $(MODAL_USER_EMAIL).attr("placeholder","Edit email");
            $(MODAL_USER_PASSWORD).attr("placeholder","Edit password");
            $(MODAL_USER_CONFIRM_PASSWORD).attr("placeholder","Confirm password");
            openModalAnimation();
            $('#btn_modal_user_edit').css(DISPLAY_BLOCK);
            $(MODAL_USER).css(DISPLAY_FLEX);
        }
    });

    /**
     * Close device modal windows. With zeroing output
     */
    function closeDeviceModalWindow () {
        closeModalAnimation();
        setTimeout(function () {
           $(MODAL_DEVICE).css(DISPLAY_NONE);
           $(MODAL_DEVICE_ID_HIDDEN).val("");
           $(MODAL_DEVICE_ID).val("");
           $(MODAL_DEVICE_KEY).val("");
           $(MODAL_DEVICE_TYPE).val("1");
           $('[id *= btn_modal]').css(DISPLAY_NONE);
        }, setTimeAnimation);
    }

    /**
     * Close user modal windows. With zeroing output
     */
    function closeUserModalWindow () {
        closeModalAnimation();
        setTimeout(function () {
           $(MODAL_USER).css(DISPLAY_NONE);
           $(MODAL_USER_ID_HIDDEN).val("");
           $(MODAL_USER_FIRST_NAME).val("");
           $(MODAL_USER_LAST_NAME).val("");
           $(MODAL_USER_EMAIL).val("");
           $(MODAL_USER_PASSWORD).val("");
           $(MODAL_USER_CONFIRM_PASSWORD).val("");
           $('#modal_user_active').prop("checked", false);
           $(MODAL_USER_CHECKBOX).each(function () {
               $(this).prop('checked', false);
           });
           $('[id *= btn_modal]').css(DISPLAY_NONE);
        }, setTimeAnimation);
    }

    // Close all modal windows
    $(CLOSE_MODAL).click(function () {
        if ($(this).data("modal") === "device") {
            closeDeviceModalWindow();
        } else {
            closeUserModalWindow();
        }
    });

    // Device editing function followed by an AJAX request
    $(BTN_MODAL_DEVICE_EDIT).click(function () {
        closeDeviceModalWindow();
        sendJSONRequest("/home/device.svc", getDevicePayload(), RequestMethod.PUT, showLoaderInDevicesTable,
                        renderDevicesTable, debug_callback, process_failures);
    });

    // Creating an AJAX request to add a new device
    $(BTN_MODAL_DEVICE_ADD).click(function () {
        closeDeviceModalWindow();
        sendJSONRequest("/home/device.svc", getDevicePayload(), RequestMethod.POST, showLoaderInDevicesTable,
                        renderDevicesTable, debug_callback, process_failures);
    });

    //Create an AJAX request to remove a device
    $('#btn_device_row_delete').click(function () {
        setDeviceModalWindowValues();
        sendJSONRequest("/home/device.svc", getDevicePayload(), RequestMethod.DELETE, showLoaderInDevicesTable,
                        renderDevicesTable, debug_callback, process_failures);
    });

    // User editing function followed by an AJAX request
    $(BTN_MODAL_USER_EDIT).click(function () {
        closeUserModalWindow();
        sendJSONRequest("/home/user.svc", getUserPayload(), RequestMethod.PUT, showLoaderInUsersTable,
                        renderUsersTable, debug_callback, process_failures);
    });

    // Creating an AJAX request to add a new user
    $(BTN_MODAL_USER_ADD).click(function () {
        closeUserModalWindow();
        sendJSONRequest("/home/user.svc", getUserPayload(), RequestMethod.POST, showLoaderInUsersTable,
                        renderUsersTable, debug_callback, process_failures);
    });

    // Create an AJAX request to remove a user
    $('#btn_user_row_delete').click(function () {
       setUserModalWindowValues();
       sendJSONRequest("/home/user.svc", getUserPayload(), RequestMethod.DELETE, showLoaderInUsersTable,
                        renderUsersTable, debug_callback, process_failures);
    });

    //Refresh table devises
    $('#btn_devises_table_refresh').click(function () {
        renderDevicesTable();
    });

    //Refresh table users
    $('#btn_users_table_refresh').click(function () {
       renderUsersTable();
    });

    /**
     * Function to reset row status
     */
    $(document).mouseup(function (e) {
        let element = $(".table-main-container");
        if (!element.is(e.target) && element.has(e.target).length === 0) {
            $('[data-modal="debug"]').removeClass("btn-active");
            $('[data-modal="edit"]').removeClass("btn-active");
            $('[data-modal="delete"]').removeClass("btn-active");
            $(TABLE_ROW).removeClass("row-active");
            rowSelected = false;
        }
    });
});