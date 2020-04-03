var username=sessionStorage.getItem("session")
document.getElementById("welcome").innerHTML="Hi ,"+username+` <img src="https://image.flaticon.com/icons/svg/1738/1738691.svg" width="40" height="40" class="rounded-circle ml-2 mr-2">
    `+`<i class="fa fa-2x fa-sign-out" aria-hidden="true" title="Sign Out" onclick="logout()" style="cursor:pointer;position:relative;top:0.2rem;color:#0b519b"></i>`

function logout()
{
    sessionStorage.removeItem("session")
    $.ajax({
        type: 'GET',
        url: `/clearSession`,
        success: function(data){
            //window.alert(`${username} session set`)
            //initial()
            location.href="/"
        }
    })
    
}


$.ajax({
    type: 'GET',
    url: '/files',

    contentType: false,
    cache: false,
    processData: false,
    success: function (data) {
        if(data.length>0)
        {
           document.getElementById("details-link").setAttribute("href","call-summary?filename="+data[0][0])
        }
    }
})
