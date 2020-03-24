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
            //alert('Success!');
            if (data.length > 0) {
                document.getElementById("visible").style.display = "block"
                document.getElementById("statistics").setAttribute("onclick", "doNav('statistics/" + data[0] + "')")
                document.getElementById("filter").setAttribute("onclick", "doNav('filters/" + data[0] + "')")
           
            }
            //console.log(data.length)
            for (i = 0; i < data.length; i++) {
                console.log(data[i][0])
                files[i] = []
                if (data[i][2] === "Processed")
                    files[i] = [data[i][0], data[i][1], data[i][2], "<span class='icon-play-contained icon-size-20'  onclick='analyse(" + i + ")'  title='Analyse' style='cursor:pointer;color:green' ></span><span class='icon-remove-contain icon-size-20' onclick='del(" + i + ")' style='cursor:pointer;color:#a52727;margin-left:1rem' title ='Remove' ></span><span class='icon-filter icon-size-20' onclick='filter(" + i + ")' style='cursor:pointer;color:#e2ae1e;margin-left:1rem' title ='Filter' ></span>"]
                else if (data[i][2] === "Processing...")
                    files[i] = [data[i][0], data[i][1], data[i][2], "<span class='icon-animation icon-size-20' onclick='refresh("+i+")' title='Refresh'</span>"]
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
    doNav('/statistics/' + data)
    //open diagram in new page
    //window.open("/diagram/" + data);
}

function del(i) {
    var table = $('#table_id').DataTable();
    data = table.rows(i).data()[0][0]
    $.ajax({
        type: 'GET',
        url: '/api/delete/' + data,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            initial()

        }
    });
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