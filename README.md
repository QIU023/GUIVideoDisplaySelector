
# Video Selector GUI

A simple Tkinter-based GUI application for video comparison and selection.

## Description

This application allows users to compare videos from two different folders side by side. Each folder should have matching filenames. The GUI provides an interface for users to play each video, choose between them, navigate through the video pairs, and finally export their choices.

## Features

- **Navigation**: Navigate through video pairs using "Prev Task" and "Next Task" buttons.
- **Video Playback**: Play videos in an external player.
- **Selection**: Choose the preferred video from each pair.
- **Export**: Export the selection results to a text file and quit the application.
- **View Pane**: View all selections and jump to a specific video pair.

## Usage

1. Ensure you have all the necessary dependencies installed:
    - Python 3.9.1 64 bits
    - PIL (Pillow)
    - VLC 3.0.16 win64
    - Tkinter (usually comes with Python installations)

2. Clone this repository:

    ```bash
    git clone https://github.com/QIU023/GUIVideoDisplaySelector.git
    cd GUIVideoDisplaySelector
    ```

3. Run the script:

    ```bash
    python guiVideoSelector.py
    ```

4. Follow the on-screen instructions to load videos, make your selections, and save your choices.

## Contributing

Feel free to fork this repository, make your changes, and submit pull requests. For major changes, please open an issue first to discuss the change.

## License

This project is licensed under the MIT License.
