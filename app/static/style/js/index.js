var request = new XMLHttpRequest();

request.open('GET', 'https://api.maicoin.com/v1/prices/', true);
request.onload = function () {

  // Begin accessing JSON data here
  var data = JSON.parse(this.response);

  if (request.status >= 200 && request.status < 400) {
    console.log(data.amount);
  } else {
    console.log('error');
  }
}

request.send();


