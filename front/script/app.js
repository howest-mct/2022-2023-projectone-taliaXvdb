const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);
let percentageProgress = 0
let theGoal = 0

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
      <th class="c-reminder_title">type</th>
      <th class="c-reminder_title">time</th>
      <th class="c-reminder_title">amount</th>
    </tr></thead>
  <tbody>`;
  for (const reminder of jsonObject.reminders) {
    if (reminder.type == 1) {
      htmlString += `<tr>
      <td class="js-reminder c-reminder__type" data-type="${reminder.type}" data-id="${reminder.reminderID}">
      <img src="img/bulb-outline.svg" class="c-reminder__img" data-type="${reminder.type}"></td>
      <td data-type="bulb"><input type="number" class="c-reminder__input js-time" value=${reminder.time}></input></td>
      <td data-type="bulb"><input type="number" class="c-reminder__input js-amount" value=${reminder.amount}></input></td>
      </tr>`;
    } else if (reminder.type == 2) {
      htmlString += `<tr>
      <td class="js-reminder c-reminder__type" data-type="${reminder.type}" data-id="${reminder.reminderID}">
      <img src="img/music-outline.svg" class="c-reminder__img" data-type="${reminder.type}"></td>
      <td data-type="music"><input type="number" class="c-reminder__input js-time" value=${reminder.time}></input></td>
      <td data-type="music"><input type="number" class="c-reminder__input js-amount" value=${reminder.amount}></input></td>
      </tr>`;
    } else if (reminder.type == 3) {
      htmlString += `<tr>
      <td class="js-reminder c-reminder__type" data-type="${reminder.type}" data-id="${reminder.reminderID}">
      <img src="img/phone-call-outline.svg" class="c-reminder__img" data-type="${reminder.type}"></td>
      <td data-type="vibrate"><input type="number" class="c-reminder__input js-time" value=${reminder.time}></input></td>
      <td data-type="vibrate"><input type="number" class="c-reminder__input js-amount" value=${reminder.amount}></input></td>
      </tr>`;
    }
  }
  htmlString += `</tbody></table>`;
  htmlReminders.innerHTML = htmlString;
  listenToClick();
};

const showDoubleLineGraph = function (
  title,
  labels,
  axistitle,
  dataTopline,
  dataBottomline,
  dateData
) {
  var options = {
    series: [
      {
        name: labels[0],
        data: dataTopline,
      },
      {
        name: labels[1],
        data: dataBottomline,
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
    colors: ['#545454', '#74C0FC'],
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
      categories: dateData,
      title: {
        text: axistitle[0],
      },
    },
    yaxis: {
      title: {
        text: axistitle[1],
      },
      min: 0,
      max: 3000,
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

const showSingleLineGraph = function(title, label, axistitle, dataLine, dateData, max, number) {
  var options = {
    series: [{
      name: label,
      data: dataLine
    }],
    chart: {
      height: 350,
      type: 'area',
      zoom: {
        enabled: false
      }
    },
    dataLabels: {
      enabled: false
    },
    stroke: {
      curve: 'straight'
    },
    title: {
      text: title,
      align: 'left'
    },
    grid: {
      row: {
        colors: ['#f3f3f3', 'transparent'],
        opacity: 0.5
      }
    },
    xaxis: {
      categories: dateData,
      title: {
        text: axistitle[0],
      },
    },
    yaxis: {
      title: {
        text: axistitle[1],
      },
      min: 0,
      max: max,
    },
    xaxis: {
      categories: dateData,
      tickAmount: 8,
      
    }
  };
  console.info(number)
  if (number == 1){
    var chart = new ApexCharts(document.querySelector(".js-chart1"), options);
  }
  else if(number == 2){
    var chart = new ApexCharts(document.querySelector(".js-chart2"), options);
  }
  chart.render();
}


const showLastLog = function (jsonObject) {
  const htmlStreak = document.querySelector('.js-streak')
  let streak = 0
  const title = 'Did I reach my goal?';
  const labels = ['goal', 'what i drank'];
  const axistitles = ['Date', 'Amount(ml)'];
  let goalData = [];
  let amountDrank = [];
  let dates = [];
  for (const logged of jsonObject.data) {
    goalData.push(logged['daily goal']);
    amountDrank.push(logged['total weight water']);
    dates.push(logged['date']);
    if (logged['total weight water'] >= logged['daily goal']){
      streak += 1
    }
  }
  htmlStreak.innerHTML = streak
  console.info(goalData);
  console.info(amountDrank);
  console.info(dates);
  showDoubleLineGraph(title, labels, axistitles, goalData, amountDrank, dates);
};

const showTemp = function(jsonObject){
  console.info(jsonObject)
  const tempTitle = `Today's evolution of temperature`
  const tempLabel = ['Temperature']
  const tempAxis = ['Time', 'Temperature(°C)']
  let tempData = []
  let tempTime = []
  for(const temp of jsonObject.data){
    tempData.push(temp.value)
    tempTime.push(temp.Time)
  }
  showSingleLineGraph(tempTitle, tempLabel, tempAxis, tempData, tempTime, 40, 1)
}

const showWeight = function(jsonObject){
  console.info(jsonObject)
  const weightTitle = `Today's evolution of weight`
  const weightLabel = ['Weight']
  const weightAxis = ['Time', 'Weight(g)']
  let weightData = []
  let weightTime = []
  for(const weight of jsonObject.data){
    if (weight.value < 0) {
      weight.value = 0
    }
    else if(weight.value > 3000){
      weight.value = 3000
    }
    weightData.push(weight.value)
    for(const weightvalue of weightData){
      if(weightvalue == 0){
        weightData.pop(weightvalue)
      }
    }
    weightTime.push(weight.Time)
  }
  console.info(weightData)
  console.info(weightTime)
  showSingleLineGraph(weightTitle, weightLabel, weightAxis, weightData, weightTime, 3500, 2)
}

const showTheProgress = function(jsonObject){
  console.info(jsonObject.progress[0]['total'])
  val = jsonObject.progress[0]['total']/theGoal
  percentageToCircle(val)
}

const showUserInfo = function(jsonObject){
  console.info(jsonObject.user)
  const htmlName = document.querySelector('.js-name')
  const htmlTheGoal = document.querySelector('.js-thegoal')
  htmlName.value = jsonObject.user.name
  htmlTheGoal.value = jsonObject.user.goal
}
// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********
const formatTime = function(seconds) {
  if(seconds < 0){
    seconds = 0
  }
  var minutes = Math.floor(seconds / 60);
  var remainingSeconds = Math.floor(seconds % 60);
  if(minutes < 10){
    if(remainingSeconds < 10){
      return '0' + minutes + ":" + '0' + remainingSeconds;
    }
    return '0' + minutes + ":" + remainingSeconds;
  }
  else if(remainingSeconds < 10){
    return minutes + ":" + '0' + remainingSeconds;
  }
  else {
    return minutes + ":" + remainingSeconds;
  }
}

const percentageToCircle = function(percentage) {
  console.info(percentage)
  if(percentage >= 1){
    showProgress(1, '#4DABF7');
  }
  else {
    showProgress(percentage, '#4DABF7');
  }
}
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

const getReminders = function () {
  let userid = localStorage.getItem('userid');
  const url = `http://${lanIP}/api/v1/waterreminder/user/${userid}/reminders/`;
  handleData(url, showReminders, showError);
};

const getTemp = function () {
  console.info('get temp')
  let userid = localStorage.getItem('userid');
  const url = `http://${lanIP}/api/v1/waterreminder/user/${userid}/temperature/`;
  handleData(url, showTemp, showError);
};

const getWeight = function () {
  console.info('getw weight')
  let userid = localStorage.getItem('userid');
  const url = `http://${lanIP}/api/v1/waterreminder/user/${userid}/weight/`;
  handleData(url, showWeight, showError);
};

const getLastLog = function(){
  let userid = localStorage.getItem('userid');
  const url = `http://${lanIP}/api/v1/waterreminder/user/${userid}/logging/last/`
  handleData(url, showLastLog, showError)
}

const getProgress = function(){
  let userid = localStorage.getItem('userid');
  const url = `http://${lanIP}/api/v1/waterreminder/user/${userid}/logging/`
  handleData(url, showTheProgress, showError)
}

const getUser = function(){
  let userid = localStorage.getItem('userid');
  const url = `http://${lanIP}/api/v1/waterreminder/user/${userid}/`
  handleData(url, showUserInfo, showError)
}
// #endregion

// #region ***  Event Listeners - listenTo___            ***********

const listenToClick = function () {
  const remindertypes = document.querySelectorAll('.js-reminder');
  const remindertime = document.querySelectorAll('.js-time');
  const reminderamount = document.querySelectorAll('.js-amount');
  const savebtn = document.querySelector('.js-savereminders')
  for (const type of remindertypes) {
    type.addEventListener('click', function () {
      console.info(this);
      const kind = this.getAttribute('data-type');
      console.info(kind);
      if (kind == 1) {
        console.info('bulb clicked');
        socketio.emit('F2B_lighton');
      } else if (kind == 2) {
        console.info('sound clicked');
        socketio.emit('F2B_playmusic');
      } else if (kind == 3) {
        console.info('vibrate clicked');
        socketio.emit('F2B_vibrate');
      }
    });
  }
  savebtn.addEventListener('click', function(){
    for(let i = 0; i < 3; i ++){
      console.info(remindertime[i].value)
      console.info(reminderamount[i].value)
      console.info(remindertypes[i].getAttribute('data-id'))
      console.info(remindertypes[i].getAttribute('data-type'))
      const timeval = remindertime[i].value
      const amountval = reminderamount[i].value
      const reminderid = remindertypes[i].getAttribute('data-id')
      const typeid = remindertypes[i].getAttribute('data-type')
      const userid = localStorage.getItem('userid')
      socketio.emit('F2B_updatereminder', [reminderid, userid, typeid, timeval, amountval])
    }
  })
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
  const empty = ['', null, 0]
  if(empty.includes(localStorage.getItem('userid'))){
    window.location = 'login.html'
  }
  iduser = localStorage.getItem('userid')
  htmlTemp = document.querySelector('.js-temp');
  htmlGoal = document.querySelector('.js-goal');
  htmlTime = document.querySelector('.js-time');
  socketio.on('connect', function () {
    console.info('succesfully connected to socket');
    socketio.emit('F2B_getgoal');
    socketio.emit('F2B_gettemp');
  });
  socketio.on('B2F_placedrink', function(interval){
    console.info(interval)
    console.info('drink')
    showPopup(1)
  })
  socketio.on('B2F_closepopup', function(){
    closePopup(1)
  })
  socketio.on('B2F_showtemp', function (temp) {
    // console.info(temp);
    htmlTemp.innerHTML = temp;
  });
  socketio.on('B2F_showgoal', function (goal) {
    console.info(goal.goal);
    theGoal = goal.goal
    htmlGoal.innerHTML = goal.goal;
    getProgress(iduser)
  });
  socketio.on('B2F_showremaining', function(time_left){
    // console.info(time_left)
    htmlTime.innerHTML = formatTime(time_left)
  })
  socketio.on('B2F_showprogress', function(progress){
    console.info(progress)
    percentageProgress = progress/theGoal
    console.info(percentageProgress);
    percentageToCircle(percentageProgress);
  })

};

const initOverview = function () {
  console.info('init overview');
  htmlTemp = document.querySelector('.js-temp');
  htmlWeight = document.querySelector('.js-weight');
  socketio.on('connect', function () {
    console.info('succesfully connected to socket');
  });
  getLastLog();
};

const initReadings = function () {
  console.info('init readings');
  getTemp()
  getWeight()
};

const initSettings = function () {
  console.info('init settings');
  const htmlSaveS = document.querySelector('.js-savespecifications');
  const htmlSaveR = document.querySelector('.js-savereminders');
  const htmlDone = document.querySelector('.js-done');
  const htmlInfo = document.querySelector('.js-info');
  getUser()
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
