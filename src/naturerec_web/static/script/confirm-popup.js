function set_record_id(recordId) {
    $(".modal-body #confirm-record-id").val(recordId);
}

function attach_yes_handler(confirmCallback) {
    $('#confirm-popup .modal-footer button').on('click', function(event) {
        let buttonId = $(event.target).attr("id");
        $(this).closest('.modal').one('hidden.bs.modal', function() {
            // Get the previously stored record ID and clear the field used to store it
            let recordId = $(".modal-body #confirm-record-id").val();
            set_record_id("");

            // If the action's confirmed, call the supplied callback, passing in the record ID
            if (buttonId == "confirm-yes-button") {
                confirmCallback(recordId);
            }
        });
    });
}

function attach_show_modal_handler() {
    var confirmModal = document.getElementById('confirm-popup');
    confirmModal.addEventListener('show.bs.modal', function (event) {
        // The confirmation popup's used to confirm a destructive action (deletion). The control used to trigger
        // the popup is associated with a specific record ID. Get that ID
        let element = event.relatedTarget;
        let recordId = element.getAttribute('data-bs-record-id');

        // Store the record ID for later use
        set_record_id(recordId);
    });
}

function initialise_confirm_popup(confirmCallback) {
    set_record_id("");
    attach_yes_handler(confirmCallback);
    attach_show_modal_handler();
}
