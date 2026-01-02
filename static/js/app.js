function createGame(){
  const host=document.getElementById("host").value;
  const opponent=document.getElementById("opponent").value;

  fetch("/create-game",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({host:host,opponent:opponent})
  })
  .then(res=>res.json())
  .then(data=>{
    window.location.href="/game.html?gameId="+data.GameId;
  });
}

function acceptGame(){
  const gameId=document.getElementById("gameId").value;

  fetch("/accept-game",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({gameId:gameId})
  })
  .then(()=>window.location.href="/game.html?gameId="+gameId);
}

function submitChoice(choice){
  const gameId=new URLSearchParams(window.location.search).get("gameId");
  const player=document.getElementById("player").value;

  fetch("/submit-choice",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({
      gameId:gameId,
      player:player,
      choice:choice
    })
  })
  .then(()=>fetchGame(gameId));
}

function fetchGame(gameId){
  fetch("/game/"+gameId)
  .then(res=>res.json())
  .then(game=>{
    if(game.Status==="FINISHED"){
      document.getElementById("status").innerText="Result: "+game.Result;
    }else{
      document.getElementById("status").innerText="Waiting for opponent...";
    }
  });
}
