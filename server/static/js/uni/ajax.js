/**
 * Enum-like request method provider
 * @type {{GET: string, POST: string, PUT: string, DELETE: string}}
 */
const RequestMethod = {
    GET: "GET",
    POST: "POST",
    PUT: "PUT",
    DELETE: "DELETE"
};

/**
 * Serializes provided object to JSON, sends it by given URL (relative to current domain)
 * and processes the response (if callback function is provided)
 *
 * @param url                   - URL, relative to current domain
 * @param payload               - Object to serialize and pass
 * @param method                - Request method. Can be "GET" or "POST"
 * @param callback              - Callback function
 * @param failure_processor     - Function that will process the errors, should they occur
 * @param beforeSend            - Calls given function before executing the AJAX request
 */
function sendJSONRequest(url, payload, method = RequestMethod.GET, beforeSend = function() {},
                        callback = function(data) {}, failure_processor = function(jqXHR, statusText, errorThrown) {}) {
    $.ajax({
        type: method,
        url: url,
        contentType: "application/json",
        data: JSON.stringify(payload),
        beforeSend: function () {
            beforeSend();
        },
        success: function(data) {
            callback(data);
        },
        fail: function(jqXHR, statusText, error) {
            failure_processor(jqXHR, statusText, error);
        }
    });
}

/**
 * Debug callback for sendJSONRequest function. Prints response and analyzes it for having
 * @param data  -   JSON object
 */
function debug_callback(data) {
    console.log(data);
    let errors_array = data.errors;
    if (errors_array.length === 0) {
        console.log("No Errors")
    } else {
        for (let index = 0; index < errors_array.length; index++) {
            console.log(errors_array[index]);
        }
    }
}

/**
 * Standard debug error processor, used in sendJSONRequest function.
 * @param jxXHR         - jxXHR context
 * @param statusText    - Status string
 * @param errorThrown   - Error
 */
function process_failures(jxXHR, statusText, errorThrown) {
    console.log(statusText);
    console.log(errorThrown);
    console.log(jxXHR.responseJSON);
}

/**
 * An empty function that serves as a stub.
 * In the case when we do not need to perform any function at the time of the request.
 */
function beforeSendEmpty () {
    
}