// Add handler for the back button
window.addEventListener('popstate', function(event) {
  if(event.state) {
    spa_nav(event.state.path, false)
  }
}, false);

function spa_nav(destination, updateHistory=true) {
  $.ajax({
    url: api+"/pages/content?page="+destination,
    success: function(result) {
      update_page(result.path, result.title, result.content);

      if(updateHistory) {
        // Update browser history
        window.history.pushState({
          title: result.title,
          path: result.path
        }, browser_title, result.path);
      }
    },
    error: function(result) {
      console.log('ERROR');
      console.log(result.status);
    }
  });
}

function update_page(path, title, content) {
      browser_title = "Bryan Wyatt - " + title;

      // Set page content
      $("head > title").html(browser_title);
      $("#sitecontent > #pagetitle > h2").html(title);
      $("#sitecontent > #pagecontent").html(content);

      // Log the action in Google Analytics
      ga('set', 'page', path);
      ga('send', 'pageview');

      // Reset the navbar selections
      $("#viewpane > #navbar > ul > li").removeClass("sel");
      // Will need to fix this to match what's done in the Jinja2 template
      $("#viewpane > #navbar > ul > li > a[href='"+path+"']").parent().addClass("sel");
}

/* vim: set ts=2 sw=2 sts=2 expandtab: */
