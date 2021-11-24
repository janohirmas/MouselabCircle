
// Constants and Variables
var startTime;

// Initialize 
window.addEventListener('DOMContentLoaded', () => {
    startTime = new Date(); // Ensure that timer starts when the page is loaded
});


// Functions
function endPage() {
    endTime = new Date();
    // Load Inputs
    let startTS = document.getElementById('sStart');
    let endTS = document.getElementById('sEnd');
    let dRT = document.getElementById('dRT');
    // If not null, write value
    if (startTS!=null)  {startTS.value = createTimeStamp(startTime)};
    if (endTS!=null)    {endTS.value = createTimeStamp(endTime)};
    if (dRT!=null)      {dRT.value = endTime - startTime};
    // Next Page
    document.getElementById('next-btn').click();       
}
function createTimeStamp(date) {
    iHH     = date.getHours();
    iMM     = date.getMinutes();
    iSS     = date.getSeconds();
    iMmm    = date.getMilliseconds();
    if (iMmm<100) {
        sMmm = `0${iMmm}`;
    } else {
        sMmm = `${iMmm}`;
    }
    return `${iHH}:${iMM}:${iSS}:${sMmm}`;
}