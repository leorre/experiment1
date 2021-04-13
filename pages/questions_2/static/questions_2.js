// //combines the user answers - those are the chosen answers of the user
// function checkForm (){
//     //table:
//     var q1=which_was_chosen("q1");
//     var q2=which_was_chosen("q2");
//     var q3=which_was_chosen("q3");
//     var q4=which_was_chosen("q4");
//     var q5=which_was_chosen("q5");
//     if (q1 == "" || q2 == "" || q3 == "" || q4 == "" || q5 == ""){ //the user didn't answer at least one of the questions in the table
//         return;
//     }
//     //alert("q1: "+q1+", q2: "+q2); ///////////////////////////// the answers of the user
//     //connectJStoFlask(q1,q2,q3,q4,q5);
//     nextPage(); //moves to the next page
// }
//
// function nextPage(){
//     var a = document.getElementById('next');
//     a.href = "/end";
// }
//
//
// //returns the chosen radio input according to it's name (gender/experience/device...)
// function which_was_chosen (name){
//     var all = document.getElementsByName(name);
//     var chosen = "";
//     var i;
//     for (i = 0; i < all.length; i++) {
//       if (all[i].checked) {
//         chosen=all[i].value;
//       }
//     }
//     return chosen;
// }

