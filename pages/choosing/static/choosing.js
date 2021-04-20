var num_of_clicks = 0; //the number of times the user clicks on the recommendation button


function userChoice(id) {
    //alert(num_of_clicks); //the number of clicks on the recommendation window
    //id = the specific vacation the user chose (vac_id).
    // if the user chose one of the recommender system's offers: id=-1.
    //var x = document.getElementById(id).innerHTML; -> this is the chosen vacation
    var double_check = confirm("Is this the vacation you want to choose?");
    if (double_check) { //yes - next page
        var choseRec = false; //didn't choose recommendation
        if (id == -1)
            choseRec = true; //chose ont of the recommendations
        connectJStoFlask(choseRec,id,num_of_clicks); //id=-1 if it's one of the recomm
        window.location.href = "/questions_1";
    }
    else { //nothing happens - the user regrets his decision
    }
}

//scrolls the page up
function scrollUp (){
    window.scroll({
        top: 0, 
        left: 0, 
        behavior: 'smooth'
      });
}