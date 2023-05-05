# AI Surveillance with Face Recognition and Telegram Bot Alert

## Overview
This project is designed to provide an AI surveillance system that uses face recognition and alerts through Telegram bot. The system works by comparing faces detected in the camera stream to a list of authorized individuals in the guest list folder. If an unknown face is detected, an alert is sent to a designated Telegram bot.

## Getting Started
1. Install the required packages listed in `requirements.txt` using pip:
2. Add authorized individuals' images to the `guestlist` folder.
3.copy the .env_example and rename it to .env .
4. Add the required information to the `.env` file (e.g., Telegram bot API key, camera information, etc.).
5. Run `main.py` using Python 3:


## Usage
The system can be used for security and surveillance purposes, such as monitoring entrances or exits of a building or a specific area. The system can be customized to fit specific needs by modifying the parameters in the `.env` file.

## Credits
This project was developed by [Your Name] as part of [Your Organization]'s project.

## License
This project is licensed under the [License Name] license.
