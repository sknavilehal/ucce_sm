var files
$(document).ready( function () {
    document.getElementById("body").removeAttribute("onload")
    document.getElementById("visible").style.display = "block"
    document.getElementById("home").classList.remove("sidebar__item--selected")
    document.getElementById("sign").classList.add("sidebar__item--selected")
});

$.ajax({
    type: 'GET',
    url: '/api/files',
    contentType: false,
    cache: false,
    processData: false,
    success: function(data) {
        //alert('Success!');
        if(data.length>0)
        {
            //document.getElementById("visible").style.display="block"
            document.getElementById("statistics").setAttribute("onclick","doNav('statistics/"+data[0]+"')")
        }
    }
});
