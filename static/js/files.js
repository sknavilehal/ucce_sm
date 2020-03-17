var files
$(document).ready( function () {
    document.getElementById("body").removeAttribute("onload")
    document.getElementById("visible").style.display = "block"
    document.getElementById("home").classList.remove("sidebar__item--selected")
    document.getElementById("files").classList.add("sidebar__item--selected")
   files=[]
    $.ajax({
        type: 'GET',
        url: '/api/files',
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
            //alert('Success!');
            if(data.length>0)
            {
                //document.getElementById("visible").style.display="block"
                document.getElementById("statistics").setAttribute("onclick","doNav('statistics/"+data[0]+"')")
            }
            for(i=0;i<data.length;i++)
            {
                files[i]=[]
                files[i]=[data[i],"<span class='icon-play-contained icon-size-20'  onclick='analyse("+i+")'  title='Analyse' style='cursor:pointer;color:green' ></span><span class='icon-remove-contain icon-size-20' onclick='del("+i+")' style='cursor:pointer;color:#a52727;margin-left:1rem' title ='Remove' ></span>"]
            }
            console.log(files)
            files
            console.log(files)
            $('#table_id').DataTable(
    {
        data: files,
            columns: [
                { title: "Filename" },
                { title: "Actions" },
               
            ],
            stateSave: true
            } ); 
           
        }
    });
 


} );

function analyse(i) {
        var table = $('#table_id').DataTable();
        data = table.rows(i).data()[0][0]
        //alert(data)
        doNav('/statistics/'+data)
        //open diagram in new page
        //window.open("/diagram/" + data);
    }

    function del(i) {
        var table = $('#table_id').DataTable();
        data = table.rows(i).data()[0][0]
        $.ajax({
            type: 'GET',
            url: '/api/delete/'+data,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
               if(data.length>0)
               {
                   location.reload()
               }
               else{
                   location.replace('/')
               }
    
            }
        });
    }