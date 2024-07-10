//geolocation api

//const apikey = f94eb871a9a9a55ca47114a1534645ef

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
   let apiUrl = `http://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${long}&APPID=3877a6b76dff6a9f49c104da5f4f31f0`
   const response = await fetch(apiUrl);
   let data = await response.json();
   console.log(data.main);
}
function error(error){
  alert("Geolocation feature not supported");
}
