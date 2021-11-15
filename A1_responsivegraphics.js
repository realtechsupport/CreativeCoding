//Assignment 1
//Responsive Graphics
//Change the display in response to the information in an audio file
//Add the audio asset to the project files ( > menu on left)
//September 2021
//-----------------------------------------------------------------------------
var circleY = [];
var mheight = 300;
var mwidth = 300;
var song, analyzer;
//-----------------------------------------------------------------------------
function preload() {
 song = loadSound('yourchoice.mp3')
}
//-----------------------------------------------------------------------------
function setup() {
  createCanvas(mheight, mwidth);
  for (let i = 0; i < 25; i++) {
    circleY[i] = random(mheight);
  }
 //-----------------------------------------------------------------------------
  song.loop();
 // create a new Amplitude analyzer
 analyzer = new p5.Amplitude();
 // Patch the input to an volume analyzer
 analyzer.setInput(song);
}
//-----------------------------------------------------------------------------
function draw() {
  background(50);
   // Get the average (root mean square) amplitude... use this as a dynamic input.
   var rms = analyzer.getLevel();
  print(rms)
  
  for (let i = 0; i < circleY.length; i++) {
    var circleX = mwidth * i / circleY.length;
    circle(circleX, circleY[i], 25);
    circleY[i]++;
    
    if (circleY[i] > mheight) {
      circleY[i] = 0;
    }   //end if
  }     //end for
}       //end draw
//-----------------------------------------------------------------------------

