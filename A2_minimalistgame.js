//Creative Coding 2021
//Exercise 2: Minmalist Game Design
//Modify this sample code to create a game with at least TWO new features

/*instructions
check out the reference on libraries: https://p5js.org/libraries/

- add the library p5.play.js to your sketch files
- https://creative-coding.decontextualize.com/making-games-with-p5-play
- include this new .js file to the <body> of index.html:
 <body>
    <script src="sketch.js"></script>
    <script src="p5.play.js"></script>
  </body>
*/

p5.disableFriendlyErrors = true;
var score = 0;
//--------------------------------------------------------------------------
function setup() {
  height = 400, width = 400, limit = 10, lower = 10, upper = 50, ccolor = 255;
  
  createCanvas(height, width);
  for (let i = 0; i < limit; i++) {
    var spr = createSprite(
      random(width), random(height),
      random(lower, upper), random(lower, upper));
    spr.shapeColor = random(ccolor);
    spr.onMouseOver = removeAndScore;
  }
}
//--------------------------------------------------------------------------
function draw() {
  bcolor = 50, dfill = 255, tsize = 72, slimit = 10;
  
  background(bcolor);
  drawSprites();
  fill(dfill);
  noStroke();
  textSize(tsize);
  textAlign(CENTER, CENTER);
  if (score < slimit) {
    text(score, width/2, height/2);
  }
  else {
    text("you win!", width/2, height/2);
  }
}
//--------------------------------------------------------------------------
function removeAndScore() {
  score += 1;
  this.remove();
}
//--------------------------------------------------------------------------
