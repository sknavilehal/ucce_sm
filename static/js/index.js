document.getElementById("body").setAttribute("onload", "initial()")
Dropzone.autoDiscover = false;

var files = []
function initial() {
    $.ajax({
        type: 'GET',
        url: '/files',

        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {

            if (data.length > 0) {

                console.log(data[0])
                document.getElementById("details-link").setAttribute("href", "call-summary/" + data[0][0])

            }

            for (i = 0; i < data.length; i++) {
                console.log(data[i][0])
                files[i] = []
                if (data[i][2] === "Processed")
                    files[i] = [data[i][0], data[i][1], `<button type='button' class='btn btn-primary btn-sm btn-success processed' disabled >${data[i][2]}</button>`,
                    "<div class='btn-group' role='group' aria-label='Basic example'><i class='fa fa-play-circle fa-2x ' style='color:#28a745;cursor:pointer' title='View Details' aria-hidden='true' onclick='analyse(" + i + ")'></i><i class='fa fa-minus-circle fa-2x' style='color:#dc3545;margin-left:5px;cursor:pointer' title='Remove' aria-hidden='true' onclick='del(" + i + ")'></i><i class='fa fa-arrow-circle-down fa-2x' style='color:#FFC107;margin-left:5px;cursor:pointer' title='Download' onclick='download(" + i + ")' data-toggle='modal' data-target='#exampleModal' aria-hidden='true'></i></div>",
                    `<button type='button' class='btn btn-sm btn-outline-primary signature'  data-toggle='modal' data-target='#exampleModal1' onclick='sign("${data[i][0]}")'>Signature</button>`]

                //  " <div class='btn-group' role='group' aria-label='Basic example'><button type='button' class='btn btn-sm btn-warning view' onclick='analyse(" + i + ")'>View</button><button type='button' class='btn btn-sm btn-danger remove' onclick='del(" + i + ")'>Remove</button></div>"   ]
                else if (data[i][2] === "Processing...")
                    files[i] = [data[i][0], data[i][1], `<button type='button' class='btn btn-primary btn-sm btn-warning'disabled >${data[i][2]}</button>`
                        , "<button type='button' class='btn btn-sm btn-primary refresh'  onclick='refresh(" + i + ")' title='Refresh'>Refresh</button>", "", ""]
                else
                    files[i] = [data[i][0], data[i][1], `<button type='button' class='btn btn-primary btn-sm btn-danger' disabled >${data[i][2]}</button>`, "<i class='fa fa-minus-circle fa-2x' style='color:#dc3545;margin-left:5px;cursor:pointer' title='Remove' aria-hidden='true' onclick='del(" + i + ")'>", "", ""]
            }

            if ($.fn.dataTable.isDataTable('#table_id')) {
                table = $('#table_id').DataTable();
                table.destroy();
            }
            $('#table_id').DataTable(
                {
                    data: files,
                    columns: [
                        { title: "Filename" },
                        { title: "Device" },
                        { title: "Status" },
                        { title: "Actions", "width": "20%" },
                        { title: "Signature" }
                    ],
                    stateSave: true
                });
        }
    });

}

options = {
    autoDiscover: false,
    url: '/uploads',
    acceptedFiles: '.txt,.log,.zip',
    addRemoveLinks: true,
    dictDefaultMessage: 'Drag a log file here to save, or click to select one',
    thumbnailWidth: '50px',
    removedfile: function (file) {
        file.previewElement.remove();
    },
    autoProcessQueue: false,
    init: function () {

        var myDropzone = this;

        // Update selector to match your button
        $("#upload").click(function (e) {
            e.preventDefault();
            myDropzone.processQueue();
        });
        this.on("queuecomplete", function (file) {
            initial()
        });
        if (this.element.dropzone) {
            return this.element.dropzone;
        }
    }
};

uploader = new Dropzone('#upload-widget', options);
$("#button").click(function (e) {
    e.preventDefault();
    uploader.processQueue();
});

function analyse(i) {
    var table = $('#table_id').DataTable();
    data = table.rows(i).data()[0][0]
    //alert(data)
    location.href = '/call-summary/' + data
    //open diagram in new page
    //window.open("/diagram/" + data);
}

function del(i) {
    var table = $('#table_id').DataTable();
    data = table.rows(i).data()[0][0]
    $.ajax({
        type: 'GET',
        url: '/delete/' + data,
        success: function (data) {
            console.log(data)
        }
    });
    //initial()
    location.reload()
}

function refresh(i) {
    initial()
}

function sign(data) {
    $.ajax({
        type: 'GET',
        url: `/match-signatures/${data}/`,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            console.log(data.signatures)
            var temp = ""
            var i
            for (i = 0; i < data.signatures.length; i++) {
                temp = temp + data.signatures[i]
            }
            document.getElementById("signatures1").innerHTML = temp

        }
    });
    //openModal('modal-small')
}

$(function () {
    $('input[name="daterange"]').daterangepicker({
        opens: 'left'
    }, function (start, end, label) {
        console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
    });
});

function download(i) {
    var table = $('#table_id').DataTable();
    data = table.rows(i).data()[0][0]
    document.getElementById("title").innerHTML = data
}
function send() {
    //alert("ff")
    var p =
    {
        from_date: document.getElementById("start").value,
        to_date: document.getElementById("end").value,
        filename: document.getElementById("title").innerHTML
    }
    $.ajax({
        url: '/logAccess',
        type: 'post',

        data: JSON.stringify(p),
        success: function (data) {
            var url = URL.createObjectURL(data);
            alert(url)
        },

    });
}