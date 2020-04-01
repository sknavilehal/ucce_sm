import suggestions from './suggestions.js';

var flaskData = document.getElementById("flaskvar")
var filename = flaskData.getAttribute("filename")
document.getElementById("home").classList.remove("active")
document.getElementById("details").classList.add("active")
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
            console.log(data)
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

function appendData(data) {
    var GUIDs = [];
    for (var i = 0; i < data.length; i++) {
        GUIDs[i] = [];
        //for Details hyperlink to work
        GUIDs[i] = [data[i][0], data[i][1], data[i][2], `<a href='#' id='seq_diag' onclick='seq("${data[i][0]}")'>Details</a>`, `<a href='#' id='sign' data-toggle='modal' data-target='#exampleModal' onclick='sign("${data[i][0]}")'>Signature</a>`];
    }
    //destroy the tables content when switching b/w files
    if (document.getElementById("call_details").innerHTML != "") {
        var table1 = $('#call_details').DataTable();
        table1.destroy()
    }
    document.getElementById('call_details').innerHTML = ""
    $('#call_details').DataTable({
        data: GUIDs,
        //add error codes
        "createdRow": function (row, data, dataIndex) {
            if (data[12] > 500) {
                $(row).addClass('red');
            }
            else if (data[12] > 400) {
                $(row).addClass('maroon');
            }
        },
        //columns for database
        columns: [
            { title: "GUID" },
            { title: "DNIS" },
            { title: "ANI" },
            { title: "Details" },
            { title: "Signature"}
        ]
    });

    var table = $('#call_details').DataTable();
}

let re = /and\s|or\s|&&\s|\|\|\s|\'/gi;
$('#autocomplete').autocomplete({
    lookupLimit: 5,
    lookup: suggestions,
    delimiter: re,
    onSelect: function (suggestion) {
        // alert('You selected: ' + suggestion.value + ', ' + suggestion.data);
    },
    beforeRender: function (container) {
        console.log(document.getElementById("autocomplete").value)
    }
});

$('#submit').click(function () {
    //alert("ggg")
    var p = document.getElementById("autocomplete").value
    console.log(p)
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
            console.log(data.signatures)
            var temp=""
            var i
            for(i=0;i<data.signatures.length;i++)
            {
                temp=temp+data.signatures[i]
            }
            document.getElementById("signatures1").innerHTML=temp

        }
    });
    //openModal('modal-small')
}

