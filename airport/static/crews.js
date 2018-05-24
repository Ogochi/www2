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
    }, res => {
        $('#alerts').empty().append(
            $('<div class="alert alert-success text-center" role="alert">\n' +
                'You\'ve successfully assigned crew!\n' +
                '</div>')
        );
    }).fail((err) => {
        $('#alerts').empty().append(
            $('<div class="alert alert-danger text-center" role="alert">\n' +
                'Error - couldn\'t assign crew!\n' +
                '</div>')
        );
    });
}

function fillSelectInputs() {
    $.get('/api/get_flights_and_crews/', res => {
        res['flights'].forEach(flight =>
            $('#flight_select').append(
                $('<option>' + "id: " + flight.id + " | " + flight.startTime.slice(0, 10) + " " +
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

// function displayMessage(message) {
//     $('#chat > ul').append(
//         $('<li>' + message + '</li>')
//     );
//     $("#chat").scrollTop($('#chat > ul').height());
// }
//
// function displayChat(messages) {
//     $('#chat > ul').empty();
//     for (var i in messages) {
//         displayMessage(messages[i].user__username + ': ' + messages[i].content);
//     }
// }
//
// function getAndDisplayChat() {
//     $.get('/ajax/get_chat/', function(res) {
//         console.log('chat messages received');
//         displayChat(res.chat);
//     }).fail(function() {
//         console.log('retrieving chat messages failed');
//     });
// }

$().ready(function() {
    fillSelectInputs();
    $('#search_crews').click(displayList);
    $('#change_crew_assignment').click(assignCrew)
    // getAndDisplayChat();
    //
    // setInterval(getAndDisplayChat, 3000);
    //
    // $('#send-button').click(function() {
    //     $.post('/ajax/send_chat_message/', {
    //         'message': $('#message-form input').val(),
    //     }, function() {
    //         console.log('chat message sent');
    //         getAndDisplayChat();
    //     }).fail(function() {
    //         console.log('sending chat message failed');
    //     });
    // });
});