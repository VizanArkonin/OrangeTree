'use strict';
// Common components for all modal windows

const modal = {
    window: {
        open: ".modal",
        close: ".modal-window-close"
    },
    user: {
        window: "#modal_user_window",
        header: "#modal_user_header",
        button: {
            open: ".modal-user-button-open",
            edit: "#modal_user_button_edit",
            add: "#modal_user_button_add",
            all: "[id *=modal_user_button]"
        },
        checkbox: {
            roles: ".modal-user-checkbox-roles",
            active: "#modal_user_checkbox_active"
        },
        field: {
            firstName: "#modal_user_field_firstName",
            lastName: "#modal_user_field_lastName",
            email: "#modal_user_field_email",
            password: "#modal_user_field_password",
            confirmPassword: "#modal_user_field_confirmPassword",
            hidden: {
                id:  "#modal_user_field_hidden_id",
                email: "#modal_user_field_hidden_email"
            }
        },
        message: {
            error: "#modal_user_message_error"
        }
    },
    device: {
        window: "#modal_device_window",
        header: "#modal_device_header",
        button: {
            open: ".modal-device-button-open",
            edit: "#modal_device_button_edit",
            add: "#modal_device_button_add",
            all: "[id *=modal_device_button]"
        },
        field: {
            id: "#modal_device_field_id",
            type: "#modal_device_field_type",
            key: "#modal_device_field_key",
            hidden: {
                id: "#modal_device_field_hidden_id",
                stateId: "#modal_device_field_hidden_stateId"
            }
        },
        message: {
            error: "#modal_device_message_error"
        }
    },
    deleteUser: {
        window: "#modal_deleteUser_window",
        button: {
            open: "#modal_deleteUser_button_open",
            del: "#modal_user_button_delete"
        },
        message: {
            name: "#modal_deleteUser_message_name"
        }
    },
    deleteDevice: {
        window: "#modal_deleteDevice_window",
        button: {
            open: "#modal_deleteDevice_button_open",
            del: "#modal_device_button_delete"
        },
        message: {
            name: "#modal_deleteDevice_message_name"
        }
    },
    logout: {
        window: "#modal_window_logout",
        button: {
            open: ".button-logout",
            close: "#modal_window_logout_button_close"
        }
    },
    animation: {
        open: "modal-animation-open",
        close: "modal-animation-close"
    }
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


