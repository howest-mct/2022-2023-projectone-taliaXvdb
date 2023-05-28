const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

//#region ***  DOM references

//#endregion

//#region ***  Callback-Visualisation - show___         ***********
const showError = function (error) {
  console.error(error);
};

const showReadings = function (jsonObject) {
  console.info(jsonObject);
  const htmlHistory = document.querySelector('.js-historytable')
  const htmlButton = document.querySelectorAll('.js-btn')
  for(const record of jsonObject.history){
    console.info(record)
    htmlHistory.innerHTML += `
    <tr>
      <td>${record.ID}</td>
      <td>${record.deviceID}</td>
      <td>${record.actionID}</td>
      <td>${record.date}</td>
      <td>${record.value}</td>
      <td>${record.comment}</td>
    </tr>
    `
  }
  for(const btn of htmlButton){
    btn.addEventListener('click', function (){
      if(btn.getAttribute('data-temperature')){

      }
    })
  }
};
//#endregion

//#region ***  Callback-No Visualisation - callback___  ***********
//#endregion

//#region ***  Data Access - get___                     ***********
const getOverview = function () {};

const getReadings = function () {
  let userid = window.localStorage.getItem('userid')
  const url = `http://127.0.0.1:5000/api/v1/waterreminder/user/${userid}/`;
  handleData(url, showReadings, showError);
};
//#endregion

//#region ***  Event Listeners - listenTo___            ***********
//#endregion

//#region ***  Init / DOMContentLoaded                  ***********
const init = function () {
  console.info('DOM geladen');

  const login = document.querySelector('.js-pagelogin');
  const index = document.querySelector('.js-pageindex');
  const overview = document.querySelector('.js-pageoverview');
  const readings = document.querySelector('.js-pagereadings');
  const settings = document.querySelector('.js-pagesettings');

  if (login) {
    initLogin();
  } else if (index) {
    initIndex();
  } else if (overview) {
    initOverview();
  } else if (readings) {
    initReadings();
  } else if (settings) {
    initSettings();
  }
};

const initLogin = function () {
  console.info('init login');

  //queryselectors
  const htmlButton = document.querySelector('.js-button');
  const htmlInput = document.querySelector('.js-input');
  htmlInput.addEventListener('change', function () {
    let userid = htmlInput.value;
    console.info(userid);
    window.localStorage.setItem('userid', userid);
  });
  htmlButton.addEventListener('click', function () {
    console.info('clicked');
    window.location = 'index.html';
  });
};

const initIndex = function () {
  console.info('init index');
};

const initOverview = function () {
  console.info('init overview');
  getOverview();
};

const initReadings = function () {
  console.info('init readings');

  getReadings();
};

const initSettings = function () {
  console.info('init settings');
};

document.addEventListener('DOMContentLoaded', init);
//#endregion
