function tarehe(){
    todayDate= new Date()
    console.log(todayDate)
    leo=todayDate.toDateString()

    hourToday = todayDate.getHours()
    minutesToday = todayDate.getMinutes()
    secondsToday = todayDate.getSeconds()

    setTimeout(tarehe, 1000)

    document.getElementById('tarehe').innerHTML = leo

    document.getElementById('saa').innerHTML = hourToday + " : " + minutesToday + " : " + secondsToday
}


function darkmode(){
    var page =document.body 
 
     page.classList.toggle('darkmode')
 
    
 }

  