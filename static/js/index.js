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

            for (i = 0; i < data.length; i++) {
                files[i] = []
                if(data[i][5].length == 0)
                    errors_html = "";
                else
                    errors_html = `<i class='fa fa-exclamation-circle fa-2x' data-toggle='modal' data-target='#error_modal' style='color:#FFC107;margin-left:5px;cursor:pointer' title='Errors' onclick='errors(${i})' aria-hidden='true'></i>`;
                if (data[i][4] === "Processed")
                    files[i] = [data[i][0], data[i][1], data[i][2], data[i][3], `<button type='button' class='btn btn-primary btn-sm btn-success processed' disabled >${data[i][4]}</button>`,
                    "<div class='btn-group' role='group' aria-label='Basic example'><i class='fa fa-play-circle fa-2x ' style='color:#28a745;cursor:pointer' title='View Details' aria-hidden='true' onclick='analyse(" + i + ")'></i><i class='fa fa-minus-circle fa-2x' style='color:#dc3545;margin-left:5px;cursor:pointer' title='Remove' aria-hidden='true' onclick='del(" + i + ")'></i><i class='fa fa-arrow-circle-down fa-2x' style='color:#FFC107;margin-left:5px;cursor:pointer' title='Download' onclick='download(" + i + ")' aria-hidden='true'></i>"+errors_html+"</div>",
                    `<button type='button' class='btn btn-sm btn-outline-primary signature'  data-toggle='modal' data-target='#exampleModal1' onclick='sign("${data[i][0]}")'>Signature</button>`,data[i][5]]

                //  " <div class='btn-group' role='group' aria-label='Basic example'><button type='button' class='btn btn-sm btn-warning view' onclick='analyse(" + i + ")'>View</button><button type='button' class='btn btn-sm btn-danger remove' onclick='del(" + i + ")'>Remove</button></div>"   ]
                else if (data[i][4] === "Processing...")
                    files[i] = [data[i][0], data[i][1], data[i][2], data[i][3], `<button type='button' class='btn btn-primary btn-sm btn-warning'disabled >${data[i][4]}</button>`
                        , "<button type='button' class='btn btn-sm btn-primary refresh'  onclick='initial()' title='Refresh'>Refresh</button>", "", ""]
                else
                    files[i] = [data[i][0], data[i][1], data[i][2], data[i][3], `<button type='button' class='btn btn-primary btn-sm btn-danger' disabled >${data[i][4]}</button>`, "<i class='fa fa-minus-circle fa-2x' style='color:#dc3545;margin-left:5px;cursor:pointer' title='Remove' aria-hidden='true' onclick='del(" + i + ")'>", "", ""]
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
                        { title: "Start Time" },
                        { title: "End Time" },
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
    url: '/Files-History/upload',
    acceptedFiles: '.txt,.log,.zip',
    addRemoveLinks: true,
    dictDefaultMessage: 'Drag a log file here to save, or click to select one',
    thumbnailWidth: '50px',
    timeout: 300000,
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
    console.log("friend")
    var table = $('#table_id').DataTable();
    data = table.rows(i).data()[0][0]

    location.href = `call-summary?filename=${data}`
}

function del(i) {
    var table = $('#table_id').DataTable();
    data = table.rows(i).data()[0][0]
    $.ajax({
        type: 'GET',
        url: `/Files-History/delete?filename=${data}`,
        success: function (data) {
            location.reload()
        }
    });
}

function errors(i) {
    var data = $('#table_id').DataTable().rows(i).data()[0][7];
    var temp="<ol>"
    for(var i=0;i<data.length;i++)
        temp=temp+`<li>${data[i]}</li>`
    temp = temp + "</ol>"
    document.getElementById("prelim_sigs").innerHTML = temp
}

function sign(data) {
    $.ajax({
        type: 'GET',
        url: `/Files-History/signature?filename=${data}`,
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
            document.getElementById("signatures1").innerHTML = temp
        }
    });
}

function download(i) {
    var data = $('#table_id').DataTable().row(i).data()[0]
    window.open(`/download-file?filename=${data}`)
}