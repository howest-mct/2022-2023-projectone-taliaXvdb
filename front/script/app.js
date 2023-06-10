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

const newUser = function () {
  var newid = localStorage.getItem('userid');
  var name = document.getElementById('userName').value;
  var goal = document.getElementById('goal').value;
  var reminderType = document.getElementById('reminderType').value;
  var interval = document.getElementById('interval').value;
  var amount = document.getElementById('amount').value;
  socketio.emit('F2B_createuser', {
    newid,
    name,
    goal,
    reminderType,
    interval,
    amount,
  });
  closePopup();
};

const showPopup = function (number) {
  if (number == 1) {
    var popupContainer = document.getElementById('popupContainer');
    popupContainer.style.display = 'block';
  } else if (number == 2) {
    var popupContainer = document.getElementById('popupContainer2');
    popupContainer.style.display = 'block';
  }
};

const closePopup = function (number) {
  if (number == 1) {
    var popupContainer = document.getElementById('popupContainer');
    popupContainer.style.display = 'none';
  } else if (number == 2) {
    var popupContainer = document.getElementById('popupContainer2');
    popupContainer.style.display = 'none';
  }
};

const showTypes = function (jsonObject) {
  const htmlType = document.querySelector('.js-type');
  console.info(jsonObject);
  for (const type of jsonObject.types) {
    console.info(type);
    htmlType.innerHTML += `<option>${type.name}</option>`;
  }
};

const showLogging = function (jsonObject) {
  console.info(jsonObject);
};

const showReminders = function (jsonObject) {
  const htmlReminders = document.querySelector('.js-table');
  let htmlString = ""
  // console.info(jsonObject)
  htmlString = `<thead><tr>
      <th>type</th>
      <th>time</th>
      <th>amount</th>
    </tr></thead>
  <tbody>`;
  for (const reminder of jsonObject.reminders) {
    console.info(reminder);
    if (reminder.type == 1) {
      htmlString += `<tr>
      <td class="js-reminder" data-type="bulb"><object data="img/bulb-outline.svg" type="image/svg+xml" class="c-reminder__img js-reminder" data-type="bulb"></object></td>
      <td>${reminder.time}</td>
      <td>${reminder.amount}</td>
      </tr>`;
    } else if (reminder.type == 2) {
      htmlString += `<tr>
      <td class="js-reminder" data-type="music"><object data="img/music-outline.svg" type="image/svg+xml" class="c-reminder__img js-reminder" data-type="music"></object></td>
      <td>${reminder.time}</td>
      <td>${reminder.amount}</td>
      </tr>`;
    } else if (reminder.type == 3) {
      htmlString += `<tr>
      <td class="js-reminder" data-type="vibrate"><object data="img/phone-call-outline.svg" type="image/svg+xml" class="c-reminder__img js-reminder" data-type="vibrate"></object></td>
      <td>${reminder.time}</td>
      <td>${reminder.amount}</td>
      </tr>`;
    }
  }
  htmlString += `</tbody></table>`;
  htmlReminders.innerHTML = htmlString
  listenToClick();
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

const getReadings = function () {
  let userid = window.localStorage.getItem('userid');
  const url = `http://192.168.168.169:5000/api/v1/waterreminder/user/${userid}/`;
  handleData(url, showReadings, showError);
};

const getTypes = function () {
  const url = `http://192.168.168.169:5000/api/v1/waterreminder/type/`;
  handleData(url, showTypes, showError);
};

const getProgress = function () {
  let userid = localStorage.getItem('userid');
  const url = `http://192.168.168.169:5000/api/v1/waterreminder/user/2/logging/`;
  handleData(url, showLogging, showError);
};

const getReminders = function () {
  let userid = localStorage.getItem('userid');
  const url = `http://192.168.168.169:5000/api/v1/waterreminder/user/2/reminders/`;
  handleData(url, showReminders, showError);
};
// #endregion

// #region ***  Event Listeners - listenTo___            ***********

const listenToClick = function () {
  const remindertypes = document.querySelectorAll('.js-reminder');
  for (const type of remindertypes) {
    type.addEventListener('click', function () {
      console.info(this);
      const kind = this.getAttribute('data-type');
      console.info(kind)
      if (kind == 'bulb') {
        console.info('bulb clicked');
        socketio.emit('F2B_lighton');
      } else if (kind == 'music') {
        console.info('sound clicked');
        socketio.emit('F2B_playmusic');
      } else if (kind == 'vibrate') {
        console.info('vibrate clicked');
        socketio.emit('F2B_vibrate');
      }
    });
  }
};
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
  const htmlBtn = document.querySelector('.js-btn');
  htmlBtn.addEventListener('click', function () {
    closePopup();
  });
  // sockets
  socketio.on('connect', function () {
    console.info('succesfully connected to socket');
    socketio.emit('F2B_readrfid');
  });
  socketio.on('B2F_showid', function (id) {
    console.info(id);
    localStorage.setItem('userid', id);
    window.location = 'index.html';
  });
  socketio.on('B2F_showuser', function (id) {
    localStorage.setItem('userid', id);
    showPopup(1);
    getTypes();
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
  getProgress();
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
};

const initReadings = function () {
  console.info('init readings');
  getHistory();
};

const initSettings = function () {
  console.info('init settings');
  const htmlSave = document.querySelector('.js-save');
  const htmlDone = document.querySelector('.js-done');
  const htmlInfo = document.querySelector('.js-info');
  htmlSave.addEventListener('click', function () {
    showPopup(1);
  });
  htmlDone.addEventListener('click', function () {
    closePopup(1);
  });
  htmlInfo.addEventListener('click', function () {
    showPopup(2);
  });
  getReminders();
  listenToClick()
};

document.addEventListener('DOMContentLoaded', init);
// #endregion
