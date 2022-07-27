function convert_none_to_zero(value) {
    return (value == "None") ? 0 : value;
}

function update_species_selector(category_id, selected_species_id) {
    $.ajax({
        url: "/sightings/list_species/" +
            convert_none_to_zero(category_id) + "/" +
            convert_none_to_zero(selected_species_id),
        type: "GET",
        cache: false,
        dataType: "html",
        success: function(data, _textStatus, _jqXHR)  {
            $("#species_selector").html(data);
        },
        error: function(_jqXHR, textStatus, _errorThrown) {
            $("#species_selector").html("Error getting species list: " + textStatus);
        }
    });
}

function initialise_species_selection(category_id, species_id) {
    // Update the species list for the selected category and select the current species
    update_species_selector(category_id, species_id);

    // When the category selection changes, update the species list
    $("#category").change(function () {
        let updated_category_id = $("#category").val();
        update_species_selector(updated_category_id, 0);
    });
}
