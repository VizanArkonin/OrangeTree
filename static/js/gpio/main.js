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
            $(this).siblings(MODE_SWITCH_BUTTON).removeClass("btn-off").addClass("btn-on").html("IN");
        } else {
            $(this).siblings(MODE_SWITCH_BUTTON).removeClass("btn-on").addClass("btn-off").html("OUT");
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
            $(this).siblings(STATUS_SWITCH_BUTTON).removeClass("btn-on").addClass("btn-off").html("OFF");
        } else {
            $(this).siblings(STATUS_SWITCH_BUTTON).removeClass("btn-off").addClass("btn-on").html("ON");
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

    ReactDOM.render(<GPIOTable pins={pins.pins} />, document.getElementById("root"))
});

class GPIOTable extends React.Component {
    constructor(props) {
        super(props);
        this.pins_list = [];
        for(let pin of props.pins) {
            if (pin.type === "wPi") {
                this.pins_list.push(<WPIPin pin={pin} />)
            } else {
                this.pins_list.push(<BlankPin pin={pin} />)
            }
        }
    }

    render() {
        return (
            <div className="flex-container">
                {this.pins_list}
            </div>
        );
    }
}

class WPIPin extends React.Component {
    constructor(props) {
        super(props);

        this.MODE_IN = this.STATUS_ON = "btn-gpio mode-switch btn-on";
        this.MODE_OUT = this.STATUS_OFF = "btn-gpio mode-switch btn-off";
        this.UNLOCKED = "fas fa-lock-open lock-icon";
        this.LOCKED = "fas fa-lock lock-icon";

        this.state = {
            mode: 1,
            state: 0,
            locked: false
        }
    }

    render() {
        return (
            <div className="pin-container icon-gpio text-gpio" data-pinId="8">
                <i className="icon-info fas fa-info-circle" data-toggle="tooltip" title={this.props.pin.meta}></i>
                <span>wPi {this.props.pin.wPi}</span>
                <i className="fas fa-lock-open lock-icon"></i>
                <button className="btn-gpio mode-switch btn-off">OUT</button>
                <button className="btn-gpio status-switch btn-off">OFF</button>
            </div>
        )
    }
}

class BlankPin extends React.Component {
    render() {
        if (this.props.pin.type === "5_power") {
            return (
                <div className="pin-container pin-power">
                    <span>+5V Power</span>
                </div>
            );
        } else if (this.props.pin.type === "3.3_power") {
            return (
                <div className="pin-container pin-power">
                    <span>+3.3V Power</span>
                </div>
            );
        } else if (this.props.pin.type === "ground") {
            return (
                <div className="pin-container pin-gnd">
                    <span>Ground</span>
                </div>
            )
        }
    }
}