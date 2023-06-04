const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);



// #region ***  DOM references                           ***********
// #endregion

// #region ***  Callback-Visualisation - show___         ***********

const showError = function (error) {
  console.error(error);
}

const showHistory = function(jsonObject){
  console.info(jsonObject)
  const htmlTable = document.querySelector('.js-historyTable')
  htmlTable.innerHTML = `<tr>
      <th>ID</th>
      <th>deviceID</th>
      <th>date</th>
      <th>value</th>
    </tr>
  <tbody>`
  for(const record of jsonObject){

  }
  htmlTable.innerHTML += `</tbody></table>`
}
// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********
// #endregion

// #region ***  Data Access - get___                     ***********

const getHistory = function(){
  const userid = localStorage.getItem('userid')
  const url = `http://192.168.168.169:5000/api/v1/waterreminder/user/2/`
  handleData(url, showHistory, showError)
}
// #endregion

// #region ***  Event Listeners - listenTo___            ***********
// #endregion

// #region ***  Init / DOMContentLoaded                  ***********

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
  const htmlRfid =document.querySelector('.js-rfid')
  socketio.on('connect', function () {
    console.info('succesfully connected to socket');
    socketio.emit('F2B_readrfid');
  });
  socketio.on('B2F_showid', function (id) {
    console.info(id);
    htmlRfid.innerHTML += id
    localStorage.setItem('userid', id)
    window.location = 'index.html'
  });
};

const initIndex = function () {
  console.info('init index');
};

const initOverview = function () {
  console.info('init overview');
  htmlTemp = document.querySelector('.js-temp')
  socketio.on('connect', function () {
    console.info('succesfully connected to socket');
    socketio.emit('F2B_gettemp');
  });
  socketio.on('B2F_showtemp', function (temp) {
    console.info(temp.value);
    htmlTemp.innerHTML += temp.value;
  });
};

const initReadings = function () {
  console.info('init readings');
  getHistory()
};

const initSettings = function () {
  console.info('init settings');
};

document.addEventListener('DOMContentLoaded', init);
// #endregion
