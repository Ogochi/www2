function displayList() {
    let date = $('#dateInput').val();

    $.ajax({
        url: '/api/get_crews/',
        type: 'get',
        data: {
            day: date.slice(8, 10),
            month: date.slice(5, 7),
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
    let flight = $('#flight_select').val();
    let crew = $('#crew_select').val().split(" ");

    $.post('/api/change_flight_crew/', {
        flightId: flight,
        captainsName: crew[0],
        captainsSurname: crew[1],
    }, res => {
        console.log(res);
    }).fail((err) => {
        //console.log(err);
        console.log("Couldn't assign crew!");
    });
}

function fillSelectInputs() {
    $.get('/api/get_flights_and_crews/', res => {
        res['flights'].forEach(flight =>
            $('#flight_select').append(
                $('<option>' + "id: " + flight.id + ", " +
                    flight.startAirport + "-" + flight.endAirport + ", " +
                    flight.startTime.slice(0, 10) + " -> " + flight.endTime.slice(0, 10) + '</option>')
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