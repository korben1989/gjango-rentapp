function initialize() {
    initAutocomplete();
    initMap();

}
var map, marker;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 12,
//      center: {lat: 0, lng: 0},
      zoomControl: true,
      mapTypeControl: false,
  		scaleControl: false,
  		streetViewControl: false,
  		rotateControl: false,
  		fullscreenControl: false
    });
  }

    //var placeSearch, autocomplete;
    //var componentForm = {
    //  locality: 'long_name',
    //  route: 'long_name',
    //  street_number: 'short_name',
    //  postal_code: 'short_name'
    //};

let address1Field;
let address2Field;
let address3Field;
let postalField;
let locationField;
function initAutocomplete() {
    address1Field = document.querySelector("#address");
    address2Field = document.querySelector("#area");
    address3Field = document.querySelector("#neighborhood");
    postalField = document.querySelector("#postcode");
    locationField = document.querySelector("#location");
  // Create the autocomplete object, restricting the search to geographical
  // location types.
  autocomplete = new google.maps.places.Autocomplete(address1Field, {
    componentRestrictions: { country: ["us"] },
    fields: ["address_components", "geometry"],
    types: ["address"],
  });

  // When the user selects an address from the dropdown, populate the address
  // fields in the form.
  autocomplete.addListener('place_changed', fillInAddress);
}

function fillInAddress() {
  // Get the place details from the autocomplete object.
  var place = autocomplete.getPlace();
  if (place.geometry.viewport) {
    map.fitBounds(place.geometry.viewport);
  } else {
    map.setCenter(place.geometry.location);
    map.setZoom(16);
  }
  if (!marker) {
    marker = new google.maps.Marker({
      map: map,
      anchorPoint: new google.maps.Point(0, -29)
    });
  } else marker.setMap(null);
  marker.setOptions({
    position: place.geometry.location,
    map: map
  });


  let address1 = "";
  let address2 = "";
  let address3 = "";
  let postcode = "";
  let location = "";

  // Get each component of the address from the place details,
  // and then fill-in the corresponding field on the form.
  // place.address_components are google.maps.GeocoderAddressComponent objects
  // which are documented at http://goo.gle/3l5i5Mr
  for (const component of place.address_components) {
    // @ts-ignore remove once typings fixed
    const componentType = component.types[0];

    switch (componentType) {
      case "street_number": {
        address1 = `${component.long_name} ${address1}`;
        break;
      }

      case "route": {
        address1 += component.short_name;
        break;
      }

       case "sublocality_level_1": {
        address2 = `${component.long_name} ${address2}`;
        break;
      }

      case "neighborhood": {
        address3 = `${component.long_name} ${address3}`;
        break;
      }

      case "postal_code": {
        postcode = `${component.long_name}${postcode}`;
        break;
      }

      case "postal_code_suffix": {
        postcode = `${postcode}-${component.long_name}`;
        break;
      }

      case "locality":
        document.querySelector("#city").value = component.long_name;
        break;

      case "administrative_area_level_1": {
        document.querySelector("#state").value = component.short_name;
        break;
      }
//      case "country":
//        document.querySelector("#country").value = component.long_name;
//        break;
    }
  }


  address1Field.value = address1;
  address2Field.value = address2;
  address3Field.value = address3;
  postalField.value = postcode;

  locationField.value = place.geometry.location;
//  for (var component in componentForm) {
//    document.getElementById(component).value = '';
//    document.getElementById(component).disabled = false;
//  }
//
//
//  for (var i = 0; i < place.address_components.length; i++) {
//
//
//    var addressType = place.address_components[i].types[0];
//    if (componentForm[addressType]) {
//      var val = place.address_components[i][componentForm[addressType]];
//      document.getElementById(addressType).value = val;
//    }
//  }
}

function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var geolocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      var circle = new google.maps.Circle({
        center: geolocation,
        radius: position.coords.accuracy
      });
      autocomplete.setBounds(circle.getBounds());
    });
  }
}
