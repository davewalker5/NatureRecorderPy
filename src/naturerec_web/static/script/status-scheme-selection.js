function convert_none_to_zero(value) {
    return (value == "None") ? 0 : value;
}

function update_rating_selector(scheme_id) {
    $.ajax({
        url: "/species/list_scheme_ratings/" + convert_none_to_zero(scheme_id),
        type: "GET",
        cache: false,
        dataType: "html",
        success: function(data, textStatus, jqXHR)  {
            $("#rating_selector").html(data);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $("#rating_selector").html("Error getting conservation status rating list: " + textStatus);
        }
    });
}

function initialise_scheme_selection() {
    // When the category selection changes, update the species list
    $("#scheme").change(function () {
        var scheme_id = $("#scheme").val();
        update_rating_selector(scheme_id);
    });
}
