// onload function
// the function randomizes the content of the options (1-4) for each of the critera (3 in total)
function orderCriteria (){
    //randomize four numbers (1,2,3,4) to the <option> elements (for each criterion)
    var firstNum, secondNum, thirdNum, forthNum;
    continents = ["Africa", "America", "Asia", "Europe"]; //array of options for each criterion
    vacation_types = ["Backpacking", "Leisure", "Package tour", "Cultural"];
    sleepings = ["Hotel", "Rental Apartment", "Guesthouse", "Cabin"];
    // for loop - three times, for each criterion
    for (var i = 0; i < 3; i++) {
        //randomize 4 numbers (the options to the criteria) - 1-4
        firstNum = Math.floor(Math.random()*4)+1;
        do{
            secondNum = Math.floor(Math.random()*4)+1;
        } while (secondNum == firstNum);
        do{
            thirdNum = Math.floor(Math.random()*4)+1;
        } while (thirdNum == firstNum || thirdNum == secondNum);
        do{
            forthNum = Math.floor(Math.random()*4)+1;
        } while (forthNum == firstNum || forthNum == secondNum || forthNum == thirdNum);
        // get the option according to the numbers
        var arr = continents;
        if (i == 1) //change the array options according to the index in the loop (0=continents, 1=vacation types, 2=sleepings)
            arr = vacation_types;
        else if (i == 2)
            arr = sleepings;
        var firstElement = randNumToCriterion(firstNum, arr);
        var secondElement = randNumToCriterion(secondNum, arr);
        var thirdElement = randNumToCriterion(thirdNum, arr);
        var forthElement = randNumToCriterion(forthNum, arr);

        //change the elements (<option>) content according to the randomazation.
        if (i == 0){ //for the first criterion - continent
            document.getElementsByTagName("option")[1].innerHTML = firstElement;
            document.getElementsByTagName("option")[2].innerHTML = secondElement;
            document.getElementsByTagName("option")[3].innerHTML = thirdElement;
            document.getElementsByTagName("option")[4].innerHTML = forthElement;
        }
        if (i == 1){ //for the second criterion - vacation type
            document.getElementsByTagName("option")[6].innerHTML = firstElement;
            document.getElementsByTagName("option")[7].innerHTML = secondElement;
            document.getElementsByTagName("option")[8].innerHTML = thirdElement;
            document.getElementsByTagName("option")[9].innerHTML = forthElement;
        }
        if (i == 2){ //for the third criterion - sleeping arrangement
            document.getElementsByTagName("option")[11].innerHTML = firstElement;
            document.getElementsByTagName("option")[12].innerHTML = secondElement;
            document.getElementsByTagName("option")[13].innerHTML = thirdElement;
            document.getElementsByTagName("option")[14].innerHTML = forthElement;
        }
    }
}

//return the correct criterion to the given number according to the arr
function randNumToCriterion (num, arr){
    if (num == 1)
        return arr[0];
    if (num == 2)
        return arr[1];
    if (num == 3)
        return arr[2];
    return arr[3];
}

var selected1, selected2, selected3; //the selected options by the user

//the function extracts the user choises according to his preferences
function chosenRank(){
    var x = document.getElementById("slct1");
    selected1 = selectedOption(x);
    var y = document.getElementById("slct2");
    selected2 = selectedOption(y);
    var z = document.getElementById("slct3");
    selected3 = selectedOption(z);
    if (selected1 == "" || selected2 == "" || selected3 == "")
        alert("Please select an option in each group.");
    else{ //success - user chose 3 options
        //first the page will show the loading circle and his <p> tag and will hide everything
        //then it will wait 3 seconds in the waitFunction and then it will redirect with the loadNextPage function.
        changeToLoadingCircle(); 
    }
}

//recieve a value which indicated which of the selects from 1-3 is know being tested, and return the chosen option by the user
//return "" if the user didn't choose an option
function selectedOption (value){
    var selectedValue = value.options[value.selectedIndex].innerHTML;
    //alert(selectedValue);    //this is the chosen option by the user
    if (selectedValue == "Continent" || selectedValue == "Vacation Type" || selectedValue == "Sleeping Arrangement")
        return ""; //false - the user did not choose an option!
    return selectedValue;
}



//////////// LOADING NEXT PAGE ////////////

// the function "cleans" (displany=none) all elemnts in page
// the function reveals the loading-circle element and redirects the user to the next page
function changeToLoadingCircle(){
    document.getElementById("loading_circle").style.display = 'block';
    document.getElementsByTagName('button')[0].style.display = 'none';
    var p_tags = document.getElementsByTagName('p');
    var select_classes = document.getElementsByClassName('select');
    for (var i = 0; i < p_tags.length; i++) {
        p_tags[i].style.display = 'none';;
    }
    for (var i = 0; i < select_classes.length; i++) {
        select_classes[i].style.display = 'none';;
    }
    document.getElementById("loading_p").style.display = 'block';
    waitFunction(3000);
}

function waitFunction(timeToWait) {
    setTimeout(function(){ 
        loadNextPage();
     }, timeToWait);  //timeToWait in miliseconds! 3000 is 3 seconds
}

function loadNextPage(){
    //alert("first: "+selected1+", second: "+selected2+", third: "+selected3);   //the choices of the user!
    connectJStoFlask(selected1,selected2,selected3);
    nextPage(); //moves to the next page
}

function nextPage(){
    var a = document.getElementById('next');
    a.href = "/choosing";
    document.getElementById('next').click(); //clicking again on the "next page" button in order to load next page
}