var flaskData = document.getElementById("flaskvar")
var filename = flaskData.getAttribute("filename")
console.log(filename)
function system_alerts() {
    $.ajax({
        url: `/system-alerts?filename=${filename}`,
        type: 'GET',
        success: function (data) {
            $('#system_alerts').DataTable(
                {
                    scrollY: '50vh',
                    scrollCollapse: true,
                    data: data,
                    columns: [
                        { title: "No." },
                        { title: "Alert" },
                        { title: "View" }
                    ],
                });
        }

    });

}
system_alerts()