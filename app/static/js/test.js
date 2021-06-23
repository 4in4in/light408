var newCold = null;
var newWarm = null;
var newPwm = null;

const inputName = document.getElementById('input-name');
const inputCold = document.getElementById('input-cold');
const inputWarm = document.getElementById('input-warm');
const inputPwm = document.getElementById('input-pwm');

const labelNewCold = document.getElementById('label-new-cold');
const labelNewWarm = document.getElementById('label-new-warm');
const labelNewPwm = document.getElementById('label-new-pwm');

const labelCold = document.getElementById('label-cold');
const labelWarm = document.getElementById('label-warm');
const labelPwm = document.getElementById('label-pwm');

const modesListElement = document.getElementById('modes-element');

const serverAddr = '0.0.0.0:5000'
var modes = null;

function getCold() {
    newCold = inputCold.value;
    labelNewCold.innerHTML = newCold;
}

function getWarm() {
    newWarm = inputWarm.value;
    labelNewWarm.innerHTML = newWarm;
}

function getPwm() {
    newPwm = inputPwm.value;
    labelNewPwm.innerHTML = newPwm;
}

function updateFields() {
    getCold();
    getWarm();
    getPwm();
}

function init() {
    var modes = fetch(`http://${serverAddr}/get_modes`)
        .then(response => response.json())
        .then(json => setModesFromSource(json));
}

function setModesFromSource(data) {
    modes = data;
    console.log(data);
    for (mode in modes) {
        opt = document.createElement('option');
        opt.value = mode;
        opt.innerHTML = modes[mode].name_ru;
        modesListElement.appendChild(opt);
    }
}

function changeMode() {
    const mode = modesListElement.value;
    labelCold.innerHTML = inputCold.value = modes[mode].cold;
    labelWarm.innerHTML = inputWarm.value = modes[mode].warm;
    labelPwm.innerHTML = inputPwm.value = modes[mode].pwm_freq;
    updateFields();
}

function setMode() {
    const mode = modesListElement.value;
    fetch(`http://${serverAddr}/set_mode_bot`, {
         method: 'POST', 
         headers:{ 'Accept':'application/json','Content-Type': 'application/json' },
         body: JSON.stringify({'mode': mode}) })
}

function checkMode() {
    fetch(`http://${serverAddr}/check_mode`, {
         method: 'POST', 
         headers:{ 'Accept':'application/json','Content-Type': 'application/json' },
         body: JSON.stringify({'cold': inputCold.value, 'warm': inputWarm.value, 'pwm': inputPwm.value}) })
}

function createMode() {
    fetch(`http://${serverAddr}1/create_mode`, {
         method: 'POST', 
         headers:{ 'Accept':'application/json','Content-Type': 'application/json' },
         body: JSON.stringify({'name_ru': inputName.value, 'cold': inputCold.value, 'warm': inputWarm.value, 'pwm': inputPwm.value}) })
         .then(()=>{
             modesListElement.innerHTML='';
            init();
            })
}
