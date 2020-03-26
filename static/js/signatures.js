
$(document).ready(function () {
    document.getElementById("body").setAttribute("onload", "signature()")
    document.getElementById("visible").style.display = "block"
    document.getElementById("home").classList.remove("sidebar__item--selected")
    document.getElementById("sign").classList.add("sidebar__item--selected")
});
console.log("message")
$.ajax({
    type: 'GET',
    url: '/api/files',
    contentType: false,
    cache: false,
    processData: false,
    success: function (data) {
        if (data.length > 0) {
            //document.getElementById("visible").style.display="block"
            document.getElementById("statistics").setAttribute("onclick", "doNav('/statistics/" + data[0] + "')")
            document.getElementById("filter").setAttribute("onclick", "doNav('/filters/" + data[0] + "')")
        }
    }
});

$('#add').click(function () {
    var p = {
        signature: document.getElementById("input-state-readonly").value,
        description: document.getElementById("input-hint-default").value
    }
    console.log(p)
    if (document.getElementById("table_id").innerHTML != "") {
        var table1 = $('#table_id').DataTable();
        table1.destroy();
        document.getElementById("table_id").innerHTML = ""
    }
    $.ajax({
        url: '/api/signature',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(p),
        success: function (data) {
            signature()
        },
    });
});


function signature() {
    list = []
    $.ajax({
        url: '/api/signatures',
        type: 'get',

        success: function (data) {
            console.log(data)
            for (i = 0; i < data.length; i++) {
                list[i] = []
                list[i] = [data[i][0], data[i][1]]
            }
            $('#table_id').DataTable(
                {
                    scrollY: '50vh',
                    scrollCollapse: true,
                    data: list,
                    columns: [
                        { title: "Signature" },
                        { title: "Description" }
                    ],
                });
        }
    });
}