# AI Surveillance with Face Recognition and Telegram Bot Alert

## Overview
This project is designed to provide an AI surveillance system that uses face recognition and alerts through Telegram bot. The system works by comparing faces detected in the camera stream to a list of authorized individuals in the guest list folder. If an unknown face is detected, an alert is sent to a designated Telegram bot.

## Getting Started
1. cd into the project folder and do "python -m venv venv" to create venv
2. on mac/linux do "source venv/bin/activate" on windows do "venv\Scripts\activate.bat" 
2. Install the required packages listed in `requirements.txt` using pip: "pip install -r requirements.txt"
3. Create `guest_list` and add Add authorized individuals' images to the `guest_list` folder.
4. copy the .env_example and rename it to .env.
5. Add the required information to the `.env` file (e.g., Telegram bot API key, camera information, etc.).
6. Run `surveillance2.py` using Python: "python surveillance2.py"


## Usage
The system can be used for security and surveillance purposes, such as monitoring entrances or exits of a building or a specific area. The system can be customized to fit specific needs by modifying the parameters in the `.env` file.

## Credits
This project was developed as part of group's project.

## License

# ai-surveillance
