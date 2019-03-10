function spa_nav(destination) {
  $.ajax({
    url: api+"/pages/content?page="+destination,
    success: function(result) {
      browser_title = "Bryan Wyatt - " + result.title
      $("head > title").html(browser_title)
      $("#sitecontent > #pagetitle > h2").html(result.title)
      $("#sitecontent > #pagecontent").html(result.content)
      window.history.pushState({}, browser_title, result.path)
      ga('set', 'page', result.path)
      ga('send', 'pageview')
      $("#viewpane > #navbar > ul > li").removeClass("sel")
      // Will need to fix this to match what's done in the Jinja2 template
      $("#viewpane > #navbar > ul > li > a[href='"+result.path+"']").parent().addClass("sel")
    },
    error: function(result) {
      console.log('ERROR');
      console.log(result.status);
    }
  });

  return false; // Disable link following
}

/* vim: set ts=2 sw=2 sts=2 expandtab: */
