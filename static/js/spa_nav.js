// Add handler for the back button
window.addEventListener('popstate', function(event) {
  if(event.state) {
    spa_nav(event.state.path, false)
  }
}, false);

const site_title = "Bryan Wyatt"

function spa_nav(destination, updateHistory=true) {
  set_loading_animation();
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

function set_loading_animation() {
  // Set page content
  $("head > title").html(site_title);
  $("#sitecontent > #pagetitle > h2").html('Loading...');
  $("#sitecontent > #pagecontent").html([
    "<div class=\"spinner\">",
    "  <div class=\"rect1\"></div>",
    "  <div class=\"rect2\"></div>",
    "  <div class=\"rect3\"></div>",
    "  <div class=\"rect4\"></div>",
    "  <div class=\"rect5\"></div>",
    "</div>"
  ].join('\n'));
}

function update_page(path, title, content) {
      browser_title = site_title + " - " + title;

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
