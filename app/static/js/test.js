
const modesDropDown = document.getElementById('modes-select')

const serverAddr = '0.0.0.0:5000'

function init() {
    fetch(`http://${serverAddr}/get_modes`)
        .then(response => response.json())
        .then(json => setModesList(json));
}

function setModesList(modesDict) {
    console.log(modesDict);
    for (let mode in modesDict) {
        let option = document.createElement("option");
        option.value = mode;
        option.text = modesDict[mode]['name_ru'];
        modesDropDown.appendChild(option);
    }
}

function modesListChange() {
    
}