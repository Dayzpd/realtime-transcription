function updateTranscription(children, msg) {
    console.log(children);
    console.log(typeof children);
    console.dir(children);
    if(!msg){return '';}  // no data, just return
    
    const data = JSON.parse(msg.data);  // read the data
    
    let output = '';

    if (children === 'string') output = children;
    output = `${children}<p>${data.text}</p>`;
    
    return output;
}
  
  window.dash_clientside = Object.assign({}, window.dash_clientside, {
      transcription : {
        update: updateTranscription
      }
  });