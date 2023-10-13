var i = 1;
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
                // в разных браузерах проверить, может не срабатывать
                // https://stackoverflow.com/questions/210643/in-javascript-can-i-make-a-click-event-fire-programmatically-for-a-file-input
                .attr('style', "display: none")
                .attr('id', "id_images");

//    var button = $('<button>')
//        .attr('id', "iclear"+i)
//        .attr('class', "btn btn-primary w-100 py-2")
//        .attr('type', "button");
        // button.text('Clear')

    var div = $('<div/>')
        .attr('style', "text-align:right;")
        .attr('id', "new_div"+i);

    $('#target_div').append(div);

    //append the created file input
    $('#new_div'+i).append(input.click());

    //initializing Multifile on the input element
//    input.MultiFile();

 i++;
});