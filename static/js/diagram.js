var flaskData = document.getElementById("flaskvar")
var guid = flaskData.getAttribute("guid")
//for the cappi id gets the svg code of its sequence diagram and messages
$.ajax({
    //document.getElementById("diagram").innerHTML=
    type: 'GET',
    url: "/api/GUID/" + guid,
    success: function (re) {
        var s = re.svg
        //parse the svg string and convert it to HTML DOM
        var parser = new DOMParser();
        var doc = parser.parseFromString(s, "image/svg+xml");
        var all = doc.getElementsByTagName("a");
        var svg = doc.getElementsByTagName("svg");

        for (var i = 0, max = all.length; i < max; i++) {
            //remove the href elements to prevent hover
            msg_id = all[i].getAttribute("xlink:title")
            // all[i].removeAttribute("xlink:title")
            all[i].removeAttribute("xlink:href")
            all[i].removeAttribute("href")
            //add onclick function
            all[i].setAttribute("style","text-decoration:none;")
            all[i].setAttribute("onclick", "get_msgs(\"" + msg_id + "\")")
        }
            var all1 = doc.getElementsByTagName("text");
                for(var i = 0, max = all1.length; i < max; i++) 
                {
                    //coloring
                    all1[i].setAttribute("font-family","'Poppins', sans-serif")
                    all1[i].setAttribute("text-decoration","none")
                    all1[i].setAttribute("font-weight","300px")
                            if(all1[i].innerHTML.search("INVITE")>=0)
                            {
                         
                            all1[i].setAttribute("fill","blue")
                            }
                            if(all1[i].innerHTML.search("BYE")>=0)
                            {
                            all1[i].setAttribute("fill","orange")
                            }
                            if(all1[i].innerHTML.search("2")==0)
                            all1[i].setAttribute("fill","green")
                            if(all1[i].innerHTML.search("3")==0)
                            all1[i].setAttribute("fill","yellow")
                            if(all1[i].innerHTML.search("1")==0)
                            all1[i].setAttribute("fill","black")
                            if(all1[i].innerHTML.search("4")==0 ||all1[i].innerHTML.search("5")==0 ||all1[i].innerHTML.search("6")==0 )
                            all1[i].setAttribute("fill","red")
                    

                
        }

        document.getElementById("diagram").innerHTML = ""
        document.getElementById("diagram").appendChild(doc.documentElement)
    }
});


function openModal (id,o) {
    $('#modal-backdrop').removeClass('hide');
    //alert(o)
    $('#'+id).before('<div id="'+id+'-placeholder"></div>').detach().appendTo('body').removeClass('hide');
document.getElementById("msg").innerHTML=o
//entById("title").innerHTML=type
}
function closeModal (id) {
    $('#'+id).detach().prependTo(('#'+id+'-placeholder')).addClass('hide');
    $('#modal-backdrop').addClass('hide');
}
function get_msgs(id) {
    $.ajax({
        type: 'GET',
        url: "/api/message/" + id,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            msg = data.msg_text
            //alert(msg)
            msg= msg.replace(/</g,"&lt;")
    
            msg= msg.replace(/>/g,"&gt;")
            //console.log(m[o].search("<"))
    //console.log(m[o])
    var temp=msg.split("\n")
    
    for(i=0;i<temp.length;i++)
    {
        if(temp[i].startsWith("m=")==1)
        {
            //console.log(temp[i])
            temp[i]="<span style='background-color:#7bff61ba'>"+temp[i]+"</span>"
        }
        if(temp[i].startsWith("a=")==1)
        {
            //.log(temp[i])
            temp[i]="<span style='background-color:#fffc55'>"+temp[i]+"</span>"
        }
        if(temp[i].indexOf("DialogId")>-1)
        {
            //console.log(temp[i])
            //temp[i]="<span style='background-color:#7bff61ba'>"+temp[i]+"</span>"
            y=temp[i].indexOf("DialogId")
            z=temp[i].indexOf(" ",y)
            console.log(y,z)
            temp[i]=temp[i].slice(0,y)+"<span style='background-color:#b061ffba'>"+temp[i].slice(y,z)+"</span>"+temp[i].slice(z,)
        }
        if(temp[i].indexOf("%CVP")>-1)
        {
            //console.log(temp[i])
            //temp[i]="<span style='background-color:#7bff61ba'>"+temp[i]+"</span>"
            y=temp[i].indexOf("%CVP")
            z=temp[i].indexOf(":",y)
            console.log(y,z)
            temp[i]=temp[i].slice(0,y)+"<span style='background-color:#79b9ef'>"+temp[i].slice(y,z)+"</span>"+temp[i].slice(z,)
        }
        if(temp[i].indexOf("CALLGUID")>-1)
        {
            //console.log(temp[i])
            //temp[i]="<span style='background-color:#7bff61ba'>"+temp[i]+"</span>"
            y=temp[i].indexOf("CALLGUID")
            z=temp[i].indexOf(" ",y)
            console.log(y,z)
            temp[i]=temp[i].slice(0,y)+"<span style='background-color:#ffbd61ba'>"+temp[i].slice(y,z)+"</span>"+temp[i].slice(z,)
        }
        if(temp[i].startsWith("Cisco-Guid")==1)
        {
            //console.log(temp[i])
            //temp[i]="<span style='background-color:#7bff61ba'>"+temp[i]+"</span>"
            //y=temp[i].indexOf("Cisco-Guid")
            //z=temp[i].indexOf(" ",y)
            //console.log(y,z)
            temp[i]="<span style='background-color:#ffbd61ba'>"+temp[i]+"</span>"
        }
        if(temp[i].indexOf("callguid")>-1)
        {
            //console.log(temp[i])
            //temp[i]="<span style='background-color:#7bff61ba'>"+temp[i]+"</span>"
            y=temp[i].indexOf("callguid")
            z=temp[i].indexOf(" ",y)
            console.log(y,z)
            temp[i]=temp[i].slice(0,y)+"<span style='background-color:#ffbd61ba'>"+temp[i].slice(y,z)+"</span>"+temp[i].slice(z,)
        }
        if(temp[i].indexOf("DialogID")>-1)
        {
            //console.log(temp[i])
            //temp[i]="<span style='background-color:#7bff61ba'>"+temp[i]+"</span>"
            y=temp[i].indexOf("DialogID")
            z=temp[i].indexOf(" ",y)
            console.log(y,z)
            temp[i]=temp[i].slice(0,y)+"<span style='background-color:#b061ffba'>"+temp[i].slice(y,z)+"</span>"+temp[i].slice(z,)
        }
        if(temp[i].startsWith("Call-ID:")==1)
        {
            //console.log(temp[i])
            temp[i]="<span style='background-color:#55ebff'>"+temp[i]+"</span>"
        }
        if(temp[i].startsWith("Sent:")==1 || temp[i].startsWith("Received:")==1 )
        {
            //console.log(temp[i])
            temp[i+1]="<span style='background-color:#ffcf55'>"+temp[i+1]+"</span>"
        }
    }
    temp=temp.join("\n")
    temp= temp.replace(/(?:\r\n|\r|\n)/g, '<br>')
    //.log(temp)
     
            msg=temp.replace(/(?:\r\n|\r|\n)/g, '<br>')
            openModal("modal-small",msg)
            //document.getElementById("msg").textContent = msg
        }
    });
}