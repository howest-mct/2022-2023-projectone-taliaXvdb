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
  let htmlString = '';
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
      <td class="js-reminder" data-type="bulb"><img src="img/bulb-outline.svg" class="c-reminder__img js-reminder" data-type="bulb"></img></td>
      <td class="js-time" data-type="bulb">${reminder.time}</td>
      <td class="js-amount" data-type="bulb">${reminder.amount}</td>
      </tr>`;
    } else if (reminder.type == 2) {
      htmlString += `<tr>
      <td class="js-reminder" data-type="music"><img src="img/music-outline.svg" class="c-reminder__img js-reminder" data-type="music"></img></td>
      <td class="js-time" data-type="music">${reminder.time}</td>
      <td class="js-amount" data-type="music">${reminder.amount}</td>
      </tr>`;
    } else if (reminder.type == 3) {
      htmlString += `<tr>
      <td class="js-reminder" data-type="vibrate"><img src="img/phone-call-outline.svg" class="c-reminder__img js-reminder" data-type="vibrate"></img></td>
      <td class="js-time" data-type="vibrate">${reminder.time}</td>
      <td class="js-amount" data-type="vibrate">${reminder.amount}</td>
      </tr>`;
    }
  }
  htmlString += `</tbody></table>`;
  htmlReminders.innerHTML = htmlString;
  listenToClick();
};

const showGraph = function (title, labels, axistitle) {
  var options = {
    series: [
      {
        name: labels[0],
        data: [28, 29, 33, 36, 32, 32, 33],
      },
      {
        name: labels[1],
        data: [12, 11, 14, 18, 17, 13, 13],
      },
    ],
    chart: {
      height: 350,
      type: 'line',
      dropShadow: {
        enabled: true,
        color: '#000',
        top: 18,
        left: 7,
        blur: 10,
        opacity: 0.2,
      },
      toolbar: {
        show: false,
      },
    },
    colors: ['#545454', '#77B6EA'],
    dataLabels: {
      enabled: true,
    },
    stroke: {
      curve: 'smooth',
    },
    title: {
      text: title,
      align: 'left',
    },
    grid: {
      borderColor: '#e7e7e7',
      row: {
        colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
        opacity: 0.5,
      },
    },
    markers: {
      size: 1,
    },
    xaxis: {
      categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
      title: {
        text: axistitle[0],
      },
    },
    yaxis: {
      title: {
        text: axistitle[1],
      },
      min: 5,
      max: 40,
    },
    legend: {
      position: 'top',
      horizontalAlign: 'right',
      floating: true,
      offsetY: -25,
      offsetX: -5,
    },
  };

  var chart = new ApexCharts(document.querySelector('.js-chart'), options);
  chart.render();
};

const showLastLog = function (jsonObject) {
  console.info(jsonObject);
  const title = 'Did I reach my goal?';
  const labels = ['goal', 'what i drank'];
  const axistitles = ['Date', 'Amount(ml)'];
  let goalData = [];
  let amountDrank = [];
  socketio.emit('F2B_getgoal');
  socketio.on('B2F_showgoal', function (goal) {
    for (const logged of jsonObject.data) {
      console.info(logged.total)
      goalData.push(jsonObject.user.goal);
      amountDrank.push(logged.total)
    }
    showGraph(title, labels, axistitles);
  });
};
// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********
// #endregion

// #region ***  Data Access - get___                     ***********

const getHistory = function () {
  const userid = localStorage.getItem('userid');
  const url = `http://${lanIP}/api/v1/waterreminder/user/${userid}/`;
  handleData(url, showHistory, showError);
};

const getReadings = function () {
  let userid = window.localStorage.getItem('userid');
  const url = `http://${lanIP}/api/v1/waterreminder/user/${userid}/`;
  handleData(url, showReadings, showError);
};

const getTypes = function () {
  const url = `http://${lanIP}/api/v1/waterreminder/type/`;
  handleData(url, showTypes, showError);
};

const getProgress = function () {
  let userid = localStorage.getItem('userid');
  const url = `http://${lanIP}/api/v1/waterreminder/user/${userid}/logging/`;
  handleData(url, showLogging, showError);
};

const getReminders = function () {
  let userid = localStorage.getItem('userid');
  const url = `http://${lanIP}/api/v1/waterreminder/user/${userid}/reminders/`;
  handleData(url, showReminders, showError);
};

const getLastLog = function () {
  let userid = localStorage.getItem('userid');
  const url = `http://${lanIP}/api/v1/waterreminder/user/${userid}/logging/last/`;
  handleData(url, showLastLog, showError);
};

const getAllLogs = function () {
  let userid = localStorage.getItem('userid');
  const url = `http://${lanIP}/api/v1/waterreminder/user/${userid}/logging/`;
  handleData(url, showLogs, showError);
};
// #endregion

// #region ***  Event Listeners - listenTo___            ***********

const listenToClick = function () {
  const remindertypes = document.querySelectorAll('.js-reminder');
  const remindertime = document.querySelectorAll('.js-time')
  const reminderamount = document.querySelectorAll('.js-amount')
  for (const type of remindertypes) {
    type.addEventListener('click', function () {
      console.info(this);
      const kind = this.getAttribute('data-type');
      console.info(kind);
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
  for(const time of remindertime){
    time.addEventListener('click', function(){
      console.info(this.innerHTML)
      currentValue = this.innerHTML
      var input = document.createElement("input");
      input.type = "number";
      input.value = currentValue;
      input.onblur = function() {
        // Wanneer het invoerveld wordt verlaten, update het getal
        var newValue = parseInt(input.value);
        this.innerHTML = newValue;

        const kind = this.getAttribute('data-type');
        console.info(kind);
        if (kind == 'bulb') {
          
        } else if (kind == 'music') {

        } else if (kind == 'vibrate') {

        }
      };
    
      // Vervang het huidige element door het invoerveld
      this.innerHTML = "";
      this.appendChild(input);
    
      // Plaats de focus op het invoerveld
      input.focus();
    })
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
    htmlBtn.addEventListener('click', function () {
      closePopup();
      window.location = 'index.html';
    });
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
    // socketio.emit('F2B_getweight');
    // socketio.emit('F2B_gettemp');
  });
  getLastLog();
};

const initReadings = function () {
  console.info('init readings');
  getHistory();
};

const initSettings = function () {
  console.info('init settings');
  const htmlSaveS = document.querySelector('.js-savespecifications');
  const htmlSaveR = document.querySelector('.js-savereminders');
  const htmlDone = document.querySelector('.js-done');
  const htmlInfo = document.querySelector('.js-info');
  htmlSaveS.addEventListener('click', function () {
    showPopup(1);
  });
  htmlSaveR.addEventListener('click', function () {
    showPopup(1);
  });
  htmlDone.addEventListener('click', function () {
    closePopup(1);
  });
  htmlInfo.addEventListener('click', function () {
    showPopup(2);
  });
  getReminders();
  listenToClick();
};

document.addEventListener('DOMContentLoaded', init);
// #endregion
