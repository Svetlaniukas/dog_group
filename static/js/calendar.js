document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: '/users/get-events/',
        dateClick: function(info) {
            $('#addEventModal').modal('show');
            $('#eventStart').val(info.dateStr);
        },
        eventClick: function(info) {
            $('#editEventModal').modal('show');
            $('#editEventId').val(info.event.id);
            $('#editEventTitle').val(info.event.title);
            $('#editEventStart').val(info.event.startStr.split('T')[0]);
            $('#editEventEnd').val(info.event.endStr ? info.event.endStr.split('T')[0] : '');
            $('#editEventLocation').val(info.event.extendedProps.location);
            $('#editEventDescription').val(info.event.extendedProps.description);
        }
    });

    calendar.render();

    $('#editEventForm').on('submit', function(event) {
        event.preventDefault();
        const eventId = $('#editEventId').val();
        $.ajax({
            url: `/users/update-event/${eventId}/`,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: JSON.stringify({
                title: $('#editEventTitle').val(),
                start_date: $('#editEventStart').val(),
                end_date: $('#editEventEnd').val(),
                location: $('#editEventLocation').val(),
                description: $('#editEventDescription').val()
            }),
            contentType: 'application/json',
            success: function(response) {
                if (response.success) {
                    calendar.refetchEvents();
                    $('#editEventModal').modal('hide');
                } else {
                    console.error('Failed to update event');
                }
            },
            error: function(xhr, status, error) {
                console.error('Error updating event:', error);
            }
        });
    });

    $('#deleteEventBtn').on('click', function() {
        const eventId = $('#editEventId').val();
        $.ajax({
            url: `/users/delete-event/${eventId}/`,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(response) {
                if (response.success) {
                    calendar.refetchEvents();
                    $('#editEventModal').modal('hide');
                } else {
                    console.error('Failed to delete event');
                }
            },
            error: function(xhr, status, error) {
                console.error('Error deleting event:', error);
            }
        });
    });
});
