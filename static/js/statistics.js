

var flaskData = document.getElementById("flaskvar")
var filename = flaskData.getAttribute("filename")
//document.getElementById("body").removeAttribute("onload")
//document.getElementById("visible").style.display = "block"
document.getElementById("home").classList.remove("active")
document.getElementById("details").classList.add("active")
get_table(filename)

$.ajax({
    type: 'GET',
    url: '/api/files',
    contentType: false,
    cache: false,
    processData: false,
    success: function (data) {
        //alert('Success!');
        if (data.length > 0) {
            //document.getElementById("visible").style.display="block"
        //    document.getElementById("statistics").setAttribute("onclick", "doNav('../statistics/" + filename + "')")
         //   document.getElementById("filter").setAttribute("onclick", "doNav('../filters/" + data[0] + "')")

        }
    }
});
function get_table(filename) {
    fetch('/api/GUIDs/' + filename)
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
        GUIDs[i] = [data[i][0], data[i][1], data[i][2], "<a href='#' id='seq_diag' onclick='seq(" + i + ")'>Details</a>"];
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
            { title: "ID" },
            { title: "From" },
            { title: "To" },
            { title: "Details" }
        ]
    });

    var table = $('#call_details').DataTable();

}
//execute this when diagram for sequence is asked
function seq(i) {
    var table = $('#call_details').DataTable();
    data = table.rows(i).data()[0][0]
    $.ajax({
        type: 'GET',
        url: '/diagram/' + data,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
        }
    });
    //open diagram in new page
    window.open("/diagram/" + data);
}



























//document.getElementById("call_details").innerHTML = ""
var countries = [
    "guid",
    "to",
    "from",
    "status",
    "Thrd",
    "CALLGUID",
    "DialogId",
    "DialogID",
    "SendSeqNo",
    "ErrorCode",
    "text",
    "type",
    "DNIS",
    "ANI",
    "CED",
    "rckey",
    "rcseq",
    "uui",
    "callguid",
    "trunkGroupId",
    "trunkNumber",
    "serviceId",
    "calledNumber",
    "location",
    "locationpkid",
    "pstntrunkgroupid",
    "sipheader",
    "variables",
    "arrays",
    "Variables",
    "text",
    "label",
    "correlationId",
    "sipheader",
    "EventID",
    "CauseCode",
    "rcday",
    "uui",
    "whisperAnnounce",
    "NEW_TRANSACTION_EVENT",
    "SET_CALL_VARIABLES_EVENT",
    "OPEN_REQ",
    "OPEN_CONF",
    "FAILURE_CONF",
    "FAILURE_EVENT",
    "HEARTBEAT_REQ",
    "HEARTBEAT_CONF",
    "CLOSE_REQ",
    "CLOSE_CONF",
    "ROUTE_REQUEST_EVENT",
    "ROUTE_SELECT",
    "ROUTE_END_EVENT",
    "ROUTE_END",
    "REGISTER_VARIABLES",
    "INIT_DATA_REQ",
    "INIT_DATA_CONF",
    "INIT_TRKGRP_DATA_EVENT",
    "INIT_SERVICE_DATA_EVENT",
    "INIT_VRU_DATA_EVENT",
    "INIT_DATA_END_EVENT",
    "DELIVERED_EVENT",
    "ORIGINATED_EVENT",
    "CALL_CLEARED_EVENT",
    "CONFERENCED_EVENT",
    "DELIVERED_EVENT",
    "VRU_STATUS_EVENT",
    "TRKGRP_STATUS_EVENT",
    "SERVICE_STATUS_EVENT",
    "ROUTE_REQUEST_EVENT",
    "ROUTE_SELECT",
    "ROUT_END_EVENT",
    "ROUTE_END",
    "TIME_SYNCH_REQ",
    "TIME_SYNCH_CONF",
    "SERVICE_CONTROL",
    "INIT_SERVICE_CTRL_REQ",
    "INIT_SERVICE_CTRL_CONF",
    "INIT_SERVICE_CTRL_DATA",
    "FEATURE_RUN_SCRIPT",
    "FEATURE_CONNECT","FEATURE_CANCEL","FEATURE_RELEASE","INIT_SERVICE_CTRL_TRKGRP","INIT_SERVICE_CTRL_SERVICE","INIT_SERVICE_CTRL_VRU","INIT_SERVICE_CTRL_END","TRKGRP_STATUS","SERVICE_STATUS","VRU_STATUS","NEW_CALL","REQUEST_INSTRUCTION","RUN_SCRIPT_REQ","RUN_SCRIPT_RESULT","EVENT_REPORT","DIALOG_FAILURE_CONF","DIALOG_FAILURE_EVENT","CONNECT_TO_RESOURCE","TEMPORARY_CONNECT","RESOURCE_CONNECTED"

];
let re = /and\s|or\s|&&\s|\|\|\s|\'/gi;
$('#autocomplete').autocomplete({
    lookupLimit: 5,
    lookup: countries,
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
    if (document.getElementById("call_details").innerHTML != "") {
        var table1 = $('#call_details').DataTable();
        table1.destroy();
        document.getElementById("call_details").innerHTML = ""

        //  console.log(document.getElementById("table_id").innerHTML.length)
    }
    //console.log(document.getElementById("table_id").innerHTML)

    $.ajax({
        url: '/api/filter',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            // temp=data.guids.toString().replace(/,/g,"<br>")
            // document.getElementById("out").innerHTML=temp
            files = []
            console.log(data.guids.length)
            for (i = 0; i < data.guids.length; i++) {
                files[i] = []
                files[i] = [data.guids[i], "<a href='#' id='seq_diag' onclick='seq(" + i + ")'>Details</a>", "<a href='#' id='sign' onclick='sign(" + i + ")'>Signatures</a>"]
            }

            $('#call_details').DataTable(
                {
                    scrollY: '50vh',
                    scrollCollapse: true,
                    data: files,
                    columns: [
                        { title: "ID" },
                        { title: "Details" },
                        { title: "Signatures" }
                    ],

                });
        },
        data: JSON.stringify(person)
    });
});

function seq(i) {
    var table = $('#call_details').DataTable();

    data = table.rows(i).data()[0][0]
    $.ajax({
        type: 'GET',
        url: '/diagram/' + data,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
        }
    });
    //open diagram in new page
    window.open("./"+filename+"/" + data);
}

function sign(i) {
    var table = $('#table_id').DataTable();

    data = table.rows(i).data()[0][0]

    $.ajax({
        type: 'GET',
        url: '/api/match/' + data + '/' + filename,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            console.log(data)
        }
    });
    //open diagram in new page
    // window.open("/diagram/" + data);
    openModal('modal-small')
}

