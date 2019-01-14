sendJSONRequest("/home/getDevicesList", null, RequestMethod.GET, drawTableDevices, debug_callback, process_failures);

function drawTableDevices (data) {
    for (let i = 0; i < data.devices.length; i++){
        renderRowDevice(data.devices[i]);
    }
}

function renderRowDevice (rowDataDevice) {
    let row = $('<tr class="table-row">');

    $('#table_device').append(row);
    row.append($("<td data-device-type-id>" + rowDataDevice.device_id + "</td>"));
    row.append($("<td data-device-type>" + rowDataDevice.device_type + "</td>"));
    row.append($("<td data-device-last-address>" + rowDataDevice.last_address + "</td>"));
    row.append($("<td data-device-last-online>" + rowDataDevice.last_connected_at + "</td>"));
    row.append($("<td data-device-status>" + rowDataDevice.online + "</td>"));
}