# Simple Django Chat App

## Requirements

- Python

## Get Started

- Create Virtual environment

  ```powershell
  python -m venv env
  ```

- Activate Virtual Environment

  ```powershell
  .\env\Scripts\activate
  ```

- Install Requirements

  ```powershell
  pip install -r requirements.txt
  ```

- Start Live Server

  - Navigate to Django Project Folder

  ```powershell
  cd django_chat_app
  ```

  - Migrate

  ```powershell
  python manage.py migrate
  ```

  - Run Server

  ```powershell
  python manage.py runserver
  ```

## Issues

Create unit Tests

Create ERM
<https://www.diagrammeditor.de/>

Backend

- Poor Exceptions handling for all Requests.
  login_chat
  register_chat
  chat

FrontEnd

- Material Design Lite
Required input fields should not be marked invalid (red) automatically.
<https://github.com/google/material-design-lite/issues/1502>

## Login View

- Backend
    Give detail Feedback:
        if user does not exist
        ( for this there should not be possible to create an user with the same email address at least)
        else credentials are wrong
    Password reset possibilities
- Frontend
     Password reset possibilities

## Register View

- Backend
    Guard against creating multiple accounts with at least the same email address.

## Index View

- Backend and Frontend
- New Message Date Format does not have the same format on post as on loading
