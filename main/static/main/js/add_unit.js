$('#ifile_1').click(function () {
    // when the add file button is clicked append
    // a new <input type="file" name="someName" />
    // to a target_div div
    var input = $('<input/>')
                .attr('type', "file")
                .attr('name', "images")
                .attr('class', "form-control")
                .attr('accept', "image/*")
                .attr('onchange', "handleFiles1(this.files)")
                .attr('id', "id_images");

    //Create array of options to be added
    var array = ['Select bedrooms','Studio', '1 bed', '2 bed', '3 bed', '4 bed+'];
    var bedroom_unit = $('<select>')
        .attr('class', "select form-select")
        .attr('name', "bedrooms_unit")
        .attr('id', "id_bedrooms_unit");

    var array1 = ['Select bathrooms', '1 bath', '1.5 bath', '2 bath', '2.5 bath',
                '3 bath', '3.5 bath', '4 bath+'];
    var bathroom_unit = $('<select/>')
        .attr('class', "select form-select")
        .attr('name', "bathrooms_unit")
        .attr('id', "id_bathrooms_unit");

    var price_unit = $('<input/>')
        .attr('type', "number")
        .attr('class', "form-control")
        .attr('placeholder', "Price")
        .attr('name', "price_unit")
        .attr('id', "id_price_unit");

    var square_footage_unit = $('<input/>')
        .attr('type', "number")
        .attr('class', "form-control")
        .attr('placeholder', "Square footage")
        .attr('name', "square_footage_unit")
        .attr('id', "id_square_footage_unit");

    var title_unit = $('<input/>')
        .attr('type', "text")
        .attr('class', "form-control")
        .attr('placeholder', "Unit title")
        .attr('name', "title_unit")
        .attr('id', "id_title_unit");

    var div_row1 = $('<div/>')
        .attr('class', 'row');

    var div_row2 = $('<div/>')
        .attr('class', 'row');

    var div_row_col1 = $('<div/>')
        .attr('class', 'col-6')
        .attr('style', 'margin: auto;');

    var div_row_col2 = $('<div/>')
        .attr('class', 'col-6')
        .attr('style', 'margin: auto;');

    var div_row_col3 = $('<div/>')
        .attr('class', 'col-6')
        .attr('style', 'margin: auto;');

    var div_row_col4 = $('<div/>')
        .attr('class', 'col-6')
        .attr('style', 'margin: auto;');

    var tag_p0 = $('<p/>');
    var tag_p = $('<p/>');
    var tag_p1 = $('<p/>');
    var tag_p2 = $('<p/>');
    var tag_br = $('<hr/>');

    //append the created file input
    var cols1 = div_row_col1.append(bedroom_unit);
    var cols2 = div_row_col2.append(bathroom_unit);
    var rows1 = div_row1.append(cols1, cols2);

    var cols3 = div_row_col3.append(price_unit);
    var cols4 = div_row_col4.append(square_footage_unit);
    var rows2 = div_row2.append(cols3, cols4);

    $('#target_div_1').append(title_unit, tag_p0, rows1, tag_p, rows2, tag_p1, input, tag_p2, tag_br);
        //Create and append the options
    for (var i = 0; i < array.length; i++) {
        var option = document.createElement("option");
        option.value = array[i];
        option.text = array[i];
        bedroom_unit.append(option);
    }
    for (var i = 0; i < array1.length; i++) {
        var option = document.createElement("option");
        option.value = array1[i];
        option.text = array1[i];
        bathroom_unit.append(option);
    }
    //initializing Multifile on the input element
    input.MultiFile();
});