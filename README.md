# Photo Selector

Photo Selector is a Python-based graphical user interface (GUI) application that allows users to browse, select, and perform actions on images from a chosen directory. This application is built using Tkinter and PIL (Pillow) libraries.

<img width="1912" alt="Screenshot 2024-07-11 at 11 52 54 PM" src="https://github.com/ammababoi/PhotoSelector/assets/81505149/c2cb58be-6799-43fb-ae65-61e3a9c3550d">

![photoselector](https://github.com/ammababoi/PhotoSelector/assets/81505149/54609c3c-1755-4c22-a152-d3a09de22e7c)


## Features

- Browse through images in a selected directory.
- Select or deselect images for further actions.
- Navigate through images using Next and Previous buttons or keyboard arrows.
- Display the name of the current image.
- Perform actions on selected images such as printing their names, copying to another directory, or moving to another directory.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/photoselector.git
    cd photoselector
    ```

## Usage

1. Run the application:
    ```bash
    python3 photoselector.py
    ```

2. Use the file dialog to select the directory containing the images you want to browse.

3. Use the `Next` and `Previous` buttons (or the left and right arrow keys) to navigate through the images.

4. Click `Select` to mark an image for selection. The button will turn green and the text will change to "Selected". Click again to deselect.

5. When you're done selecting images, click the `Finish` button to open the Finish Options window.

6. In the Finish Options window, choose the actions you want to perform on the selected images:
    - Print the names of the selected images.
    - Copy the selected images to another directory.
    - Move the selected images to another directory.

7. Click `Apply` to perform the selected actions.

## Keyboard Shortcuts

| Key        | Function                       |
|------------|--------------------------------|
| Left Arrow | Navigate to the previous image |
| Right Arrow| Navigate to the next image     |
| Space      | Toggle selection of image      |
| Enter      | Open Finish Options window     |

## Dependencies

- Python 3.x
- Tkinter (included with Python)
- Pillow

