var form_1 = document.querySelector(".form_1");
var form_2 = document.querySelector(".form_2");
var form_3 = document.querySelector(".form_3");
var form_4 = document.querySelector(".form_4");
var form_5 = document.querySelector(".form_5");


var form_1_btns = document.querySelector(".form_1_btns");
var form_2_btns = document.querySelector(".form_2_btns");
var form_3_btns = document.querySelector(".form_3_btns");
var form_4_btns = document.querySelector(".form_4_btns");
var form_5_btns = document.querySelector(".form_5_btns");


var form_1_next_btn = document.querySelector(".form_1_btns .btn_next");
var form_2_back_btn = document.querySelector(".form_2_btns .btn_back");
var form_2_next_btn = document.querySelector(".form_2_btns .btn_next");
var form_3_back_btn = document.querySelector(".form_3_btns .btn_back");
var form_3_next_btn = document.querySelector(".form_3_btns .btn_next");
var form_4_back_btn = document.querySelector(".form_4_btns .btn_back");
var form_4_next_btn = document.querySelector(".form_4_btns .btn_next");
var form_5_back_btn = document.querySelector(".form_5_btns .btn_back");

var form_2_progessbar = document.querySelector(".form_2_progessbar");
var form_3_progessbar = document.querySelector(".form_3_progessbar");
var form_4_progessbar = document.querySelector(".form_4_progessbar");
var form_5_progessbar = document.querySelector(".form_5_progessbar");

var btn_done = document.querySelector(".btn_done");
var modal_wrapper = document.querySelector(".modal_wrapper");
var shadow = document.querySelector(".shadow");

// для формы добавления объявления по первому шагу беру уникальные айди
var title = document.querySelector('#id_title');
var property_description = document.querySelector('#id_property_description');
var phone = document.querySelector('#id_phone');

form_1_next_btn.addEventListener("click", function(){
// если все поля заполнены, кнопка перехода на следующий шаг становится активной
if (title.value !== '' && property_description.value !== ''&& phone.value.length == 14) {
	form_1.style.display = "none";
	form_2.style.display = "block";

	form_1_btns.style.display = "none";
	form_2_btns.style.display = "flex";

	form_2_progessbar.classList.add("active");

	title.style.border = '1px solid #dee2e6';
	property_description.style.border = '1px solid #dee2e6';
	phone.style.border = '1px solid #dee2e6';

    // проверка на заполнение полей для перехода на следующий шаг
	} else { if (title.value == '') {
            title.style.border = '0.1rem solid red';
            document.getElementsByClassName('req1')[0].style.color='red';
                } else { if (property_description.value == '') {
                        property_description.style.border = '0.1rem solid red';
                        document.getElementsByClassName('req2')[0].style.color='red';
                    } else { if (phone.value.length < 14) {
                    phone.style.border = '0.1rem solid red';
                    document.getElementsByClassName('req3')[0].style.color='red';
                        } else {}
                    }
                }
            }
});


form_2_back_btn.addEventListener("click", function(){
	form_1.style.display = "block";
	form_2.style.display = "none";

	form_1_btns.style.display = "flex";
	form_2_btns.style.display = "none";

	form_2_progessbar.classList.remove("active");
});


var images = document.getElementById('target_div');

form_2_next_btn.addEventListener("click", function(){
if (images.innerHTML.length > 0) {
	form_2.style.display = "none";
	form_3.style.display = "block";

	form_3_btns.style.display = "flex";
	form_2_btns.style.display = "none";

	form_3_progessbar.classList.add("active");

    document.getElementsByClassName('req4')[0].style.color='black';

	} else { if (images.innerHTML.length == 0) {
            document.getElementsByClassName('req4')[0].style.color='red';
                }
	        }
});

form_3_back_btn.addEventListener("click", function(){
	form_2.style.display = "block";
	form_3.style.display = "none";

	form_3_btns.style.display = "none";
	form_2_btns.style.display = "flex";

	form_3_progessbar.classList.remove("active");
});


var address = document.querySelector('#address');
var city = document.querySelector('#city');
var state = document.querySelector('#state');
var postcode = document.querySelector('#postcode');

form_3_next_btn.addEventListener("click", function(){
if (address.value !== '' && city.value !== '' && state.value !== '' && postcode.value !== '') {
	form_3.style.display = "none";
	form_4.style.display = "block";

	form_3_btns.style.display = "none";
	form_4_btns.style.display = "flex";

	form_4_progessbar.classList.add("active");

    address.style.border = '0.1rem solid #dee2e6';
    document.getElementsByClassName('req5')[0].style.color='black';

    city.style.border = '0.1rem solid #dee2e6';
    document.getElementsByClassName('req6')[0].style.color='black';

    state.style.border = '0.1rem solid #dee2e6';
    document.getElementsByClassName('req7')[0].style.color='black';

    postcode.style.border = '0.1rem solid #dee2e6';
    document.getElementsByClassName('req8')[0].style.color='black';


	} else { if (address.value == '') {
            address.style.border = '0.1rem solid red';
            document.getElementsByClassName('req5')[0].style.color='red';
                } else { if (city.value == '') {
                        city.style.border = '0.1rem solid red';
                        document.getElementsByClassName('req6')[0].style.color='red';
                    } else { if (state.value == '') {
                        state.style.border = '0.1rem solid red';
                        document.getElementsByClassName('req7')[0].style.color='red';
                    } else { if (postcode.value == '') {
                        postcode.style.border = '0.1rem solid red';
                        document.getElementsByClassName('req8')[0].style.color='red';
                    }
                    }
                }
            }
        }
});

form_4_back_btn.addEventListener("click", function(){
	form_3.style.display = "block";
	form_4.style.display = "none";

	form_4_btns.style.display = "none";
	form_3_btns.style.display = "flex";

	form_4_progessbar.classList.remove("active");
});


var property_type = document.querySelector('#id_property_type');
var bedrooms = document.querySelector('#id_bedrooms');
var bathrooms = document.querySelector('#id_bathrooms');
var price = document.querySelector('#id_price');
var square_footage = document.querySelector('#id_square_footage');

form_4_next_btn.addEventListener("click", function(){
if (property_type.value !== '' && bedrooms.value !== '' && bathrooms.value !== ''
    && price.value !== '' && square_footage.value !== '') {
	form_4.style.display = "none";
	form_5.style.display = "block";

	form_4_btns.style.display = "none";
	form_5_btns.style.display = "flex";

	form_5_progessbar.classList.add("active");


	} else { if (property_type.value == '') {
            property_type.style.border = '0.1rem solid red';
            document.getElementsByClassName('req9')[0].style.color='red';
                } else { if (bedrooms.value == '') {
                        bedrooms.style.border = '0.1rem solid red';
                        document.getElementsByClassName('req10')[0].style.color='red';
                    } else { if (bathrooms.value == '') {
                        bathrooms.style.border = '0.1rem solid red';
                        document.getElementsByClassName('req11')[0].style.color='red';
                    } else { if (price.value.trim().length === 0) {
                        price.style.border = '0.1rem solid red';
                        document.getElementsByClassName('req12')[0].style.color='red';
                    } else { if (square_footage.value.trim().length === 0) {
                        square_footage.style.border = '0.1rem solid red';
                        document.getElementsByClassName('req13')[0].style.color='red';
                    }
                    }
                    }
                    }
                }
            }
});

form_5_back_btn.addEventListener("click", function(){
	form_4.style.display = "block";
	form_5.style.display = "none";

	form_5_btns.style.display = "none";
	form_4_btns.style.display = "flex";

	form_5_progessbar.classList.remove("active");
});

btn_done.addEventListener("click", function(){
	modal_wrapper.classList.add("active");
	btn_done.type="submit";
})

shadow.addEventListener("click", function(){
	modal_wrapper.classList.remove("active");
})