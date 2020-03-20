var files
var flaskData = document.getElementById("flaskvar")
var filename = flaskData.getAttribute("filename")
$(document).ready( function () {
    document.getElementById("body").removeAttribute("onload")
    document.getElementById("visible").style.display = "block"
    document.getElementById("home").classList.remove("sidebar__item--selected")
    document.getElementById("filters").classList.add("sidebar__item--selected")
});

$.ajax({
    type:  'GET',
    url: '/api/files',
    contentType: false,
    cache: false,
    processData: false,
    success: function(data) {
        //alert('Success!');
        if(data.length>0)
        {
            //document.getElementById("visible").style.display="block"
            document.getElementById("statistics").setAttribute("onclick","doNav('../statistics/"+data[0]+"')")
            document.getElementById("filter").setAttribute("onclick", "doNav('../filters/" + filename + "')")
        }
    }
});




function openModal (id) {
    $('#modal-backdrop').removeClass('hide');
    //alert(o)
    $('#'+id).before('<div id="'+id+'-placeholder"></div>').detach().appendTo('body').removeClass('hide');
//document.getElementById("msg").innerHTML=o
//entById("title").innerHTML=type
}
function closeModal (id) {
    $('#'+id).detach().prependTo(('#'+id+'-placeholder')).addClass('hide');
    $('#modal-backdrop').addClass('hide');
}



$('#signature').click(function()
{
    document.getElementById("input-state-readonly").value=document.getElementById("autocomplete").value
   // console.log(document.getElementById("autocomplete").value)
openModal('modal-small-sign')
});

$('#add').click(function()
{
    var p={
        filter:document.getElementById("autocomplete").value,
    signature:document.getElementById("input-hint-default").value}
    $.ajax({
        url: '/api/signature',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
          alert("Added")   
            
        },
        data: JSON.stringify(p)
    });
});


$('#list-signature').click(function()
{
   // alert("fff")
    $.ajax({
        url: '/api/signatures',
        type: 'get',
        
        success: function (data) {
          alert(data)   
            
        },
       
    });
});
 document.getElementById("table_id").innerHTML=""
    var countries = [
 
"guid" ,
"to" ,
"from" ,
"status" ,
"Thrd" ,
"CALLGUID" ,
"DialogId" ,
"DialogID" ,
"SendSeqNo" ,
"ErrorCode",
"text" ,
"type" ,
"DNIS" ,
"ANI",
"CED" ,
"rckey" ,
"rcseq" ,
"uui" ,
"callguid",
"trunkGroupId" ,
"trunkNumber" ,
"serviceId" ,
"calledNumber" ,
"location" ,
"locationpkid" ,
"pstntrunkgroupid" ,
"sipheader" ,
"variables" ,
"arrays" ,
"Variables" ,
"text" ,
"label" ,
"correlationId" ,
"sipheader" ,
"EventID" ,
"CauseCode" ,
"rcday" ,
"uui" ,
"whisperAnnounce" 
   ];
   let re  = /and\s|or\s|&&\s|\|\|\s/gi;
   $('#autocomplete').autocomplete({
     lookupLimit:5,
       lookup: countries,
       delimiter:re,
       onSelect: function (suggestion) {
          // alert('You selected: ' + suggestion.value + ', ' + suggestion.data);
           
       },
       beforeRender: function (container) {
         console.log(document.getElementById("autocomplete").value)
       }
   });
   
   $('#submit').click(function()
   {
     //alert("ggg")
     var p=document.getElementById("autocomplete").value
     console.log(p)
     //document.getElementById("entered_query").innerHTML=p
     var person = {
               filter: p,
               filename:filename
           }
           if (document.getElementById("table_id").innerHTML!="") {
                var table1 = $('#table_id').DataTable();
                table1.destroy();
                document.getElementById("table_id").innerHTML=""

              //  console.log(document.getElementById("table_id").innerHTML.length)
           }
           //console.log(document.getElementById("table_id").innerHTML)
   
     $.ajax({
               url: '/api/filter',
               type: 'post',
               dataType: 'json',
               contentType: 'application/json',
               success: function (data) {
                // temp=data.guids.toString().replace(/,/g,"<br>")
                  // document.getElementById("out").innerHTML=temp
                  files=[]
                  console.log(data.guids.length)
                  for(i=0;i<data.guids.length;i++)
            {
                files[i]=[]
                files[i]=[data.guids[i],"<a href='#' id='seq_diag' onclick='seq(" + i + ")'>Details</a>","<a href='#' id='sign' onclick='sign("+i+")'>Signatures</a>"]
            }
            /* if (document.getElementById("table_id").innerHTML != "") {
                var table1 = $('#table_id').DataTable();
                table1.destroy()
            }*/
            //document.getElementById('table_id').innerHTML = ""
            $('#table_id').DataTable(
    {scrollY:        '50vh',
        scrollCollapse: true,
        data: files,
            columns: [
            { title: "ID" },
                    { title: "Details" } ,
                    {title:"Signatures"}
               
            ],
           
            } ); 
                   
               },
               data: JSON.stringify(person)
           });
   });

   function seq(i) {
            var table = $('#table_id').DataTable();
            
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


        function sign(i) {
            var table = $('#table_id').DataTable();
            
            data = table.rows(i).data()[0][0]

            $.ajax({
                type: 'GET',
                url: '/api/match/' + data+'/'+filename,
                contentType: false,
                cache: false,
                processData: false,
                success: function (data) {
                    console.log(data)
                }
            });
            //open diagram in new page
           // window.open("/diagram/" + data);
            openModal('modal-small')
        }
