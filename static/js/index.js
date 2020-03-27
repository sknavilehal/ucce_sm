document.getElementById("body").setAttribute("onload","initial()")
Dropzone.autoDiscover = false;
var files=[]
function initial(){
    $.ajax({
        type: 'GET',
        url: '/api/files',

        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            
            if (data.length > 0) {
                
                console.log(data[0])
                document.getElementById("details-link").setAttribute("href","details/" + data[0][0] )
              
            }
            
            for (i = 0; i < data.length; i++) {
                console.log(data[i][0])
                files[i] = []
                if (data[i][2] === "Processed")
                    files[i] = [data[i][0], data[i][1], "<button type='button' class='btn btn-primary btn-sm btn-success processed' disabled >Processed</button>", 
                    " <div class='btn-group' role='group' aria-label='Basic example'><button type='button' class='btn btn-sm btn-warning view' onclick='analyse(" + i + ")'>View</button><button type='button' class='btn btn-sm btn-danger remove' onclick='del(" + i + ")'>Remove</button></div>"   ]
                else if (data[i][2] === "Processing...")
                    files[i] = [data[i][0], data[i][1], "<button type='button' class='btn btn-primary btn-sm btn-warning'disabled >Processing</button>"
                    ,"  <button type='button' class='btn btn-sm btn-primary refresh'  onclick='refresh("+i+")' title='Refresh'>Refresh</button>" ]
                else
                    files[i] = [data[i][0], data[i][1], data[i][2], "<span class='icon-remove-contain icon-size-20' onclick='del(" + i + ")' style='cursor:pointer;color:#a52727' title ='Remove' ></span>"]
            }
            //console.log(files)
            //files
            //console.log(files)
            if ( $.fn.dataTable.isDataTable( '#table_id' ) ) {
                table = $('#table_id').DataTable();
                table.destroy();
            }
            $('#table_id').DataTable(
                {
                    data: files,
                    columns: [
                        { title: "Filename" },
                        { title: "Device"},
                        { title: "Status" },
                        { title: "Actions","width":"30%" },

                    ],
                    stateSave: true
                });
        }
    });

}


//alert("ggg")
options = {
    autoDiscover:false,
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
    location.href='/details/' + data
    //open diagram in new page
    //window.open("/diagram/" + data);
}

function del(i) {
    var table = $('#table_id').DataTable();
    data = table.rows(i).data()[0][0]
    $.ajax({
        type: 'GET',
        url: '/api/delete/' + data,
        success: function (data) {
            console.log(data)
            

        }
    });
    //initial()
    location.reload()
}

function filter(i) {
    var table = $('#table_id').DataTable();
    data = table.rows(i).data()[0][0]
    //alert(data)
    doNav('/filters/' + data)
}

function refresh(i)
{
    initial()
}