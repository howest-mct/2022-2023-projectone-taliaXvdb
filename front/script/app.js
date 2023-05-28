const lanIP = `${window.location.hostname}:5000`;
// const socketio = io(lanIP);

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
  const htmlButton = document.querySelector('.js-button')
  const htmlInput = document.querySelector('.js-input')
  htmlInput.addEventListener('change', function(){
    let userid = htmlInput.value
    console.info(userid)
  })
  htmlButton.addEventListener('click', function(){
    console.info('clicked')
  })
};

const initIndex = function () {
  console.info('init index');
};

const initOverview = function () {
  console.info('init overview');
};

const initReadings = function () {
  console.info('init readings');
};

const initSettings = function () {
  console.info('init settings');
};

document.addEventListener('DOMContentLoaded', init);
