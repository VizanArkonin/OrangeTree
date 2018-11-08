/**
 * Serializes provided object to JSON, sends it by given URL (relative to current domain)
 * and processes the response (if callback function is provided)
 *
 * @param url       - URL, relative to current domain
 * @param payload   - Object to serialize and pass
 * @param method    - Request method. Can be "GET" or "POST"
 * @param callback  - Callback function
 */
function sendRequest(url, payload, method = "GET", callback = function(data) {}) {
    $.ajax({
        type: method,
        url: url,
        contentType: "application/json",
        data: JSON.stringify(payload),
        success: function(data) {
            callback(data)
        }
    })
}