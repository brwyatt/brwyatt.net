function spa_nav(destination) {
  $.ajax({
    url: api+"/pages/content?page="+destination,
    success: function(result) {
      browser_title = "Bryan Wyatt - " + result.title;

      // Set page content
      $("head > title").html(browser_title);
      $("#sitecontent > #pagetitle > h2").html(result.title);
      $("#sitecontent > #pagecontent").html(result.content);

      // Update browser history
      window.history.pushState({}, browser_title, result.path);

      // Log the action in Google Analytics
      ga('set', 'page', result.path);
      ga('send', 'pageview');

      // Reset the navbar selections
      $("#viewpane > #navbar > ul > li").removeClass("sel");
      // Will need to fix this to match what's done in the Jinja2 template
      $("#viewpane > #navbar > ul > li > a[href='"+result.path+"']").parent().addClass("sel");
    },
    error: function(result) {
      console.log('ERROR');
      console.log(result.status);
    }
  });
}

/* vim: set ts=2 sw=2 sts=2 expandtab: */
