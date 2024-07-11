const city = document.querySelector(".location");
const date = document.querySelector(".date");
const weather_image = document.querySelector(".weather-img");
const temperature = document.querySelector(".temp")
const wind = document.querySelector(".wind")
const pressure = document.querySelector(".pressure")
const humidity = document.querySelector(".humidity")
const weather_state = document.querySelector(".weather-state")

//geolocation api
if(navigator.geolocation){
  navigator.geolocation.getCurrentPosition(success,error);
}
else{
  alert("Geolocation feature not supported");
}

async function success(position){
   const lat = position.coords.latitude;
   const long = position.coords.longitude;
   console.log(lat,long);
   let apiUrl = `http://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${long}&APPID=3af25885126dbc4791bba802e680a5c3`
   const response = await fetch(apiUrl);
   let data = await response.json();
   console.log(data);
  city.innerHTML = data.name;
  date.innerHTML = Date.now();
  temperature.innerHTML = Math.round((data.main.temp - 32) * (5/9));
  wind.innerHTML = data.wind.speed;
  pressure.innerHTML = data.main.pressure;
  humidity.innerHTML = data.main.humidity;
  weather_state.innerHTML = data.weather[0].description;

  //weather image
  switch(data.weather[0].main){
    case "Rain":
      weather_image.src = 'static/images/rain.png';
      break;
    case "Clear":
      weather_image.src = 'static/images/clear.png';
      break;
    case "Mist":
      weather_image.src = 'static/images/mist.png';
      break;
    case "Clouds":
        weather_image.src = 'static/images/clouds.png';
        break;
    default:
      weather_image.src = 'static/images/drizzle.png';
  }
}
function error(error){
  alert("Geolocation feature not supported");
}
