# User Manual

The code was developed to guide a standard commercial telescope mount through a ST-4 port to follow the Moon using a Raspberry Pi (4B), a camera, and a relay board. The system should work with any version of Raspberry Pi running Raspberry Pi OS as long as the other components are compatible. Due to computing demand, a version 4 or higher is recommended.

The relay card can be any 4 channel relay card compatible with the Raspberry Pi. For this project, an opto-isolator relay card was used, but other relays will also work. Any camera compatible with the Raspberry Pi will work as long as the video stream can be called with Picam2. To achieve reasonable precision, the sensor and lens should provide for a sufficient resolution of the Moon. At least 100 pixels per Moon diameter are recommended. The other components can be chosen freely.

For the original project, these components were used:

- Raspberry Pi 4B
- Raspberry Pi High Quality Camera (C-Mount)
- *sertronics* 50mm Lens (C-Mount)
- *sertronics* RELM-4 4 Channel Relay Module
- *waveshare* 3.5 inch RPi LCD (A) Display
- *Innomaker* aluminium case
- Steel Button
- GPIO extension
- Dupont connector cables
- Standard RJ12 cable
- Standard camera screws

## Installation

On your Raspberry Pi running Raspberry Pi OS, do an update/upgrade and install the latest version of git (if not installed already):

```
sudo apt install git
```

Then get the MoonGuider repo from GitHub:

```
git clone https://github.com/tobiasKurz1/MoonGuider.git
```

Navigate to the download folder and use the requirements file to install the necessary libraries:

```
cd MoonGuider
pip3 install -r requirements.txt
```

Adjust the configuration parameters by editing the `config.ini`:

```
nano config.ini
```

The program can be run by executing the main file:

```
python3 main.py
```

## Usage

The system is designed to be easy to use and self-explanatory. Also, the code is modular and comprehensive to allow for changes and adjustments to changing circumstances.

Use the `config.ini` to configure the system with different parameters. The configuration file includes settings for the Moon phases full, half, and new Moon, but custom profiles can be added. The parameters are explained at the top of the file.

The most important parameters for first launch include `pin_ra_down`, `pin_ra_up`, `pin_dec_down`, `pin_dec_up`, `pin_button` (depending on the wiring), as well as `image_height` and `image_width` (depending on the camera resolution). The pins may need to be adjusted based on the specific wiring. The numbers can be looked up in the Raspberry Pi documentation. When starting up and closing, a keyboard is required. While the program is running, it can be controlled via the button only.

For additional functionality of the code `show_cam_feed`, `do_relay_test`, and `export_to_excel` can be toggled on or off.

### Running the Code

When the main file is executed, the `config.ini` is read. The user must then select a profile using the keyboard (if only one profile is present, it will be selected automatically). Next, the clicking of each relay should be heard. If there are fewer than four on and off clicks, the relay board is not working correctly. After that, the above-mentioned functions for camera setup and testing are executed if activated.

Log files can be visualized using the included `plotter.py`, which outputs an image to the `/Logs` folder.

## Troubleshooting

Custom hardware other than the parts listed above can be used for this system. Here are some configuration changes and considerations which need to be made when running the code with a change in the respective component:

### Computing Unit

A lower computing power may lead to very slow response times and low frame rates. To compensate for this, parameters like `image_buffer` and `in_scale` can be set to lower values. It may also help to raise `dp`. However, all of these changes may impact guiding precision.

### Switching Unit

In the original system, the inactive relay position is `GPIO.HIGH`. If this is not the case, the `HIGH` and `LOW` may need to be switched in the code inside `relay_handling.py`. In the case of standard three-way relays, the order of the wiring can also be changed to accomplish the same result without changing the code. Pins used for the connection of the relay board need to be specified in `config.ini`.

### Camera

Adjust image width and height in `config.ini`. Change in resolution results in changed computing power requirements. Adjust these parameters to fit for your system. Also, `margin` and `pulse_multiplier` may be adjusted since they are dependent on the deviation in pixels. Depending on how the camera is oriented on the telescope mount, adjust `rotate` in the configurations.

### Lens

Different lenses lead to changes in Moon size on the sensor. Therefore, `margin` and `pulse_multiplier` may need to be adjusted.

### Display

Different screen sizes are usually not a problem as long as they are seamlessly integrated into the OS. Displays which require python libraries to be operated will need to be custom coded in `calc.py`. To improve image quality on higher resolution displays increase `out_scale`.

### Mount

For the development of this system, the *Skywatcher Star Adventurer GTI* was used as a telescope mount. As different mounts may guide with different speeds, the `pulse_multiplier` needs to be adjusted accordingly.

### Button

The system is designed to include a button, whose pin needs to be specified in `config.ini`. If no button is connected, the system can still be entirely operated by using the keyboard.
