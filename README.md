# Project Overview

This project is a backend application designed to handle video processing, chat functionalities, and WebRTC communications. It is structured to facilitate modular development, with separate modules for different functionalities.

## Directory Structure

```
backend/
├── src/
│   ├── main.py
│   └── utils/
│       └── __init__.py
├── requirements.txt
└── README.md
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To run the application, execute the following command:

```bash
python src/main.py
```

## Modules

- **main.py**: Entry point of the application, initializes the app and sets up API routes.
- **api/**: Contains modules for video processing, chat functionalities, and WebRTC services.
  - **video.py**: Handles video processing tasks.
  - **companions.py**: Manages companion features.
  - **webrtc.py**: Manages WebRTC functionalities.
  - **chat.py**: Manages chat functionalities.
- **ws/**: Contains signaling for WebSocket communication.
  - **signaling.py**: Implements WebSocket signaling.
- **models/**: Contains data models used throughout the application.
- **utils/**: Contains utility functions and classes.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.