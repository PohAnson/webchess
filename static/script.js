$(function(){ 
// For loop to create all of your confetti items on load
for (var i = 0; i < 30; i++){
  create(i);
}

function create(i){
  // Create confetti particles
  
  //Generates random number, then multiples by 15
  var width = Math.random() * 15;
  
  //Takes generated width, multiplies by .4 for height
  var height = width * 0.4;
  
  //generates a random number to decide whether the confetti is blue, yellow, or red
  var colorIdx = Math.ceil(Math.random() * 3);
  var color = "red";
  
  // Select random color for particle
  switch(colorIdx){
    case 1:
      color = "yellow";
      break;
    case 2:
      color = "blue";
      break;
    case 3:
        color = "green";
   //add more colors here by doing this:
   /*
   case 3:
   color = "colorname";
   break
   */
   // Make sure to style the class of your color name to set the background color
    default:
      color = "red";
  }
  
  // Create DOM object for particle
  // and add particle to wrapper 
  $('<div class="confetti-'+i+' '+color+'"></div>').css({
    "width" : width+"px",
    "height" : height+"px",
    "top" : -Math.random()*20+"%",
    "left" : Math.random()*100+"%",
    "opacity" : Math.random()+0.5,
    "transform" : "rotate("+Math.random()*360+"deg)"
  }).appendTo('.wrapper');  
  
  // Make confetti drop
  drop(i);
}

function drop(x) {
  $('.confetti-'+x).animate({
    top: "100%",
    left: "+="+Math.random()*15+"%"
  }, Math.random()*2000 + 2000, function() {
    reset(x);
  });
}
    

function reset(x) {
  // Reset opacity
  $('.confetti-'+x).css('opacity','1');
  
  $('.confetti-'+x).animate({
    "top" : -Math.random()*20+"%",
    "left" : "-="+Math.random()*15+"%"
  }, 0, function() {
    drop(x);             
  });
}

});