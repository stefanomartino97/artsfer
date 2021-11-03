//ALways start at the first panel
const panels = ["first-panel", "second-panel", "third-panel"];
document.getElementById(panels[0]).scrollIntoView();
let currentPanel = 0;
let lastScrollTop = 0;

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

window.ontouchmove = function () {
  console.log("Hello");
};

/*const _window = $(window);
_window.scroll(function (event) {
  const currentScrollTop = $(this).scrollTop();
  if (currentScrollTop > lastScrollTop) {
    //downscroll
    if (currentPanel > 0) {
      currentPanel--;
    }
  } else {
    //upscroll
    if (currentPanel < panels.length - 1) {
      currentPanel++;
    }
  }

  lastScrollTop = currentScrollTop;
});*/
