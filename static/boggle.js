"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");
const $submitBtn = $("#submit-btn");


let gameId;


/** Start */

async function start() {
  let response = await axios.get("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();

  // loop over board and create the DOM tr/td structure
  for(let row of board){
    let $tr = $("<tr>");
    for(let char of row){
      $tr.append(`<td>${char}</td>`)
    }
    $table.append($tr);
  }
}

async function handleSubmit(evt){
  evt.preventDefault();

  let word = $wordInput.val().toUpperCase()

  if(!word) return;

  await checkIfWordIsValid(word)
}

async function checkIfWordIsValid(word){

  let response = await axios.post("/api/score-word", {
    'word' : word,
    'gameId': gameId
  })

  if(response.data.result === "not-word"){
    showMessage('Oops, not a word!', "err")
  } else if(response.data.result === "not-word"){
    showMessage('Not a legal play!', "err")
  } else {
    $message.append(`<p>${word}</p>`)
    showMessage(`Added: ${word}', "ok"`)
    showWord(word);    
  }
}

/** Show status message. */

function showMessage(msg, cssClass) {
  $message
    .text(msg)
    .removeClass()
    .addClass(`msg ${cssClass}`);
}

/** Add word to played word list in DOM */

function showWord(word) {
  $($playedWords).append($("<li>", { text: word }));
}

$form.on('submit', handleSubmit);

start();