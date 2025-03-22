# Simple File Transfer Application

A simple drag & drop file transfer app with a modern UI and basic secure authentication, designed for Raspberry Pi 5.

## Features

- Drag & drop file upload
- List and download uploaded files
- Secure login using Flask session
- Modern interface with Bootstrap

## Installation

1. Clone the repository.
2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install flask werkzeug
   ```
3. Run the application:
   ```bash
   python app.py
   ```

## Usage

- Access the app at [http://0.0.0.0:4242](http://0.0.0.0:4242).
- Log in with the default credentials (`admin` / `admin123`).
- Drag & drop files to upload.

> You'll have to open your 4242 port on your router to access the app outside your home.

## Note

For production, update credentials and secure the secret key.