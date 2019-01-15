"use strict";
const TABLE_USERS = '#table_users';
const TABLE_DEVICES = '#table_device';
let renderTableDelay = 200;

// Callback function, called on success, for reading device data
function drawTableDevices (data) {
    for (let i = 0; i < data.devices.length; i++) {
        drawRowDevice(data.devices[i]);
    }
}

// The function of drawing the rows of the table of devices
function drawRowDevice (rowDataDevice) {
    let row = $('<tr class="table-row table-remove-row-device">');
    let onlineStatus = rowDataDevice.online;
    let deviceTypeNumber = rowDataDevice.device_type;
    let deviceType = {
        1: "Orange Pi Lite",
        2: "Orange Pi Zero",
        3: "Orange Pi One",
        4: "Orange Pi PC",
        5: "Orange Pi Plus",
        6: "Orange Pi 2G-IoT"
    };

    onlineStatus = onlineStatus === true ? "Online" : "Offline";

    $(TABLE_DEVICES).append(row);
    row.append($("<input data-device-id type=\"hidden\">").val(rowDataDevice.id));
    row.append($("<td data-device-type-id>" + rowDataDevice.device_id + "</td>"));
    row.append($("<td data-device-type>" + deviceType[deviceTypeNumber] + "</td>"));
    row.append($("<td data-device-last-address>" + rowDataDevice.last_address + "</td>"));
    row.append($("<td data-device-last-online>" + rowDataDevice.last_connected_at + "</td>"));

    if (onlineStatus === "Online") {
        row.append($("<td data-device-status class='online'>" + onlineStatus + "</td>"));
    } else {
        row.append($("<td data-device-status class='offline'>" + onlineStatus + "</td>"));
    }
}

// Callback function, called on success, for reading users data
function drawTableUsers (data) {
    for (let i = 0; i < data.users.length ; i++) {
        drawRowUsers(data.users[i]);
    }
}

// The function of drawing user table rows
function drawRowUsers(rowDataUsers) {
    let row = $('<tr class="table-row table-remove-row-user">');
    let userEnabled = rowDataUsers.active;

    userEnabled = userEnabled === true ? "Yes" : "No";

    $(TABLE_USERS).append(row);
    row.append($("<input data-user-id type=\"hidden\">").val(rowDataUsers.id));
    row.append($("<td data-user-name>" + rowDataUsers.first_name + " " + rowDataUsers.last_name + "</td>"));
    row.append($("<td data-user-email>" + rowDataUsers.email + "</td>"));
    row.append($("<td data-user-last-login>" + rowDataUsers.last_login_at + "</td>"));

    if (userEnabled === "Yes") {
        row.append($("<td data-user-enabled class='online'>" + userEnabled + "</td>"));
    } else {
        row.append($("<td data-user-enabled class='offline'>" + userEnabled + "</td>"));
    }
}

// Cleaning the device table
function removeTableDevices () {
    $(".table-remove-row-device").remove();
}

// Clearing the user table
function removeTableUsers () {
    $(".table-remove-row-user").remove();
}


function renderTableDevices () {
    removeTableDevices();
    sendJSONRequest("/home/getDevicesList", null, RequestMethod.GET, drawTableDevices, debug_callback, process_failures);
    setTimeout(function () {
        rowSelection();
    },renderTableDelay);
}

function renderTableUsers () {
    removeTableUsers();
    sendJSONRequest("/home/getUsersList", null, RequestMethod.GET, drawTableUsers, debug_callback, process_failures);
    setTimeout(function () {
        rowSelection();
    },renderTableDelay);
}

$(document).ready(function () {

    renderTableUsers();
    renderTableDevices();

    setInterval(function () {
        renderTableUsers();
        renderTableDevices();
    }, 60000);

});