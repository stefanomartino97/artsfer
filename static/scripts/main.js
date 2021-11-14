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

$("#run-button").click(() => {
  let currentEpoch = 0;

  $("#modal-show").fadeIn(1000);
  const epochs = parseInt(document.getElementById("myRange").value);
  $("#status").html(`0/${epochs}`);

  //Get uploaded images
  const contentImage = document.getElementById("content-image-upload").files[0];
  const styleImage = document.getElementById("style-image-upload").files[0];

  const socket = io();

  socket.on("connect", function () {
    socket.emit("upload", { epochs, contentImage, styleImage });
  });

  socket.on("epoch", function (data) {
    currentEpoch++;

    if (currentEpoch == epochs) {
      //Done
      $("#logo-gif").hide();
      $("#logo-still").show();
    }

    $("#status").html(`${currentEpoch}/${epochs}`);
    $("#inner").css("width", `${Math.floor((currentEpoch * 100) / epochs)}%`);

    $("#download").fadeIn();
    $("#download").attr("href", data["data"]);
    $("#transfer-img").fadeOut(function () {
      $(this).attr("src", data["data"]).fadeIn();
    });
  });
});

$("#close").click(() => {
  $("#modal-show").fadeOut(500);
  $("#inner").css("width", "0%");
  const epochs = parseInt(document.getElementById("myRange").value);
  $("#status").html(`0/${epochs}`);
  $("#download").fadeOut();
  $("#logo-gif").show();
  $("#logo-still").hide();
});

/*Upload Image*/
document.getElementById("content-image-upload").onchange = (event) => {
  const imageURL = URL.createObjectURL(event.target.files[0]);
  document.getElementById("content-image").src = imageURL;
};

document.getElementById("style-image-upload").onchange = (event) => {
  const imageURL = URL.createObjectURL(event.target.files[0]);
  document.getElementById("style-image").src = imageURL;
};

/*Slider*/
document.getElementById("myRange").oninput = function () {
  document.getElementById("range-value").innerHTML = this.value;
};
