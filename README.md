# VidFeedback - Video Testimonial Platform

VidFeedback is a Django-based platform that helps businesses collect, manage, and showcase video testimonials from their customers.

## Features

- 🎥 Easy video testimonial collection
- 👤 Multi-step user registration
- 💼 Business dashboard
- 📊 Plan-based limitations
- 🔄 Google My Business integration (coming soon)
- 📱 Responsive design

## Tech Stack

- Python 3.10
- Django 5.1
- Bootstrap 5
- SQLite (Development)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rakeshptajlapur/vidfeedback_django.git
cd vidfeedback_django
```

2. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Run development server:
```bash
python manage.py runserver
```

## Project Structure

```
VidFeedback/
├── accounts/            # User authentication and profiles
├── feedback/           # Video testimonial functionality
├── integrations/      # Third-party integrations
├── templates/         # HTML templates
├── static/           # Static files (CSS, JS)
└── veedfeedback/    # Project settings
```

## Plans and Pricing

- Free: 1 form, 10 submissions
- Basic: 5 forms, 100 submissions
- Pro: Unlimited forms & submissions

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.