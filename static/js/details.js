import suggestions from './suggestions.js';

var flaskData = document.getElementById("flaskvar")
var filename = flaskData.getAttribute("filename")
document.getElementById("home").classList.remove("active")
get_table(filename)
window.seq = seq
window.sign = sign
window.get_table = get_table

$.ajax({
    type: 'GET',
    url: '/files',
    contentType: false,
    cache: false,
    processData: false,
    success: function (data) {
        //alert('Success!');
        if (data.length > 0) {
            var d=document.getElementById("files")
            var temp=""
            for(let i=0;i<data.length;i++)
            {
                temp=temp+"<a class='dropdown-item' onclick='get_table(\""+data[i][0]+"\")' href='#'>"+data[i][0]+"</a>"
            }
            d.innerHTML=temp
        }
    }
});
function get_table(filename) {
    fetch(`/Files-History/analyze?filename=${filename}`)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            //add data to datatables
            appendData(data);
        })
        .catch(function (err) {
            console.log(err);
        });
}

function appendData(table) {
    console.log(table)
    var data = table["GUIDs"]
    var headers = table["headers"]
    var GUIDs = [];
    for (var i = 0; i < data.length; i++) {
        GUIDs[i] = [];
        //for Details hyperlink to work
        GUIDs[i] = [data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], `<a href='#' id='seq_diag' onclick='seq("${data[i][0]}")'>Details</a>`, `<a href='#' id='sign' data-toggle='modal' data-target='#exampleModal' onclick='sign("${data[i][0]}")'>Signature</a>`];
    }
    //destroy the tables content when switching b/w files
    if (document.getElementById("call_details").innerHTML != "") {
        var table1 = $('#call_details').DataTable();
        table1.destroy()
    }
    document.getElementById('call_details').innerHTML = ""
    $('#call_details').DataTable({
        data: GUIDs,
        //columns for database
        columns: headers
    });

    var table = $('#call_details').DataTable();
}

let re = /and\s|or\s|&&\s|\|\|\s|\'/gi;
$('#autocomplete').autocomplete({
    lookupLimit: 6,
    lookup: suggestions,
    delimiter: re,
    onSelect: function (suggestion) {
        // alert('You selected: ' + suggestion.value + ', ' + suggestion.data);
    },
    beforeRender: function (container) {
    }
});

$('#submit').click(function () {
    //alert("ggg")
    var p = document.getElementById("autocomplete").value
    //document.getElementById("entered_query").innerHTML=p
    var person = {
        filter: p,
        filename: filename
    }
    $.ajax({
        url: 'Call-Summary/filter',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(person),
        success: function (data) {
            appendData(data)
        }
    });
});

function seq(data) {
    window.open(`/diagram-page?filename=${filename}&guid=${data}`);
}

function sign(data) {
    $.ajax({
        type: 'GET',
        url: `/Call-Summary/signature?filename=${filename}&guid=${data}`,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            var temp="<ol>"
            for(var i=0;i<data.signatures.length;i++)
            {
                temp=temp+`<li>${data.signatures[i]}</li>`
            }
            temp = temp + "</ol>"
            document.getElementById("signatures1").innerHTML=temp

        }
    });
    //openModal('modal-small')
}

