'use strict';

/**
 * Reset line activity status (device table)
 * Deactivating device table buttons
 */
function resetStateTableDeviceButton () {
    $(TABLE_ROW_DEVICE).removeClass('row-active');
    $('[data-modal-device = "edit"]').disabledButton();
    $('[data-modal-device = "debug"]').disabledButton();
    $('[data-modal-device = "delete"]').disabledButton();

    tableRowsHomePage.state.device = false;
}

/**
 * Set the status of the line activity
 * Activate device table buttons
 */
function setStateTableDeviceButton () {
    $('[data-modal-device = "edit"]').activeButton();
    $('[data-modal-device = "debug"]').activeButton();
    $('[data-modal-device = "delete"]').activeButton();

    tableRowsHomePage.state.device = true;
}

/**
 * Perform actions to click on the row of the device table
 */
function resetRowDeviseSelection () {
    $(TABLE_ROW_DEVICE).click(function () {
        tableRowsHomePage.active.device = $(this);

        resetStateTableDeviceButton();
        $(this).addClass('row-active');
        setStateTableDeviceButton();
    });
}

/**
 * Reset line activity status (user table)
 * Deactivating user table buttons
 */
function resetStateTableUserButton () {
    $(TABLE_ROW_USER).removeClass('row-active');
    $('[data-modal-user = "edit"]').disabledButton();
    $('[data-modal-user = "debug"]').disabledButton();
    $('[data-modal-user = "delete"]').disabledButton();

    tableRowsHomePage.state.user = false;
}

/**
 * Set the status of the line activity
 * Activate device table buttons
 */
function setStateTableUserButton () {
    $('[data-modal-user = "edit"]').activeButton();
    $('[data-modal-user = "debug"]').activeButton();
    $('[data-modal-user = "delete"]').activeButton();

    tableRowsHomePage.state.user = true;
}

/**
 * Perform actions to click on the row of the device table
 */
function resetRowUserSelection () {
    $(TABLE_ROW_USER).click(function () {
        tableRowsHomePage.active.user = $(this);

        resetStateTableUserButton();
        $(this).addClass('row-active');
        setStateTableUserButton();
    });
}

$(document).ready(function () {
    /**
     * Function to reset row status for device/user table
     */
    $(document).mouseup(function (event) {
        let element = $(".table-main-container");
        if (!element.is(event.target) && element.has(event.target).length === 0) {
            resetStateTableDeviceButton();
            resetStateTableUserButton();
        }
    });
});