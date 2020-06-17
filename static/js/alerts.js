function system_alerts() {
    var list = []
    $.ajax({
        url: '/get-system-alerts',
        type: 'GET',

        success: function (data) {
            for (var i = 0; i < data.length; i++) {
                list[i] = []
                list[i] = [data[i][0], data[i][1], data[i][2], data[i][3], `<div class='btn-group' role='group' aria-label='Basic example'><i class='fa fa-minus-circle fa-2x' style='color:#dc3545;margin-left:5px;cursor:pointer' title='Remove' aria-hidden='true' onclick='del(${i})'></i></div>`]
            }

            $('#system_alerts').DataTable(
                {
                    scrollY: '50vh',
                    scrollCollapse: true,
                    data: list,
                    columns: [
                        { title: "Alert Name" },
                        { title: "Description" },
                        { title: "Type" },
                        { title: "Alert Matches" },
                    ],
                });
        }

    });

}

function feature_alerts() {
    var list = []
    $.ajax({
        url: '/get-feature-alerts',
        type: 'GET',

        success: function (data) {
            for (var i = 0; i < data.length; i++) {
                list[i] = []
                list[i] = [data[i][0], data[i][1], data[i][2], data[i][3]]
            }

            $('#feature_alerts').DataTable(
                {
                    scrollY: '50vh',
                    scrollCollapse: true,
                    data: list,
                    columns: [
                        { title: "Alert Name" },
                        { title: "Description" },
                        { title: "Type" },
                        { title: "Alert Matches" },
                    ],
                });
        }

    });

}