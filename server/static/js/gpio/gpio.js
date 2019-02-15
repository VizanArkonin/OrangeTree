"use strict";
const MODE_SWITCH_BUTTON = "button[class *= 'mode-switch']";
const STATUS_SWITCH_BUTTON = "button[class *= 'status-switch']";
const LOCK_ICON = ".lock-icon";

const MODE_SWITCH_INPUT = "input[class = 'mode-switch-input']";
const STATUS_SWITCH_INPUT = "input[class = 'status-switch-input']";
const LOCK_INPUT = "input[class = 'lock-input']";

/**
 * Main processing workhorse, takes the JSON list with pin statuses (received by socket) and applies it's state to page elements.
 * @param pinsList: JSON - list of pin objects
 */
function processPins(pinsList) {
    for (let index = 0; index < pinsList.length; index++) {
        let pin = pinsList[index];
        let pin_container = "[data-pinid = " + pin.pin + "]";

        let mode_switch_input = $(pin_container).children(MODE_SWITCH_INPUT);
        let status_switch_input = $(pin_container).children(STATUS_SWITCH_INPUT);
        let lock_input = $(pin_container).children(LOCK_INPUT);

        // To prevent excessive change triggering, we validate if value has indeed changed.
        if (parseInt(mode_switch_input.val()) !== pin.mode) {
            mode_switch_input.val(pin.mode).trigger('change');
        }
        if (parseInt(status_switch_input.val()) !== pin.state) {
            status_switch_input.val(pin.state).trigger('change');
        }
        if ((lock_input.val() === "true") !== pin.locked || lock_input.val().length === 0) {
            lock_input.val(pin.locked).trigger('change');
        }
    }
}

$(document).ready(function() {
    // NOTE: Socket variable is created and imported in template file in order to pass parameters through template
    /**
     * We use trigger/observer pairs for mode, state and lock indicators.
     * Trigger initiates socket message with value change, another socket receives the new board state and changes the
     * observer-targeted inputs, which in turn triggers the elements processing.
     */
    // Mode trigger
    $(MODE_SWITCH_BUTTON).click(function() {
        let newMode;
        if ($(this).siblings(MODE_SWITCH_INPUT).val() === "0") {
            newMode = 1;
        } else {
            newMode = 0
        }

        gpioSocket.emit("setPinMode",
            {"pinID": $(this).parent().attr("data-pinId"),
             "modeID": newMode});
        if (newMode === 1) {
            gpioSocket.emit("setOutput",
                {"pinID": $(this).parent().attr("data-pinId"),
                 "value": 0});
        }
    });
    // Mode observer
    $(MODE_SWITCH_INPUT).on("change", function() {
        if ($(this).val() === "0") {
            $(this).siblings(MODE_SWITCH_BUTTON).removeClass("button-off").addClass("button-on").html("IN");
        } else {
            $(this).siblings(MODE_SWITCH_BUTTON).removeClass("button-on").addClass("button-off").html("OUT");
        }
    });

    // Status trigger
    $(STATUS_SWITCH_BUTTON).click(function() {
        if ($(this).siblings(MODE_SWITCH_INPUT).val() === "1") {
            let newValue;
            if ($(this).siblings(STATUS_SWITCH_INPUT).val() === "0") {
                newValue = 1
            } else {
                newValue = 0
            }

            gpioSocket.emit("setOutput",
                {"pinID": $(this).parent().attr("data-pinId"),
                 "value": newValue})
        }
    });
    // Status observer
    $(STATUS_SWITCH_INPUT).on("change", function() {
        if ($(this).val() === "0") {
            $(this).siblings(STATUS_SWITCH_BUTTON).removeClass("button-on").addClass("button-off").html("OFF");
        } else {
            $(this).siblings(STATUS_SWITCH_BUTTON).removeClass("button-off").addClass("button-on").html("ON");
        }
    });

    // Lock trigger
    $(LOCK_ICON).click(function() {
        let newMode;
        newMode = $(this).siblings(LOCK_INPUT).val() === "false";

        gpioSocket.emit("setPinLock",
            {"pinID": $(this).parent().attr("data-pinId"),
             "locked": newMode})
    });
    // Lock observer
    $(LOCK_INPUT).on("change", function() {
        if ($(this).val() === "false") {
            $(this).siblings(LOCK_ICON).removeClass("fa-lock").addClass("fa-lock-open");
        } else {
            $(this).siblings(LOCK_ICON).removeClass("fa-lock-open").addClass("fa-lock");
        }
    });
});