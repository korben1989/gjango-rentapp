$('#ifile').click(function () {
    // when the add file button is clicked append
    // a new <input type="file" name="someName" />
    // to a target_div div
    var input = $('<input/>')
                .attr('type', "file")
                .attr('name', "images")
                .attr('class', "form-control")
                .attr('accept', "image/*")
                .attr('onchange', "handleFiles(this.files)")
                .attr('id', "id_images");
    //append the created file input
    $('#target_div').append(input);
    //initializing Multifile on the input element
    input.MultiFile();
});