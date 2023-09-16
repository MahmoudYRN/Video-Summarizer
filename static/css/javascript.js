function myFunction() {
  var x = document.getElementById("subtn");
  var y = document.getElementById("loading");
  var z = document.getElementById("load1");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
  y.style.display = "block"
  z.style.display = "block"
}