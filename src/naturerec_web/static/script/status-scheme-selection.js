function convert_none_to_zero(value) {
    return (value == "None") ? 0 : value;
}

function update_rating_selector(scheme_id) {
    $.ajax({
        url: "/species_ratings/list_scheme_ratings/" + convert_none_to_zero(scheme_id),
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

function initialise_rating_selection() {
    // Set up the initial rating list
    update_rating_selector(0);

    // When the scheme selection changes, update the rating list
    $("#scheme").change(function () {
        var scheme_id = $("#scheme").val();
        update_rating_selector(scheme_id);
    });
}
