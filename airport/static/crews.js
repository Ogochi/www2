function displayList() {
    let date = $('#dateInput').val();
    $('#crew_list').empty();

    $.ajax({
        url: '/api/get_crews/',
        type: 'get',
        data: {
            day: date.slice(8, 10),
            month: date.slice(5, 7),
            year: date.slice(0, 4),
        },
        success: res => {
            res['crews'].forEach(x =>
                $('#crew_list').append(
                    $('<tr><td>' + x.flightId + '</td><td>' + x.crew + '</td></tr>')
                )
            );
        },
        error: () => {
            console.log("Couldn't display crews and flights list!");
        },
    });
}

function assignCrew() {
    let flight = $('#flight_select').val().split(" ")[1];
    let crew = $('#crew_select').val().split(" ");

    $.post('/api/change_flight_crew/', {
        flightId: flight,
        captainsName: crew[0],
        captainsSurname: crew[1],
        username: window.localStorage.getItem("username"),
        password: window.localStorage.getItem("password"),
    }, res => {
        $('#alerts').empty().append(
            $('<div class="alert alert-success text-center" role="alert">\n' +
                'You\'ve successfully assigned crew!\n' +
                '</div>')
        );
    }).fail((err) => {
        $('#alerts').empty().append(
            $('<div id="error_alert" class="alert alert-danger text-center" role="alert">\n' +
                'Error - couldn\'t assign crew! You have to be logged in!\n' +
                '</div>')
        );
    });
}

function fillSelectInputs() {
    $.get('/api/get_flights_and_crews/', res => {
        res['flights'].forEach(flight =>
            $('#flight_select').append(
                $('<option id="flight_option' + flight.id + '">id: ' + flight.id + " | " +
                    flight.startTime.slice(0, 10) + " " +
                    flight.startTime.slice(11, 19) + " " +flight.startAirport + " -> " +
                    flight.endTime.slice(0, 10) + " " + flight.endTime.slice(11, 19) + " " +
                    flight.endAirport + '</option>')
            )
        );
        res['crews'].forEach(crew =>
            $('#crew_select').append(
                $('<option>' + crew.name + '</option>')
            )
        );
    }).fail(() => {
        console.log("Couldn't get flights and crews!");
    });
}

function login(showAlert) {
    $.post('/api/login/', {
        username: window.localStorage.getItem("username"),
        password: window.localStorage.getItem("password"),
    }, () => {
        if (showAlert) {
            $('#alerts').empty().append(
                $('<div class="alert alert-success text-center" role="alert">\n' +
                    'You\'ve successfully logged in!\n' +
                    '</div>')
            );
        }
        $('#hello').append(`Hello, ${window.localStorage.getItem("username")}.`);
        $('#logged_in').css("display", "");
        $('#login_form').css("display", "none");
    }).fail(() => {
        if (showAlert) {
            $('#alerts').empty().append(
                $('<div class="alert alert-danger text-center" role="alert">\n' +
                    'Log in error, check if username and password are correct!\n' +
                    '</div>')
            );
        }
    });
}

$().ready(() => {
    login(false);
    fillSelectInputs();
    $('#search_crews').click(displayList);
    $('#change_crew_assignment').click(assignCrew);
    $('#login_button').click(() => {
        window.localStorage.setItem("username", $('#login_username').val());
        window.localStorage.setItem("password", $('#login_password').val());
        login(true);
    });
    $('#logout_button').click(() => {
        window.localStorage.removeItem("username");
        window.localStorage.removeItem("password");
        $('#alerts').empty().append(
                $('<div class="alert alert-success text-center" role="alert">\n' +
                    'You\'ve successfully logged out!\n' +
                    '</div>')
            );
        $('#logged_in').css("display", "none");
        $('#login_form').css("display", "");
    })
});