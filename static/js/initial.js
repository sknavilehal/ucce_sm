

function initial() {
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
                document.getElementById("statistics").setAttribute("onclick","doNav('statistics/"+data[0]+"')")
            }

        }
    });
}

//alert("ggg")
options = {
    url: '/uploads',
    acceptedFiles: '.txt,.log',
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
            initial()});
    }

};

const uploader = new Dropzone('#upload-widget', options);
$("#button").click(function (e) {
    e.preventDefault();
    uploader.processQueue();
});