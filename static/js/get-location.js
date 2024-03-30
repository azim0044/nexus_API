const http = new XMLHttpRequest();
let result = document.querySelector('#result');
let latitude = document.getElementById('event-latitude');
let longitude = document.getElementById('event-longitude');
let latitude_hidden = document.getElementById('event-latitude-hidden');
let longitude_hidden = document.getElementById('event-longitude-hidden');

const GOOGLE_MAP_API_KEY = `AIzaSyDGG_n1zVZwUen4gn7R77Ccz2ADpQgh2BY`

document.querySelector('#get-current-location').addEventListener('click', function () {
    findmycoordinate()
});

function findmycoordinate() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((showPosition) => {
            latitude.value = showPosition.coords.latitude;
            longitude.value = showPosition.coords.longitude;

            latitude_hidden.value = showPosition.coords.latitude;
            longitude_hidden.value = showPosition.coords.longitude;
            
            const url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${showPosition.coords.latitude},${showPosition.coords.longitude}&key=${GOOGLE_MAP_API_KEY}`;
            getAPI(url);
        },
            (error) => {
                console.log(error);
            }
        );
    } else {
        result.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function getAPI(url) {
    http.open("GET", url);
    http.send();
    http.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            const data = JSON.parse(this.responseText);
            if (data.results && data.results.length > 0) {
                let city = data.results[0].address_components[2].long_name;
                let state = data.results[0].address_components[4].long_name;
                let zipcode = data.results[0].address_components[6].long_name;

                let inputCity = document.getElementById('inputCity');
                let inputState = document.getElementById('inputState');
                let inputZip = document.getElementById('inputZip');

                inputCity.value = city;
                inputState.value = state;
                inputZip.value = zipcode;
            }
        }
    }
}