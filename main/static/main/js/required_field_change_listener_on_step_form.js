var title = document.querySelector('#id_title');
var property_description = document.querySelector('#id_property_description');
var phone = document.querySelector('#id_phone');

var images = document.getElementById('target_div');

var address = document.querySelector('#address');
var city = document.querySelector('#city');
var state = document.querySelector('#state');
var postcode = document.querySelector('#postcode');

var property_type = document.querySelector('#id_property_type');
var bedrooms = document.querySelector('#id_bedrooms');
var bathrooms = document.querySelector('#id_bathrooms');
var price = document.querySelector('#id_price');
var square_footage = document.querySelector('#id_square_footage');

title.addEventListener('change', () => {
 if (title.value.trim() == "") {
     title.style.border = '0.1rem solid red';
     document.getElementsByClassName('req1')[0].style.color='red';
     return false;
 } else {
   title.style.border = '1px solid #dee2e6';
   document.getElementsByClassName('req1')[0].style.color='black';
   return true; }

});

property_description.addEventListener('change', () => {
 if (property_description.value.trim() == "") {
     property_description.style.border = '0.1rem solid red';
     document.getElementsByClassName('req2')[0].style.color='red';
     return false;
 } else {
   property_description.style.border = '1px solid #dee2e6';
   document.getElementsByClassName('req2')[0].style.color='black';
   return true; }

});

phone.addEventListener('change', () => {
 if (phone.value.trim() == "") {
     phone.style.border = '0.1rem solid red';
     document.getElementsByClassName('req3')[0].style.color='red';
     return false;
 } else {
   phone.style.border = '1px solid #dee2e6';
   document.getElementsByClassName('req3')[0].style.color='black';
   return true; }

});

images.addEventListener('change', () => {
 if (images.innerHTML.length == 0) {
     document.getElementsByClassName('req4')[0].style.color='red';
     return false;
 } else {
   document.getElementsByClassName('req4')[0].style.color='black';
   return true; }

});

address.addEventListener('change', () => {
 if (address.value.trim() == "") {
     address.style.border = '0.1rem solid red';
     document.getElementsByClassName('req5')[0].style.color='red';
     return false;
 } else {
   address.style.border = '1px solid #dee2e6';
   document.getElementsByClassName('req5')[0].style.color='black';
   return true; }

});

city.addEventListener('change', () => {
 if (city.value.trim() == "") {
     city.style.border = '0.1rem solid red';
     document.getElementsByClassName('req6')[0].style.color='red';
     return false;
 } else {
   city.style.border = '1px solid #dee2e6';
   document.getElementsByClassName('req6')[0].style.color='black';
   return true; }

});

state.addEventListener('change', () => {
 if (state.value.trim() == "") {
     state.style.border = '0.1rem solid red';
     document.getElementsByClassName('req7')[0].style.color='red';
     return false;
 } else {
   state.style.border = '1px solid #dee2e6';
   document.getElementsByClassName('req7')[0].style.color='black';
   return true; }

});

postcode.addEventListener('change', () => {
 if (postcode.value.trim() == "") {
     postcode.style.border = '0.1rem solid red';
     document.getElementsByClassName('req8')[0].style.color='red';
     return false;
 } else {
   postcode.style.border = '1px solid #dee2e6';
   document.getElementsByClassName('req8')[0].style.color='black';
   return true; }

});

property_type.addEventListener('change', () => {
 if (property_type.value.trim() == "") {
     property_type.style.border = '0.1rem solid red';
     document.getElementsByClassName('req9')[0].style.color='red';
     return false;
 } else {
   property_type.style.border = '1px solid #dee2e6';
   document.getElementsByClassName('req9')[0].style.color='black';
   return true; }

});

bedrooms.addEventListener('change', () => {
 if (bedrooms.value.trim() == "") {
     bedrooms.style.border = '0.1rem solid red';
     document.getElementsByClassName('req10')[0].style.color='red';
     return false;
 } else {
   bedrooms.style.border = '1px solid #dee2e6';
   document.getElementsByClassName('req10')[0].style.color='black';
   return true; }

});

bathrooms.addEventListener('change', () => {
 if (bathrooms.value.trim() == "") {
     bathrooms.style.border = '0.1rem solid red';
     document.getElementsByClassName('req11')[0].style.color='red';
     return false;
 } else {
   bathrooms.style.border = '1px solid #dee2e6';
   document.getElementsByClassName('req11')[0].style.color='black';
   return true; }

});

price.addEventListener('change', () => {
 if (price.value.trim() == "") {
     price.style.border = '0.1rem solid red';
     document.getElementsByClassName('req12')[0].style.color='red';
     return false;
 } else {
   price.style.border = '1px solid #dee2e6';
   document.getElementsByClassName('req12')[0].style.color='black';
   return true; }

});

square_footage.addEventListener('change', () => {
 if (square_footage.value.trim() == "") {
     square_footage.style.border = '0.1rem solid red';
     document.getElementsByClassName('req13')[0].style.color='red';
     return false;
 } else {
   square_footage.style.border = '1px solid #dee2e6';
   document.getElementsByClassName('req13')[0].style.color='black';
   return true; }

});