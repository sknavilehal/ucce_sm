var flaskData = document.getElementById("flaskvar")
var filename = flaskData.getAttribute("filename")
document.getElementById("body").removeAttribute("onload")
document.getElementById("visible").style.display = "block"
document.getElementById("home").classList.remove("sidebar__item--selected")
document.getElementById("stat").classList.add("sidebar__item--selected")
get_table(filename)
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
                GUIDs[i] = [data[i][0], "<a href='#' id='seq_diag' onclick='seq(" + i + ")'>Details</a>"];
            }
            //destroy the tables content hen switching b/w files
            if (document.getElementById("example").innerHTML != "") {
                var table1 = $('#example').DataTable();
                table1.destroy()
            }
            document.getElementById('example').innerHTML = ""
            $('#example').DataTable({
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
                    { title: "Details" }
                ]
            });
    
            var table = $('#example').DataTable();
    
        }
        //execute this when diagram for sequence is asked
        function seq(i) {
            var table = $('#example').DataTable();
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