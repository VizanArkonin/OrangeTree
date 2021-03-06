"use strict";
const renderTableDelay = 300;
/**
 * Callback function, called on success, for reading device data
 * @param data       - JSON object
 */
function drawDevicesTable (data) {
    for (let index = 0; index < data.devices.length; index++) {
        drawDeviceRow(data.devices[index]);
    }
}

/**
 * The function of drawing the rows of the table of devices
 * @param rowData       - JSON object (format - data.devices[index])
 */
function drawDeviceRow (rowData) {
    let $row = $('<tr class="table-row-device table-remove-row-device">');
    let onlineStatus = rowData.online;
    let deviceTypeNumber = rowData.device_type;
    let lastAddress = rowData.last_address;
    let lastOnline = rowData.last_connected_at;
    const deviceType = {
        1: "Orange Pi Lite",
        2: "Orange Pi Zero",
        3: "Orange Pi One",
        4: "Orange Pi PC",
        5: "Orange Pi Plus",
        6: "Orange Pi 2G-IoT"
    };

    onlineStatus = onlineStatus === true ? "Online" : "Offline";

    $(table.device.content).append($row);

    $row.append($("<input data-device-id type=\"hidden\">").val(rowData.id));
    $row.append($("<td data-device-type-id>" + rowData.device_id + "</td>"));
    $row.append($("<td data-device-type>" + deviceType[deviceTypeNumber] + "</td>"));
    $row.children('[data-device-type]').attr('data-device-type', rowData.device_type);

    if ( lastAddress === null) {
        $row.append($("<td data-device-last-address>" + "N/A" + "</td>"));
    } else {
        $row.append($("<td data-device-last-address>" + lastAddress + "</td>"));
    }

    if (lastOnline === null) {
        $row.append($("<td data-device-last-online>" + "N/A" + "</td>"));
    } else {
        $row.append($("<td data-device-last-online>" + lastOnline + "</td>"));
    }

    if (onlineStatus === "Online") {
        $row.append($("<td data-device-status class='online'>" + onlineStatus + "</td>"));
    } else {
        $row.append($("<td data-device-status class='offline'>" + onlineStatus + "</td>"));
    }
}

/**
 * Callback function, called on success, for reading users data
 * @param data      - JSON object
 */
function drawUsersTable (data) {
    for (let index = 0; index < data.users.length ; index++) {
        drawUserRow(data.users[index]);
    }
}

/**
 * The function of drawing user table rows
 * @param rowData      - JSON object (format - data.users[index])
 */
function drawUserRow(rowData) {
    let $row = $('<tr class="table-row-user table-remove-row-user">');
    let userEnabled = rowData.active;
    let lastLogin = rowData.last_login_at;

    userEnabled = userEnabled === true ? "Yes" : "No";

    $(table.user.content).append($row);
    $row.append($("<input data-user-id type='hidden'>").val(rowData.id));
    $row.append($("<td data-user-name data-first-name data-last-name>" +
                "" + rowData.first_name + " " + rowData.last_name + "</td>"));
    $row.children('[data-user-name]').attr('data-first-name', rowData.first_name);
    $row.children('[data-user-name]').attr('data-last-name', rowData.last_name);
    $row.append($("<td data-user-email>" + rowData.email + "</td>"));

    if (lastLogin === null) {
        $row.append($("<td data-user-last-login>" + "N/A" + "</td>"));
    } else {
        $row.append($("<td data-user-last-login>" + lastLogin + "</td>"));
    }

    if (userEnabled === "Yes") {
        $row.append($("<td data-user-enabled class='online'>" + userEnabled + "</td>"));
    } else {
        $row.append($("<td data-user-enabled class='offline'>" + userEnabled + "</td>"));
    }

    $row.children('[data-user-enabled]').attr('data-user-enabled', rowData.active);

    $row.append($("<div class='user-roles-container'></div>"));

    for (let index = 0; index < rowData.roles.length; index++) {
        $row.children('.user-roles-container').append($("<input data-user-role type='hidden'>").val(rowData.roles[index].name));
    }
}

/**
 * Cleaning the device table
 */
function removeDeviceTableRows () {
    $(".table-remove-row-device").remove();
}

/**
 * Clearing the user table
 */
function removeUserTableRows () {
    $(".table-remove-row-user").remove();
}


function renderDevicesTable () {
    removeDeviceTableRows();
    sendJSONRequest("/home/getDevicesList", null, RequestMethod.GET, showLoaderInDevicesTable,
                    drawDevicesTable, debug_callback, process_failures);
    setTimeout(function () {
        resetRowDeviseSelection();
    }, renderTableDelay);
    resetStateTableDeviceButton();
    hideLoaderInDevicesTable();
}

function renderUsersTable () {
    removeUserTableRows();
    sendJSONRequest("/home/getUsersList", null, RequestMethod.GET, showLoaderInUsersTable,
                    drawUsersTable, debug_callback, process_failures);
    setTimeout(function () {
        resetRowUserSelection();
    }, renderTableDelay);
    resetStateTableUserButton();
    hideLoaderInUsersTable();
}

$(document).ready(function () {
    /**
     * The first function call when the page loads. To update the table (users, devices)
     */
    renderUsersTable();
    renderDevicesTable();

    setInterval(function () {
        renderUsersTable();
        renderDevicesTable();
    }, 300000);
});