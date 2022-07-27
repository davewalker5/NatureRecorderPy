function geocode_location(postcode, country) {
    $.ajax({
        url: "/locations/geocode/" + postcode + "/" + country,
        type: "GET",
        cache: false,
        dataType: "json",
        success: function(data, _textStatus, _jqXHR)  {
            $("#latitude").val(data.latitude);
            $("#longitude").val(data.longitude);
        },
        error: function(_jqXHR, _textStatus, _errorThrown) {
            // Nothing to do here, for now
        }
    });
}
