// Set initial browser state
window.history.replaceState({
  title: $("#sitecontent > #pagetitle > h2").html(),
  path: window.location.pathname,
}, $("head > title").html(), window.location.pathname);

// Add handler for the back button
window.addEventListener('popstate', function(event) {
  if(event.state) {
    spa_nav(event.state.path, false, true)
  }
}, false);

// Prevent lingering "active" state
$("#navbar > ul > li > a").each(function(){this.onmouseup = this.blur();});

const site_title = "Bryan Wyatt"
var xhr = false;

function spa_nav(destination, updateHistory=true, forceReload=false) {
  if(!forceReload && destination == window.location.pathname) {
    // Don't do anything if we're already there!
    return
  }

  if(xhr) {
    xhr.abort()
  }

  if(updateHistory) {
    // Update browser history
    window.history.pushState({
      title: destination,
      path: destination
    }, destination, destination);
  }

  // Set selected page
  $("#navbar > ul > li > a").each(function(){this.blur();});
  $("#navbar > ul > li").removeClass("sel");
  // Will need to fix this to match what's done in the Jinja2 template
  $("#navbar > ul > li > a[href='"+destination+"']").parent().addClass("sel");

  set_loading_animation();
  xhr = $.ajax({
    url: api+"/pages/content?page="+destination,
    success: function(result) {
      update_page(result.path, result.title, result.content);
    },
    error: function(result) {
      console.log("ERROR: " + result.status);
      console.log("Response: ", result);
      try {
        response = JSON.parse(result.responseText);
        update_page(destination, response.title, response.content);
      } catch(err) {
        update_page(destination, "Unexpected Error: " + result.status,
          "<p>An unexpected error happened while trying to process the request.</p>"
          + "<p>Try again later.</p>")
      }
    }
  });
}

function set_loading_animation() {
  // Set page content
  $("head > title").html(site_title + " - Loading...");
  $("#sitecontent > #pagetitle > h2").html("Loading...");
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

  window.history.replaceState({
    title: title,
    path: path
  }, browser_title, path);

  // Refresh page ads
  if(googletag) {
    googletag.pubads().refresh();
  }
}

/* vim: set ts=2 sw=2 sts=2 expandtab: */
