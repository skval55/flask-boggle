"use strict";
console.log("sup");
const timerDisplay = document.getElementById("timer-display");
const startButton = document.getElementById("start");

class Game {
  constructor() {
    this.score = 0;
    this.words = [];
    this.duration = 60;
    this.game = false;
  }

  changeInput(resp, word) {
    // changes place holder that tells player if word or not
    $("input").val("");
    if (boggle.words.includes(word)) {
      $("input").attr("placeholder", "already found word");
      return;
    }
    if (resp === "not-word") {
      $("input").attr("placeholder", "Not a word!!");
    }
    if (resp === "not-on-board") {
      $("input").attr("placeholder", "Not on board!!");
    }
    if (resp === "ok") {
      $("input").attr("placeholder", "Nice Work!");
      this.scoreCounter(word);
      boggle.words.push(word);
    }
  }

  async handleSubmitClick(e) {
    // handles submit button when active
    e.preventDefault();
    if (boggle.game === false) {
      return;
    }
    const wrd = $("input").val();
    if (!wrd) {
      return;
    }
    const resp = await axios.get("/check-word", { params: { word: wrd } });
    const game = new Game(); // create an instance of Game
    game.changeInput(resp.data.result, wrd);
  }

  scoreCounter(word) {
    // counts score of words
    const points = word.length;
    boggle.score = boggle.score + points;
    $("#score").text(`Score: ${boggle.score}`);
  }

  //   timer for game set to 60 seconds
  timer() {
    let timeLeft = boggle.duration;
    let timer = setInterval(() => {
      // update the timer display
      timerDisplay.textContent = `${timeLeft} seconds`;

      // check if the timer has reached 0
      if (timeLeft === 0) {
        // stop the timer
        clearInterval(timer);
        boggle.endGame();
      }
      // decrement the time left
      timeLeft--;
    }, 1000);
  }

  //ends game and posts score
  endGame() {
    boggle.postScore(boggle.score);
    boggle.game = false;
    timerDisplay.textContent = `Time up!`;
  }

  //   starts game and timer
  startGame() {
    boggle.game = true;
    $(".game-card").removeClass("hidden");
    boggle.score = 0;
    $("#start").text("Reset");
    $("#start").click(boggle.resetGame);
    $("#your-score").text(``);
    boggle.timer();
  }

  resetGame() {
    location.replace("/");
  }

  async postScore(score) {
    let resp = await axios.post("/get-score", { score: score });
    $("#high-score").text(`High Score: ${resp.data.score}`);
    $("#your-score").text(`${resp.data.new_highscore}`);
    $("#times-played").text(`Times Played ${resp.data.times}`);
  }
}
let boggle = new Game();
startButton.addEventListener("click", boggle.startGame);

$("#submit").click(boggle.handleSubmitClick);
