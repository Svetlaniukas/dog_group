
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
