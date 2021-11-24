const dR1       = 0.4;
    

window.addEventListener('DOMContentLoaded', () => {
    let dRadius1 = dR1*Math.min(window.innerHeight,window.innerWidth);
    positionBtns('attr-circ', dRadius1);    
});

window.addEventListener('resize', ()=>{
    let dRadius1 = dR1*Math.min(window.innerHeight,window.innerWidth);
    positionBtns('attr-circ', dRadius1);
});

document.addEventListener('keypress', (event)=>{
    switch (event.key) {
        case "Enter":
            endPage();
    }
});


function positionBtns(className,dRadius){
    
    let dXCenter = window.innerWidth / 2;
    let dYCenter = window.innerHeight / 2;
    let btns = document.getElementsByClassName(className);
    let iBtns = btns.length;
    let dAngleStep = 2*Math.PI/iBtns;
    for (let i=0;i<iBtns;i++) {
        let dRadian = -0.5*Math.PI+dAngleStep*i;
        // console.log(dRadian);
        let dX = Math.cos(dRadian)*dRadius + dXCenter; 
        let dY = Math.sin(dRadian)*dRadius + dYCenter; 
        d = btns[i];
        d.style.left = dX+'px';
        d.style.top = dY+'px';
        d.style.visibility = 'visible';
    };
};


// function drawLines(dRadius,iAttr) {
//     let canvas         = document.getElementById('screen-canvas');
//     canvas.style.width = window.innerWidth+'px';
//     canvas.style.height = window.innerHeight+'px';
//     const ctx = canvas.getContext('2d');
//     ctx.lineWidth   = 10;
//     ctx.strokeStyle = '#000';
//     let dXCenter    = window.innerWidth / 2;
//     let dYCenter    = window.innerHeight / 2;
//     let dAngleStep  = 2*Math.PI/iAttr;
    
//     for (let i=0;i<iAttr;i++) {
//         let dRadian = -0.5*Math.PI+dAngleStep*i;
//         let dX = Math.floor(Math.cos(dRadian)*dRadius + dXCenter); 
//         let dY = Math.floor(Math.sin(dRadian)*dRadius + dYCenter); 
//         console.log([dX,dY])
//         ctx.beginPath();
//         ctx.moveTo(dX,dY);
//         ctx.lineTo(dXCenter,dYCenter);
//         ctx.stroke();
//     };
// }