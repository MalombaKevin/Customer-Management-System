function tarehe(){
    todayDate= new Date()
    console.log(todayDate)
    leo=todayDate.toDateString()

    document.getElementById('tarehe').innerHTML = leo
}

  