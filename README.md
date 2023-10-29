# Streamlining Business Verification with Smile ID and Django REST: A Celery-Powered Solution

![Smile ID Logo](https://cdn-images-1.medium.com/max/800/1*R4IgNzc_GRen02OFeo-tuw.png)

## Overview

This project demonstrates how to integrate Smile ID's Business Verification with Django REST, powered by Celery, for streamlined business verification processes. It's designed to ensure a responsive application while performing robust verifications.

## Features

- Seamless integration of Smile ID Business Verification
- Asynchronous job scheduling using Celery
- Effortless KYB (Know Your Business) verification process
- Error handling and retries for robustness
- Integration with Django REST framework

## Technologies Used

- Django
- Celery
- Smile ID API
- Python
- Redis (message broker)
- REST API (Django REST framework)

## Get Started

1. Clone this repository.
2. Configure your Django project and set up Celery.
3. Install the required libraries, including the Smile ID Python library.
4. Implement the provided Django models and serializers.
5. Create the BusinessKYBView to initiate the KYB process.
6. Utilize the Celery task `handle_kyb_task` to submit and track verification jobs.

## Contribution

I welcome contributions and suggestions to make the Kenyan Weather App even better. If you have ideas, bug reports, or feature requests, feel free to open an issue or submit a pull request.
For detailed implementation and usage, check the full article on Medium.

## Author

- aibunny
- Blog: [Medium Blog](https://medium.com/@aibunny/streamlining-business-verification-with-smile-id-and-django-rest-a-celery-powered-solution-340bdc96d998)
