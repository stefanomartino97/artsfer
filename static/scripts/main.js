let thirdPanel = false;

function isInSecondPanel() {
  return window.scrollY >= window.innerHeight;
}

function isInThirdPanel() {
  return 2 * window.scrollY >= window.innerHeight;
}

const sky = document.getElementById("sky");
const city = document.getElementById("city");
const tree = document.getElementById("tree");

const background = document.getElementById("background");
const firstLevel = document.getElementById("first-level");
const secondLevel = document.getElementById("second-level");

const backgroundDali = document.getElementById("background-dali");
const firstLevelDali = document.getElementById("first-layer-dali");

//Always start at the first panel
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
    2000
  );
};

document.getElementById("second-panel-button").onclick = function () {
  $("html, body").animate(
    {
      scrollTop: $("#third-panel").offset().top,
    },
    2000
  );
};

window.ontouchmove = function () {
  console.log("Hello");
};

/* Parallax */

window.addEventListener("scroll", function () {
  const value = window.scrollY;

  sky.style.top = value * 0.5 + "px";
  city.style.top = value * 0.3 + "px";
  tree.style.top = value * 0.1 + "px";

  if (isInSecondPanel()) {
    background.style.top = (value - window.innerHeight) * 0.7 + "px";
    firstLevel.style.top = (value - window.innerHeight) * 0.5 + "px";
    secondLevel.style.top = (value - window.innerHeight) * 0.1 + "px";
  }

  if (isInThirdPanel()) {
    thirdPanel = true;
  }

  if (thirdPanel) {
    backgroundDali.style.top = (value - 2 * window.innerHeight) * 0.7 + "px";
    firstLevelDali.style.top = (value - 2 * window.innerHeight) * 0.2 + "px";
  }
});
