console.log("Script Running...")
document.querySelector('.close').style.display = 'none';
document.querySelector('.menubar').addEventListener("click",()=>{
    document.querySelector('.headerbar').classList.toggle('headerbargo');
    if(document.querySelector('.headerbar').classList.contains('headerbargo')){
        document.querySelector('.open').style.display = 'inline'
        document.querySelector('.close').style.display = 'none'
    }
    else{
        document.querySelector('.open').style.display = 'none'
        setTimeout(() => {
            document.querySelector('.close').style.display = 'inline'
        },300);
    }
})
document.getElementById("a-close").onclick = function() {myFunction()};
function myFunction() {
    const container = document.getElementById('alert');
    // container.classList.remove("alert")
    container.className = '';
    container.replaceChildren(); 

}

