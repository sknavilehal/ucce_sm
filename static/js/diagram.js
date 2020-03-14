//var flaskData = document.getElementById("flaskvar")
var guid = flaskData.getAttribute("guid")
//for the cappi id gets the svg code of its sequence diagram and messages
$.ajax({
    type: 'GET',
    url: "/api/GUID/" + guid,
    success: function (re) {
        var s = re.svg
        //parse the svg string and convert it to HTML DOM
        var parser = new DOMParser();
        var doc = parser.parseFromString(s, "image/svg+xml");
        var all = doc.getElementsByTagName("a");
        var svg = doc.getElementsByTagName("svg");

        for (var i = 0, max = all.length; i < max; i++) {
            //remove the href elements to prevent hover
            msg_id = all[i].getAttribute("xlink:title")
            // all[i].removeAttribute("xlink:title")
            all[i].removeAttribute("xlink:href")
            all[i].removeAttribute("href")
            //add onclick function
            all[i].setAttribute("style", "text-decoration:none")
            all[i].setAttribute("onclick", "get_msgs(\"" + msg_id + "\")")
        }

        document.getElementById("diagram").innerHTML = ""
        document.getElementById("diagram").appendChild(doc.documentElement)
    }
});
function get_msgs(id) {
    $.ajax({
        type: 'GET',
        url: "/api/message/" + id,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            msg = data.msg_text
            document.getElementById("msg").textContent = msg
        }
    });
}