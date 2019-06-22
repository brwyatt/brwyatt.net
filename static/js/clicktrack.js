function clicktrack(event) {
  console.log("Event: %O", event);
  if(event.target.nodeName == 'A') { // only operate on link tags
    if(event.target.host != event.target.baseURI.split('/')[2]) { // Ignore self links
      // Fire and forget!
      $.ajax({
        method: "POST",
        url: api+"/tracking/linkclick",
        data: {
          Source: event.target.baseURI,
          Destination: event.target.href,
          Text: event.target.innerText,
        },
        success: function(result) {
          console.log("Click logged");
        },
        error: function(result) {
          console.log("ERROR: " + result.status);
          console.log("Response: ", result);
        }
      });
    }
  }
}

/* vim: set ts=2 sw=2 sts=2 expandtab: */
