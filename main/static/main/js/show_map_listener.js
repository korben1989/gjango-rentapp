var address = document.querySelector('#address');
var map = document.querySelector('#map');
//var map = document.getElementsByClassName('req17');

address.addEventListener('change', () => {
 if (address.value.trim() !== "") {
     console.log('ok');
     console.log(map.style);
     map.style.display = 'block';
 }
});