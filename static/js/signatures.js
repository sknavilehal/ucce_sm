import suggestions from './suggestions.js'

document.getElementById("home").classList.remove("active")
document.getElementById("signatures").classList.add("active")
document.getElementById("body").setAttribute("onload","signature()")
window.del = del
window.signature = signature

let re = /and\s|or\s|&&\s|\|\|\s|\'/gi;
$('#signature').autocomplete({
    lookupLimit: 6,
    lookup: suggestions,
    delimiter: re,
});

$('#add').click(function () {
    var p = {
        signature: document.getElementById("signature").value,
        description: document.getElementById("description").value
    }
    if (document.getElementById("table_id").innerHTML != "") {
        var table1 = $('#table_id').DataTable();
        table1.destroy();
        document.getElementById("table_id").innerHTML = ""
    }
    $.ajax({
        url: '/Signatures/new-sig',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(p),
        success: function(data) {
            signature()
        },
        
    });
});

function signature(){
    var list=[]
    $.ajax({
        url: '/get-signatures',
        type: 'GET',

        success: function (data) {
            for (var i = 0; i < data.length; i++) {
                list[i] =[]
                list[i] =[data[i][0],data[i][1],`<div class='btn-group' role='group' aria-label='Basic example'><i class='fa fa-minus-circle fa-2x' style='color:#dc3545;margin-left:5px;cursor:pointer' title='Remove' aria-hidden='true' onclick='del(${i})'></i></div>`]
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
function del(i){
    var data = $("#table_id").DataTable().row(i).data()
    $.ajax({
        url: `/Signatures/delete-sig?signature=${data[0]}`,
        type: `GET`,
        success: function(res){
            $('#table_id').DataTable().destroy()
            signature();
        },
        error: function(err){
            console.log(err)
        }
    });
}
