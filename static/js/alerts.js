function system_alerts() {
    $.ajax({
        url: `/system-alerts`,
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