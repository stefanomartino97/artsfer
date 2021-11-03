//Add Scroll functions
document.getElementById("first-panel-button").onclick = function () {
  $("html, body").animate(
    {
      scrollTop: $("#second-panel").offset().top,
    },
    1000
  );
};

document.getElementById("second-panel-button").onclick = function () {
  $("html, body").animate(
    {
      scrollTop: $("#third-panel").offset().top,
    },
    1000
  );
};
