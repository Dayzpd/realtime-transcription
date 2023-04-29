


function transcriptionTemplate(text) {

  return (
    `<div class="d-flex text-body-secondary pt-3 my-auto">
      <p class="pb-3 mb-0 small lh-sm border-bottom">${text}</p>
    </div>`
  )
}

function establishConnection() {

  const socket = new WebSocket("ws://127.0.0.1/sockets/english");

  if (!socket) return establishConnection();

  return socket;
}


window.addEventListener("load", () => {

  const socket = establishConnection();

  const transcriptionsBox = document.getElementById("transcriptions");

  socket.addEventListener("open", (event) => {
    console.log("Listening for new transcriptions...")
  });

  socket.addEventListener("message", (event) => {

    const data = JSON.parse(event.data);

    if (!data.text) return;

    const transcription = document.createElement("div")
    
    transcription.innerHTML = transcriptionTemplate(data.text);
    
    transcriptionsBox.append(transcription);

  });

})