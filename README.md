# SmartParker

SmartParker is a web application designed to facilitate efficient parking and reduced fuel consumption during the process. It also provides parking spot rental and management. It allows users to rent out their parking spots and enables others to book those spots for specified durations. The project is built using Django, a high-level Python web framework.

## Features

- User Authentication: Users can sign up, log in, and activate their accounts via email confirmation.
- Parking Spot Management: Users can register their parking spots, providing details such as location, pricing, and availability.
- Booking System: Registered users can book available parking spots for specified durations.
- Payment Integration: Integration with a payment system to handle transactions for parking spot bookings.
- Reporting System: Users can report issues related to parking spots, such as damage or maintenance needs.

## Installation

To run the SmartParker application locally, follow these steps:

1. Clone the repository: `git clone https://github.com/your_username/smartparker.git`
2. Navigate to the project directory: `cd smartparker`
3. Install dependencies: `pip install -r requirements.txt`
4. Configure the database settings in `settings.py`.
5. Apply database migrations: `python manage.py migrate`
6. Start the development server: `python manage.py runserver`
7. Access SmartParker at `http://localhost:8000` in your web browser.


# Usage

1. As a User:
   - Register or log in to your account.
   - Search for available parking spaces based on your requirements.
   - Select a suitable parking space and make a booking.
   - Complete the payment process securely.
   - Receive confirmation and details of your booking.

2. As a Parking Space Owner:
   - Register or log in to your account.
   - List your parking spaces with relevant details.
   - Manage bookings, update availability, and track occupancy.
   - Receive notifications for new bookings and updates.

## Technologies Used

- Django: Web framework for backend development.
- HTML/CSS/JavaScript: Frontend development.
- MySQL: Database management system.
- Bootstrap: Frontend framework for responsive design.
- Payment Gateway Integration (e.g., Stripe): Secure payment processing.
- MapboxAPI: Integration for location-based services.
