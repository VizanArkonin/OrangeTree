"use strict";
const TABLE_ROW = ".table-row";

/**
 * Resets table row event listener, allowing it to be selected/deselected
 * @var $activeRow        - It contains selected row
 * @var rowSelected       - Active row indicator
 */
let rowSelected = false;
let $activeRow;

function resetRowSelection () {
    $(TABLE_ROW).click(function () {
        $activeRow = $(this);
        $(TABLE_ROW).removeClass("row-active");
        $activeRow.addClass("row-active");
        $('[data-modal="edit"]').activeButton();
        $('[data-modal="debug"]').activeButton();
        $('[data-modal="delete"]').activeButton();
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

    $(modal.device.field.hidden.id).val($deviseIdHidden);
    $(modal.device.field.id).val($deviceID);
    $(modal.device.field.hidden.stateId).val($deviceID);
    $(modal.device.field.type).val($deviseType);
}

/**
 * The function of forming a JSON object by reading the data of the modal window
 * @returns         - Device data payload object
 */
function getDevicePayload () {
    let payload = {"deviceData": {}};

    payload.deviceData.id = $(modal.device.field.hidden.id).val();
    payload.deviceData.device_id = $(modal.device.field.id).val();
    payload.deviceData.device_type = $(modal.device.field.type).val();
    payload.deviceData.device_access_key = $(modal.device.field.key).val();

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
    let $hiddenContainer = $activeRow.children('.user-roles-container').children('input');
    let userRolesList = [];

    $(modal.user.field.hidden.id).val($deviceIdHidden);
    $(modal.user.field.firstName).val($userFirstName);
    $(modal.user.field.lastName).val($userLastName);
    $(modal.user.field.email).val($userEmail);
    $(modal.user.field.hidden.email).val($userEmail);

    if ($userActive === 'true') {
        $(modal.user.checkbox.active).prop("checked", true);
    }

    $hiddenContainer.each(function () {
        userRolesList.push($(this).val());
        for (let userRoleIndex = 0; userRoleIndex < userRolesList.length; userRoleIndex++) {
            let userRole = userRolesList[userRoleIndex];
            $(modal.user.checkbox.roles).each(function () {
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

    payload.userData.id = $(modal.user.field.hidden.id).val();
    payload.userData.email = $(modal.user.field.email).val();
    payload.userData.first_name = $(modal.user.field.firstName).val();
    payload.userData.last_name = $(modal.user.field.lastName).val();
    payload.userData.password = $(modal.user.field.password).val();
    payload.userData.active = $(modal.user.checkbox.active).prop('checked') === true;

    $(modal.user.checkbox.roles).each(function () {
       if ($(this).prop('checked') === true) {
           payload.userData.roles.push({"role_name": $(this).val()});
       }
    });

    return payload;
}

$(document).ready(function () {

    const setTimeAnimation = 400;
    //Library of modal user window errors
    const errorMessageModalUser = {
        firstName: 'First name field cannot be empty',
        lastName: 'Last name field cannot be empty',
        password: 'Confirm the password',
        confirmPassword: 'Invalid password',
        passwordEmpty: 'Password field cannot be empty',
        emailCheck: 'This email address already exists',
        emailEmpty: 'Email address cannot be empty',
        emailCorrect: 'An invalid email address was entered'
    };
    let stateModalUser = {};
    //Library of modal device window errors
    const errorMessageModalDevices = {
        deviceIdEmpty: 'Device ID field cannot be empty',
        deviceIdCheck: 'This id already exists',
        deviceKey: 'Device Key field cannot be empty'
    };
    let stateModalDevice = {};
    let stateModalButtonDevice = {
        edit: false,
        add: false
    };
    let stateModalButtonUser = {
        edit: false,
        add: false
    };

    /**
     * Animation when opening a modal window
     */
    function openModalAnimation () {
        $(modal.window.open).removeClass(modal.animation.close);
        $(modal.window.open).addClass(modal.animation.open);
    }

    /**
     * Animation when closing a modal window
     */
    function closeModalAnimation () {
        $(modal.window.open).removeClass(modal.animation.open);
        $(modal.window.open).addClass(modal.animation.close);
    }

    /**
     * Function to reset row status
     */
    $(document).mouseup(function (e) {
        let element = $(".table-main-container");
        if (!element.is(e.target) && element.has(e.target).length === 0) {
            $('[data-modal="debug"]').disabledButton();
            $('[data-modal="edit"]').disabledButton();
            $('[data-modal="delete"]').disabledButton();
            $(TABLE_ROW).removeClass("row-active");
            rowSelected = false;
        }
    });

    /**
     * Check for duplicate device id
     * @param data - JSON object {"deviceExists": true/false}
     */
    function checkDeviceDataId (data) {
        stateModalDevice.deviceIdCheck = data.deviceExists !== true;
    }
    
    function  checkFieldDeviceId () {
        stateModalDevice.deviceIdEmpty = $(modal.device.field.id).val() !== "";

        if ($(modal.device.field.id).val() !== $(modal.device.field.hidden.stateId).val()) {
            let URL = "/home/validateDeviceExistence?device_id=" + $(modal.device.field.id).val();

            sendJSONRequest(URL, null, RequestMethod.GET, beforeSendEmpty,
                            checkDeviceDataId, debug_callback, process_failures);
        } else {
            stateModalDevice.deviceIdCheck = true;
        }
    }

    /**
     * This function ensures that the field is not empty
     */
    function checkFieldDeviceKey () {
        if (stateModalButtonDevice.add === true) {
            stateModalDevice.deviceKey = $(modal.device.field.key).val() !== "";
        }
    }

    /**
     * The function checks the conditions for a modal device window
     */
    function setDeviceState () {
        checkFieldDeviceId();
        checkFieldDeviceKey();
    }

    /**
     * For device
     * The function displays errors according to the status of the component.
     * Enables / disables the form submit button according to the state of the components.
     */
    function showErrorMessageDevice () {
        let arrayCheckState = [];
        let arrayErrorMessage = [];

        for (let index in stateModalDevice) {
            arrayCheckState.push(stateModalDevice[index]);
        }

        let checkState = arrayCheckState.every(function (state) {
            return state !== false;
        });

        if (checkState === false) {
            for (let index in stateModalDevice) {
                if (stateModalDevice[index] === false) {
                    arrayErrorMessage.push(errorMessageModalDevices[index]);
                    $(modal.device.message.error).text(arrayErrorMessage[0]).useClassErrorMessage();
                    $(modal.device.button.edit).disabledButton();
                    $(modal.device.button.add).disabledButton();
                }
            }
        } else {
            $(modal.device.message.error).text('Correct').useClassSuccessMessage();
            $(modal.device.button.all).activeButton();
        }
    }

    /**
     * This function ensures that the field is not empty
     */
    function checkFieldFirsName () {
        stateModalUser.firstName = $(modal.user.field.firstName).val() !== "";
    }

    /**
     * This function ensures that the field is not empty
     */
    function checkFieldLastName () {
        stateModalUser.lastName = $(modal.user.field.lastName).val() !== "";
    }

    /**
     * Check for duplicate email address
     * @param data - JSON object {"userExists": true/false}
     */
    function checkUserDataEmail (data) {
        stateModalUser.emailCheck = data.userExists !== true;
    }

    /**
     * The function of checking the correctness of the email address of the user
     */
    function checkFieldEmail () {
        let regExp = /^([A-Za-z0-9_\-.+])+@([A-Za-z0-9_\-.])+\.([A-Za-z]{2,})$/;

        // Check for empty input field
        stateModalUser.emailEmpty = $(modal.user.field.email).val() !== "";

        // Check email for validity
        stateModalUser.emailCorrect = regExp.test($(modal.user.field.email).val());

        // Execution of the request, if there are changes in the email input field
        if ($(modal.user.field.email).val() !== $(modal.user.field.hidden.email).val()) {
            let URL = "/home/validateUserExistence?user_email=" + $(modal.user.field.email).val();

            sendJSONRequest(URL, null, RequestMethod.GET, beforeSendEmpty,
                            checkUserDataEmail, debug_callback, process_failures);
        } else {
            stateModalUser.emailCheck = true;
        }
    }

    /**
     * The function checks whether the input field is correctly filled
     */
    function checkFieldPassword () {
        if (stateModalButtonUser.add === true) {
            stateModalUser.passwordEmpty = $(modal.user.field.password).val() !== "";
            stateModalUser.password = !($(modal.user.field.password).val() !== $(modal.user.field.confirmPassword).val() && $(modal.user.field.confirmPassword).val() === "");
            stateModalUser.confirmPassword = $(modal.user.field.confirmPassword).val() === $(modal.user.field.password).val();
        }
        if (stateModalButtonUser.edit === true) {
            stateModalUser.password = !($(modal.user.field.password).val() !== $(modal.user.field.confirmPassword).val());
        }
    }

    /**
     * The function checks the conditions for a modal user window
     */
    function setUserState () {
        checkFieldFirsName();
        checkFieldLastName();
        checkFieldEmail();
        checkFieldPassword();
    }

    /**
     * For user
     * The function displays errors according to the status of the component.
     * Enables / disables the form submit button according to the state of the components.
     */
    function showErrorMessageUser () {
        let arrayCheckState = [];
        let arrayErrorMessage = [];

        for (let index in stateModalUser) {
            arrayCheckState.push(stateModalUser[index]);
        }

        let checkState = arrayCheckState.every(function (state) {
            return state !== false;
        });

        if (checkState === false) {
            for (let index in stateModalUser) {
                if (stateModalUser[index] === false) {
                    arrayErrorMessage.push(errorMessageModalUser[index]);
                    $(modal.user.message.error).text(arrayErrorMessage[0]).useClassErrorMessage();
                    $(modal.user.button.edit).disabledButton();
                    $(modal.user.button.add).disabledButton();
                }
            }
        } else {
            $(modal.user.message.error).text('Correct').useClassSuccessMessage();
                $(modal.user.button.edit).activeButton();
                $(modal.user.button.add).activeButton();
        }
    }

    // Field check Device Id
    $(modal.device.field.id).focusout(function () {
        checkFieldDeviceId();
        setTimeout(function () {
            showErrorMessageDevice();
        }, 200);
    });

    // Field check Device Key
    $(modal.device.field.key).keyup(function () {
        checkFieldDeviceKey();
        showErrorMessageDevice();
    });

    // Field check Firs Name
    $(modal.user.field.firstName).keyup(function () {
        checkFieldFirsName();
        showErrorMessageUser();
    });

    // Field check Last Name
    $(modal.user.field.lastName).keyup(function () {
        checkFieldLastName();
        showErrorMessageUser();
    });

    // Field check User email
    $(modal.user.field.email).focusout(function () {
        checkFieldEmail();
        setTimeout(function () {
            showErrorMessageUser();
        }, 200);
    });

    // Field check User password
    $(modal.user.field.password).keyup(function () {
        checkFieldPassword();
        showErrorMessageUser();
    });

    // Field check Confirm password (for user)
    $(modal.user.field.confirmPassword).keyup(function () {
        checkFieldPassword();
        showErrorMessageUser();
    });

    /**
     * Opening modal windows to add a new / edit device
     */
    $(modal.device.button.open).click(function () {
        if ($(this).data("modal") === "add") {
            $(modal.device.header).text("Add new device");
            $(modal.device.field.id).attr("placeholder","Enter device ID");
            $(modal.device.field.key).attr("placeholder","Enter device key");
            $(modal.device.field.type).val("1");
            stateModalButtonDevice.add = true;
            openModalAnimation();
            $(modal.device.button.add).css(DISPLAY_BLOCK);
            $(modal.device.window).css(DISPLAY_FLEX);
            setDeviceState();
            showErrorMessageDevice();
        }
        if ($(this).data("modal") === "edit" && rowSelected) {
            setDeviceModalWindowValues();
            $(modal.device.header).text("Edit device");
            $(modal.device.field.id).attr("placeholder","Edit device ID");
            $(modal.device.field.key).attr("placeholder","Edit device key");
            openModalAnimation();
            stateModalButtonDevice.edit = true;
            $(modal.device.button.edit).css(DISPLAY_BLOCK);
            $(modal.device.window).css(DISPLAY_FLEX);
            stateModalDevice.deviceKey = true;
            setDeviceState();
            showErrorMessageDevice();
        }
    });

    /**
     * Opening modal windows to add a new / edit user
     */
    $(modal.user.button.open).click(function () {
        if ($(this).data("modal") === "add") {
            $(modal.user.header).text("Add new user");
            $(modal.user.field.firstName).attr("placeholder","Enter First Name");
            $(modal.user.field.lastName).attr("placeholder","Enter Last Name");
            $(modal.user.field.email).attr("placeholder","Enter email");
            $(modal.user.field.password).attr("placeholder","Enter password");
            $(modal.user.field.confirmPassword).attr("placeholder","Confirm password");
            openModalAnimation();
            stateModalButtonUser.add = true;
            $(modal.user.button.add).css(DISPLAY_BLOCK);
            $(modal.user.window).css(DISPLAY_FLEX);
            setUserState();
            showErrorMessageUser();
        }
        if ($(this).data("modal") === "edit" && rowSelected) {
            setUserModalWindowValues();
            $(modal.user.header).text("Edit user");
            $(modal.user.field.firstName).attr("placeholder","Edit First Name");
            $(modal.user.field.lastName).attr("placeholder","Edit Last Name");
            $(modal.user.field.email).attr("placeholder","Edit email");
            $(modal.user.field.password).attr("placeholder","Edit password");
            $(modal.user.field.confirmPassword).attr("placeholder","Confirm password");
            openModalAnimation();
            stateModalButtonUser.edit = true;
            $(modal.user.button.edit).css(DISPLAY_BLOCK);
            $(modal.user.window).css(DISPLAY_FLEX);
            setUserState();
            showErrorMessageUser();
        }
    });

    /**
     * Close device modal windows. With zeroing output
     */
    function closeDeviceModalWindow () {
        closeModalAnimation();
        stateModalButtonDevice.add = false;
        stateModalButtonDevice.edit = false;
        setTimeout(function () {
           $(modal.device.window).css(DISPLAY_NONE);
           $(modal.deleteDevice.window).css(DISPLAY_NONE);
           $(modal.device.field.hidden.id).val("");
           $(modal.device.field.id).val("");
           $(modal.device.field.key).val("");
           $(modal.device.field.type).val("1");
           $(modal.user.button.all).css(DISPLAY_NONE);
           $(modal.device.button.all).css(DISPLAY_NONE);
        }, setTimeAnimation);
    }

    /**
     * Close user modal windows. With zeroing output
     */
    function closeUserModalWindow () {
        closeModalAnimation();
        stateModalButtonUser.add = false;
        stateModalButtonUser.edit = false;
        setTimeout(function () {
           $(modal.user.window).css(DISPLAY_NONE);
           $(modal.deleteUser.window).css(DISPLAY_NONE);
           $(modal.user.field.hidden.id).val("");
           $(modal.user.field.firstName).val("");
           $(modal.user.field.lastName).val("");
           $(modal.user.field.email).val("");
           $(modal.user.field.hidden.email).val("");
           $(modal.user.field.password).val("");
           $(modal.user.field.confirmPassword).val("");
           $(modal.user.checkbox.active).prop("checked", false);
           $(modal.user.checkbox.roles).each(function () {
               $(this).prop('checked', false);
           });
           $(modal.user.button.all).css(DISPLAY_NONE);
           $(modal.device.button.all).css(DISPLAY_NONE);
        }, setTimeAnimation);
    }

    // Close all modal windows
    $(modal.window.close).click(function () {
        if ($(this).data("modal") === "device") {
            closeDeviceModalWindow();
        } else {
            closeUserModalWindow();
        }
    });

    // Device editing function followed by an AJAX request
    $(modal.device.button.edit).click(function () {
        closeDeviceModalWindow();
        sendJSONRequest("/home/device.svc", getDevicePayload(), RequestMethod.PUT, showLoaderInDevicesTable,
                        renderDevicesTable, debug_callback, process_failures);
    });

    // Creating an AJAX request to add a new device
    $(modal.device.button.add).click(function () {
        closeDeviceModalWindow();
        sendJSONRequest("/home/device.svc", getDevicePayload(), RequestMethod.POST, showLoaderInDevicesTable,
                        renderDevicesTable, debug_callback, process_failures);
    });

    // User editing function followed by an AJAX request
    $(modal.user.button.edit).click(function () {
        closeUserModalWindow();
        sendJSONRequest("/home/user.svc", getUserPayload(), RequestMethod.PUT, showLoaderInUsersTable,
                        renderUsersTable, debug_callback, process_failures);
    });

    // Creating an AJAX request to add a new user
    $(modal.user.button.add).click(function () {
        closeUserModalWindow();
        sendJSONRequest("/home/user.svc", getUserPayload(), RequestMethod.POST, showLoaderInUsersTable,
                        renderUsersTable, debug_callback, process_failures);
    });

    //Opening a modal window to remove a device
    $(modal.deleteDevice.button.open).click(function () {
        setDeviceModalWindowValues();
        openModalAnimation();
        $(modal.deleteDevice.message.name).text($(modal.device.field.id).val());
        $(modal.deleteDevice.button.del).css(DISPLAY_BLOCK);
        $(modal.deleteDevice.window).css(DISPLAY_FLEX);
    });

    // Create an AJAX request to remove a user
    $(modal.deleteDevice.button.del).click(function () {
        closeDeviceModalWindow();
        sendJSONRequest("/home/device.svc", getDevicePayload(), RequestMethod.DELETE, showLoaderInDevicesTable,
                        renderDevicesTable, debug_callback, process_failures);
    });

    // Opening a modal window to remove a user
    $(modal.deleteUser.button.open).click(function () {
        setUserModalWindowValues();
        openModalAnimation();
        $(modal.deleteUser.message.name).text($(modal.user.field.firstName).val() + " " + $(modal.user.field.lastName).val());
        $(modal.deleteUser.button.del).css(DISPLAY_BLOCK);
        $(modal.deleteUser.window).css(DISPLAY_FLEX);
    });

    // Create an AJAX request to remove a user
    $(modal.deleteUser.button.del).click(function () {
        closeUserModalWindow();
        sendJSONRequest("/home/user.svc", getUserPayload(), RequestMethod.DELETE, showLoaderInUsersTable,
                        renderUsersTable, debug_callback, process_failures);
    });

    //Refresh table devises
    $(table.device.button.refresh).click(function () {
        renderDevicesTable();
    });

    //Refresh table users
    $(table.user.button.refresh).click(function () {
       renderUsersTable();
    });
});