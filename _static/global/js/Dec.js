const iMax      = js_vars.iMax;
var iValue      = Math.round((1+iMax)/2);

window.addEventListener('DOMContentLoaded', () => {
    activateButton(iValue);
});

document.addEventListener('keypress', (event)=>{
    switch (event.key) {
        case "a":
        case "A" :
            iValue = Math.max(1,iValue-1);
            activateButton(iValue);
            break;
        case "d" :
        case "D" :
            iValue = Math.min(iMax,iValue+1);
            activateButton(iValue);
            break;
        // case "Enter":
        //     submitAnswer(iValue);
    }

});

function activateButton(iVal){
    deactivateAll();
    let btn = document.getElementById(`rating-${iVal}`);
    btn.classList.add('active-btn');
};

function deactivateAll() {
    vBtns = document.getElementsByClassName('rating-btn');
    for (let i=0;i<vBtns.length;i++){
        vBtns[i].classList.remove('active-btn');
    }
};

function submitAnswer(sValue){
    let endTime = new Date();
    let dif = endTime - startTime;
    document.getElementById('iDec').value = sValue; 
    endPage();
};

