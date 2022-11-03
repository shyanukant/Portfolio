// console.log("Script Running...")
const toggle = document.getElementById('toggle');
const navbar = document.getElementById('headerbar')
toggle.onclick = function(){
    toggle.classList.toggle('active')
    navbar.classList.toggle('active')
}
// document.querySelector('.close').style.display = 'visible';
// document.querySelector('.menubar ').addEventListener("click",()=>{
//     document.querySelector('.headerbar').classList.toggle('headerbargo');
//     toggle.classList.toggle('active')
//     if(document.querySelector('.headerbar').classList.contains('headerbargo')){
//         document.querySelector('.open').style.display = 'inline'
//         document.querySelector('.close').style.display = 'none'
//         toggle.onclick = function(){
//             toggle.classList.toggle('active')
//         } 
//     }
//     else{
//         document.querySelector('.open').style.display = 'none'
//         setTimeout(() => {
//             document.querySelector('.close').style.display = 'inline'
//         },300);
//     }
    
// })
// const slider = document.getElementsByClassName('headerbargo');
// document.onclick = function(clickEvent){
//     if(clickEvent.target.className != 'menubar' && clickEvent.target.className != 'headerbar'){
//         slider.classList.remove('headerbar');
//     }
// }

document.getElementById("a-close").onclick = function() {myFunction()};
function myFunction() {
    const container = document.getElementById('alert');
    // container.classList.remove("alert")
    container.className = '';
    container.replaceChildren(); 

}

