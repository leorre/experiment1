//combines the user answers - those are the chosen answers of the user
function checkForm (){
    if(checkAge("age")==false){ //the user didn't write an age
        return;
    }

    //age, gender, experience, device
    var age=document.getElementById("age").value;
    var gender=which_was_chosen("gender"); //takes the "value"
    var experience=which_was_chosen("experience");
    var device=which_was_chosen("device");
    //alert("age: "+age+", gender: "+gender+", experience: "+experience+", device: "+device); ///////////////////////////// the answers of the user
    if (gender!='' && experience!='' && device!='') { //for flask - "required" on radio buttons doesn't work without it
        gender = onlyFirstChar(gender);
        experience = yesNoToBoolean(experience);
        connectJStoFlask(age,gender,experience,device);
        nextPage(); //moves to the next page
    }
}

//changing the value for the database (instead of "yes" -> true).
function yesNoToBoolean(data){
    if (data == 'yes')
        return true;
    return false;
}

//changing the value for the database (instead of "female" -> 'f').
function onlyFirstChar(gender){
    if (gender == 'female')
        return 'f';
    if (gender == 'male')
        return 'm'
    return 'o'; //other
}

function nextPage(){
    var a = document.getElementById('next');
    a.href = "/questions_2";
}

//returns the chosen radio input according to it's name (gender/experience/device...)
function which_was_chosen (name){
    var all = document.getElementsByName(name);
    var chosen = "";
    var i;
    for (i = 0; i < all.length; i++) {
      if (all[i].checked) {
        chosen=all[i].value;
      }
    }
    return chosen;
}


//the function warns the user if the input of the age is invalid (not a number, not between 18-120, starts with 0, empty..)
//also return true if the age is ok, otherwise return false
function checkAge(id){
    var b1=document.getElementById(id).value;
    if (b1=="") //the user didn't enter an age
        return false;
    var b2=onlyNumbers(b1);
    if (b2 == "" || b2[0] == 0 || b2 < 18 || b2 > 120){ //invalid age
        alert("Invalid age");
        document.getElementById(id).value = "";
        return false;
    }
    return true; //valid age
}

//return the num input as a number. if it contains something other than 0-9 digits - it returns ""
function onlyNumbers(num){
    var ans="";
    var i;
    for (i = 0; i < num.length; i++) {
      var digit = num[i];
      if (digit=='0' || digit=='1' || digit=='2' || digit=='3' || digit=='4' || digit=='5' || digit=='6' || digit=='7' || digit=='8' || digit=='9'){
        ans += num[i];
      }
      else
        return "";
    }
    return ans;
  }