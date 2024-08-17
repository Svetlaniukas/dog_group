
# Dog Walking Exchange https://dog-group.onrender.com/

**Dog Walking Exchange** is a web application designed to connect dog owners in Dublin, facilitating the process of finding walking partners, sharing dog walking tips, and accessing resources for dog training and parks in the area.

## Overview

This application provides various features to enhance the dog walking experience for users by allowing them to create profiles, post offers for walking partners, share information through posts, and communicate via messages.

## Features

- **User Registration and Authentication:** Users can sign up, log in, and manage their sessions securely.
- **User Profile Management:** View and update profiles, upload profile pictures, and update personal information.
- **Creating and Viewing Dog Walking Offers:** Users can create offers for dog walking, which are displayed on the homepage.
- **Creating and Viewing Posts:** Users can share posts with images and interact through comments and emoji ratings.
- **Post Management:** Users can edit or delete their own posts.
- **Sending and Receiving Messages:** Private messaging system for user communication.
- **Sent and Archived Messages:** Users can view sent messages and archive messages to keep the inbox organized. Archived messages can also be unarchived.
- **Interactive Homepage:** Homepage displays offers, posts, and includes resources like dog walking tips and park suggestions.
- **Post Interaction:** Users can comment on and rate posts with emojis.
- **Participation System:** Track users who join specific dog walking offers.
- **UI Enhancements:** Responsive design using Bootstrap, with custom CSS for a modern look.
- **Security Improvements:** CSRF protection, secured pages for logged-in users only.
- **Database Migrations:** Proper handling of database changes to support new features.
- **Error Handling and Debugging:** Addressed runtime errors and ensured proper URL configurations.
- **Legal Pages:** Terms of Service and Privacy Policy pages.

## CRUD Functionality

### Create

- **Offers:** Users can create offers through a form, specifying details like title, description, location, and time.
- **Posts:** Users can create posts with content and images.
- **Messages:** Users can send messages to other users from their profile or inbox.

### Read

- **Homepage:** Displays all available offers and posts.
- **Messages:** Users can read active, sent, and archived messages in their inbox.

### Update

- **Edit Offers and Posts:** Users can edit their own content with pre-filled forms for easy updating.
- **Unarchive Messages:** Users can move messages back to the inbox from the archive.

### Delete

- **Deleting Offers and Posts:** Users can delete their content with confirmation prompts.
- **Archiving Messages:** Move messages to the archive instead of deleting them.

## Hosting

The project is successfully hosted on Render. The database is configured and connected using PostgreSQL, storing the application data securely.

## Development Strategy

### Phases

- **Phase 1 - Setting up the Django environment:** Initial setup of the Django framework, including environment configuration and dependency installation.
- **Phase 2 - Designing the database schema:** Planning and implementing the database schema using PostgreSQL to handle users, offers, posts, messages, and events.
- **Phase 3 - Building core backend functionalities:** Implementing the essential backend features like user management, offer creation, and messaging systems.
- **Phase 4 - Crafting the frontend:** Developing the frontend using HTML templates, enhancing the design with Bootstrap, and integrating JavaScript for interactive functionalities.
- **Phase 5 - Rigorous testing:** Conducting extensive testing for functionality, responsiveness, and security to ensure the application performs as expected.
- **Phase 6 - Deploying the application on Render:** Final deployment of the application, including database migration and securing the environment.

## Security Features

The project implements several security measures to protect user data and ensure secure operations:

- **Password Encryption:** All user passwords are encrypted before storage to prevent unauthorized access.
- **Role-Based Access Control:** User roles and permissions are enforced to restrict access to specific features based on user roles.
- **CSRF Protection:** Cross-Site Request Forgery (CSRF) protection is enabled throughout the application to prevent unauthorized actions.
- **Secure Communication:** Secure connections and data handling are ensured across the platform.

## JavaScript Script

```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Calendar
    var calendarEl = document.getElementById('calendar');
    var csrfToken = '{{ csrf_token }}';

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: '/users/get-events/',
        eventDidMount: function(info) {
            var createdBy = info.event.extendedProps.created_by;
            if (createdBy) {
                var avatarHtml = createdBy.avatar ? `<img src="${createdBy.avatar}" class="avatar" alt="${createdBy.username}" style="width: 20px; height: 20px; border-radius: 50%; margin-right: 5px;">` : '';
                var usernameHtml = `<span>${createdBy.username}</span>`;
                var eventContent = info.el.querySelector('.fc-event-title');
                if (eventContent) {
                    eventContent.innerHTML = avatarHtml + usernameHtml + ' - ' + eventContent.innerHTML;
                }
            }
        },
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

    $('#addEventForm').on('submit', function(event) {
        event.preventDefault();

        const startDate = $('#eventStart').val();
        const endDate = $('#eventEnd').val();

        if (!startDate.match(/^\d{4}-\d{2}-\d{2}$/)) {
            console.error('Invalid start date format. Expected format: YYYY-MM-DD');
            return;
        }

        if (endDate && !endDate.match(/^\d{4}-\d{2}-\d{2}$/)) {
            console.error('Invalid end date format. Expected format: YYYY-MM-DD');
            return;
        }

        $.ajax({
            url: '/users/add-event/',
            type: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: JSON.stringify({
                title: $('#eventTitle').val(),
                start_date: startDate,
                end_date: endDate,
                location: $('#eventLocation').val(),
                description: $('#eventDescription').val()
            }),
            contentType: 'application/json',
            success: function(response) {
                if (response.success) {
                    calendar.refetchEvents();
                    $('#addEventModal').modal('hide');
                    $('#addEventForm')[0].reset();
                } else {
                    console.error('Failed to add event:', response.error);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error adding event:', error);
            }
        });
    });

    $('#editEventForm').on('submit', function(event) {
        event.preventDefault();
        const eventId = $('#editEventId').val();

        const startDate = $('#editEventStart').val();
        const endDate = $('#editEventEnd').val();

        if (!startDate.match(/^\d{4}-\d{2}-\d{2}$/)) {
            console.error('Invalid start date format. Expected format: YYYY-MM-DD');
            return;
        }

        if (endDate && !endDate.match(/^\d{4}-\d{2}-\d{2}$/)) {
            console.error('Invalid end date format. Expected format: YYYY-MM-DD');
            return;
        }

        $.ajax({
            url: `/users/update-event/${eventId}/`,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: JSON.stringify({
                title: $('#editEventTitle').val(),
                start_date: startDate,
                end_date: endDate,
                location: $('#editEventLocation').val(),
                description: $('#editEventDescription').val()
            }),
            contentType: 'application/json',
            success: function(response) {
                if (response.success) {
                    calendar.refetchEvents();
                    $('#editEventModal').modal('hide');
                } else {
                    console.error('Failed to update event:', response.error);
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
                    console.error('Failed to delete event:', response.error);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error deleting event:', error);
            }
        });
    });

    // Handle emoji ratings
    document.querySelectorAll('.emoji-button').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const postId = this.getAttribute('data-post-id');
            const emoji = this.getAttribute('data-emoji');
            const csrfToken = '{{ csrf_token }}';

            fetch(`{% url 'add_rating' 0 %}`.replace('0', postId), {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `emoji=${emoji}`,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update emoji counts
                    const emojiCountsDiv = document.getElementById(`emoji-counts-${postId}`);
                    emojiCountsDiv.innerHTML = `
                        😊: ${data.emoji_counts.😊} |
                        😢: ${data.emoji_counts.😢} |
                        😡: ${data.emoji_counts.😡}
                    `;
                } else {
                    console.error('Failed to add rating');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Handle comment toggling
    document.querySelectorAll('.toggle-comments').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            const commentsSection = document.getElementById(`comments-${postId}`);

            if (commentsSection.style.display === 'none' || commentsSection.style.display === '') {
                commentsSection.style.display = 'block';
                this.textContent = 'Hide Comments';
            } else {
                commentsSection.style.display = 'none';
                this.textContent = 'Show Comments';
            }
        });
    });
});


## Project Structure

```plaintext
dog_walking_exchange/
│
├── dog_walking_exchange/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── users/
│   ├── migrations/
│   ├── templates/
│   │   └── users/
│   │       ├── create_offer.html
│   │       ├── create_post.html
│   │       ├── edit_post.html
│   │       ├── edit_offer.html
│   │       ├── send_message.html
│   │       ├── inbox.html
│   │       ├── archived_messages.html
│   │       ├── login.html  
│   │       └── register.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── terms.html
│   ├── privacy.html
│   └── registration/
│       ├── login.html
│       ├── logged_out.html  
│
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── img/
│   │   ├── dog_training_1.jpg
│   │   ├── dog_training_2.jpg
│   │   └── dog_training_3.jpg
│   └── js/
│       └── main.js
│
└── manage.py


## Technologies Used

- **Backend**: Django 5.0.7
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: PostgreSQL

## Installation

To run this project locally, follow these steps:

### Prerequisites

- Python 3.11
- Virtualenv (optional, but recommended)
- pip install -r requirements.txt
- PostgreSQL

### Setup

1. **Clone the repository:**
bash
   git clone https://github.com/Svetlaniukas/dog_group
   cd dog_walking_exchange# dog_group

   cd dog_walking_exchange# dog_group
