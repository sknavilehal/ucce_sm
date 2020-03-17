var files
$(document).ready( function () {
    document.getElementById("body").removeAttribute("onload")
    document.getElementById("visible").style.display = "block"
    document.getElementById("home").classList.remove("sidebar__item--selected")
    document.getElementById("sign").classList.add("sidebar__item--selected")
});