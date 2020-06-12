var username = sessionStorage.getItem("session")
document.getElementById("welcome").innerHTML = username;
document.getElementById("log").innerHTML = `<i class="fa fa-2x fa-sign-out" aria-hidden="true" title="Sign Out" onclick="logout()" style="cursor:pointer;position:relative;top:0.2rem;color:#0b519b"></i>`

function logout() {
    sessionStorage.removeItem("session")
    $.ajax({
        type: 'GET',
        url: `/clearSession`,
        success: function (data) {
            //window.alert(`${username} session set`)
            //initial()
            location.href = "/"
        }
    })

}


(function ($) {

    "use strict";

    var fullHeight = function () {

        $('.js-fullheight').css('height', $(window).height());
        $(window).resize(function () {
            $('.js-fullheight').css('height', $(window).height());
        });

    };
    fullHeight();

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });

})(jQuery);
