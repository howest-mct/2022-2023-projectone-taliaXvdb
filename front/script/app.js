const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

// #region ***  DOM references                           ***********
// #endregion

// #region ***  Callback-Visualisation - show___         ***********

const showError = function (error) {
  console.error(error);
};

const showHistory = function (jsonObject) {
  console.info(jsonObject);
  const htmlTable = document.querySelector('.js-historyTable');
  htmlTable.innerHTML = `<tr>
      <th>ID</th>
      <th>deviceID</th>
      <th>date</th>
      <th>value</th>
    </tr>
  <tbody>`;
  for (const record of jsonObject.history) {
    // console.info(record)
    htmlTable.innerHTML += `<tr>
    <td>${record.ID}</td>
    <td>${record.deviceID}</td>
    <td>${record.date}</td>
    <td>${record.value}</td>
    </tr>`;
  }
  htmlTable.innerHTML += `</tbody></table>`;
};

const showReadings = function (jsonObject) {
  console.info(jsonObject);
  const htmlHistory = document.querySelector('.js-historytable');
  const htmlButton = document.querySelectorAll('.js-btn');
  for (const record of jsonObject.history) {
    console.info(record);
    htmlHistory.innerHTML += `
    <tr>
      <td>${record.ID}</td>
      <td>${record.deviceID}</td>
      <td>${record.actionID}</td>
      <td>${record.date}</td>
      <td>${record.value}</td>
      <td>${record.comment}</td>
    </tr>
    `;
  }
  for (const btn of htmlButton) {
    btn.addEventListener('click', function () {
      if (btn.getAttribute('data-temperature')) {
      }
    });
  }
};

const showProgress = function (progress, color) {
  var canvas = document.getElementById('progressCanvas');
  var context = canvas.getContext('2d');

  var centerX = canvas.width / 2;
  var centerY = canvas.height / 2;
  var radius = 80;
  var startAngle = -0.5 * Math.PI;
  var endAngle = (2 * progress - 0.5) * Math.PI;

  context.clearRect(0, 0, canvas.width, canvas.height);

  // Tekenen van de voortgangscirkel
  context.beginPath();
  context.arc(centerX, centerY, radius, startAngle, endAngle);
  context.lineWidth = 10;
  context.strokeStyle = color;
  context.stroke();

  // Toevoegen van het percentage als tekst in de cirkel
  var percentage = Math.round(progress * 100);
  context.font = '28px Oscine';
  context.fillStyle = '#000000';
  context.textAlign = 'center';
  context.textBaseline = 'middle';
  context.fillText(percentage + '%', centerX, centerY);
};
// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********
// #endregion

// #region ***  Data Access - get___                     ***********

const getHistory = function () {
  const userid = localStorage.getItem('userid');
  const url = `http://192.168.168.169:5000/api/v1/waterreminder/user/2/`;
  handleData(url, showHistory, showError);
};

const getOverview = function () {};

const getReadings = function () {
  let userid = window.localStorage.getItem('userid');
  const url = `http://127.0.0.1:5000/api/v1/waterreminder/user/${userid}/`;
  handleData(url, showReadings, showError);
};
// #endregion

// #region ***  Event Listeners - listenTo___            ***********
// #endregion

//#region ***  DOM references

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
  const htmlRfid = document.querySelector('.js-rfid');
  socketio.on('connect', function () {
    console.info('succesfully connected to socket');
    socketio.emit('F2B_readrfid');
  });
  socketio.on('B2F_showid', function (id) {
    console.info(id);
    htmlRfid.innerHTML += id;
    localStorage.setItem('userid', id);
    window.location = 'index.html';
  });
};

const initIndex = function () {
  console.info('init index');
  showProgress(0.76, '#4DABF7');
  htmlTemp = document.querySelector('.js-temp');
  htmlGoal = document.querySelector('.js-goal');
  htmlTime = document.querySelector('.js-time');
  socketio.on('connect', function () {
    console.info('succesfully connected to socket');
    socketio.emit('F2B_getgoal');
    socketio.emit('F2B_gettemp');
  });
  socketio.on('B2F_showtemp', function (temp) {
    console.info(temp);
    htmlTemp.innerHTML = temp;
  });
  socketio.on('B2F_showgoal', function (goal) {
    console.info(goal.goal);
    htmlGoal.innerHTML = goal.goal;
  });
};

const initOverview = function () {
  console.info('init overview');
  htmlTemp = document.querySelector('.js-temp');
  htmlWeight = document.querySelector('.js-weight');
  socketio.on('connect', function () {
    console.info('succesfully connected to socket');
    socketio.emit('F2B_getweight');
    socketio.emit('F2B_gettemp');
  });
  // socketio.on('B2F_showweight', function (weight) {
  //   console.info(weight.value);
  //   htmlWeight.innerHTML += weight.value;
  // });
};

const initReadings = function () {
  console.info('init readings');
  getHistory();
};

const initSettings = function () {
  console.info('init settings');
};

document.addEventListener('DOMContentLoaded', init);
// #endregion
