document.getElementById("home").classList.remove("active")
document.getElementById("signatures").classList.add("active")
document.getElementById("body").setAttribute("onload","signature()")

$('#add').click(function () {
    var p = {
        signature: document.getElementById("signature").value,
        description: document.getElementById("description").value
    }
    console.log(p)
    if (document.getElementById("table_id").innerHTML != "") {
        var table1 = $('#table_id').DataTable();
        table1.destroy();
        document.getElementById("table_id").innerHTML = ""

        //  console.log(document.getElementById("table_id").innerHTML.length)
    }
    $.ajax({
        url: '/post-signature',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(p),
        success: function(data) {
            signature()
        },
        
    });
});


function signature(){
list=[]
    $.ajax({
        url: '/get-signatures',
        type: 'GET',

        success: function (data) {
            console.log(data)
            for (i = 0; i < data.length; i++) {
                list[i] =[]
                list[i] =[data[i][0],data[i][1],"<div class='btn-group' role='group' aria-label='Basic example'><i class='fa fa-minus-circle fa-2x' style='color:#dc3545;margin-left:5px;cursor:pointer' title='Remove' aria-hidden='true' onclick='del(" + i + ")'></i></div>"]
            }
            $('#table_id').DataTable(
                {
                    scrollY: '50vh',
                    scrollCollapse: true,
                    data: list,
                    columns: [
                        { title: "Signature" },
                        { title: "Description" },
                        {title:"Actions"}
                    ],
                });
        }
    });
}