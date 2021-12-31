function geocode_location(postcode, country) {
    $.ajax({
        url: "/locations/geocode/" + postcode + "/" + country,
        type: "GET",
        cache: false,
        dataType: "json",
        success: function(data, textStatus, jqXHR)  {
            $("#latitude").val(data.latitude);
            $("#longitude").val(data.longitude);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            // Nothing to do here, for now
        }
    });
}
