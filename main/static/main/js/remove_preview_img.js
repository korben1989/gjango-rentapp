//reset form
$("body").on("click", "[id^=iclear]", function () {
            $(this).parents("[id^=new_div]").remove();
            })