[![Downloads](https://static.pepy.tech/personalized-badge/mini-cheetah-motor-driver-socketcan?period=total&units=abbreviation&left_color=blue&right_color=black&left_text=PyPi%20Downloads)](https://pepy.tech/project/mini-cheetah-motor-driver-socketcan)   [![DOI](https://zenodo.org/badge/342504440.svg)](https://zenodo.org/badge/latestdoi/342504440)


# Python Motor Driver for Mini Cheetah-type Actuators from T-Motor/CubeMars

This driver was developed at the Underactuated Lab in Robotics Innovation Center at DFKI GmbH, Bremen.

It assumes the use of a CAN to USB adapter (such as [PEAK System's PCAN-USB](https://www.peak-system.com/PCAN-USB.199.0.html?&L=1) or [ESD's CAN-USB/2](https://esd.eu/produkte/can-usb-2)) connected to a linux (tested on Ubuntu) computer. The SocketCAN interface is used, thus allowing the use of Python Socket library.

Initial tests show communication (send-reply) frequencies of ~800Hz  using PCAN-USB and ~1500Hz using ESD CAN-USB/2 with a single motor connected.

# Dependencies:

* bitstring

Install via:

`pip3 install bitstring`

# Documentation

- Useful videos: 
    - [From T-Motor](https://www.youtube.com/watch?v=hbqQCgebaF8)
    - [From Skyentific](https://www.youtube.com/watch?v=HzY9vzgPZkA)
- [Motor Datasheets](https://store.cubemars.com/images/file/20220307/1646619452473352.pdf)
- [Ben Katz Documentation](https://docs.google.com/document/d/1dzNVzblz6mqB3eZVEMyi2MtSngALHdgpTaDJIW_BpS4/edit)

# Pre-requisites:

* Setting up the CAN interface:

  * Run this command and make sure that `can0` (or any other can interface depending on the system)shows up as an interface after connecting the USB cable to your laptop: `ip link show`

  * Configure the `can0` interface to have a 1 Mbaud communication frequency: `sudo ip link set can0 type can bitrate 1000000`

  * To bring up the `can0` interface, run: `sudo ip link set up can0`

* To change motor parameters such as CAN ID or to calibrate the encoder, a serial connection is used. The serial terminal used on linux for this purpose is `screen`. Example usage:
```
sudo apt-get install screen
screen /dev/ttyUSB0 921600
```

# Usage:

Import: `from motor_driver.canmotorlib import CanMotorController` if installed via `pip`. Otherwise, adjust import statement based on system's `PYTHONPATH` (e.g. when cloned from GitHub).

Example Motor Initialization: `motor = CanMotorController(can_socket='can0', motor_id=0x01, motor_type='AK80_6_V2', socket_timeout=0.5)`

Available Functions:

- `enable_motor()`
- `disable_motor()`
- `set_zero_position()`
- `send_deg_command(position_in_degrees, velocity_in_degrees, Kp, Kd, tau_ff):`
- `send_rad_command(position_in_radians, velocity_in_radians, Kp, Kd, tau_ff):`
- `change_motor_constants(P_MIN_NEW, P_MAX_NEW, V_MIN_NEW, V_MAX_NEW, KP_MIN_NEW, KP_MAX_NEW, KD_MIN_NEW, KD_MAX_NEW, T_MIN_NEW, T_MAX_NEW)`

All motor communication functions return current position, velocity, torque in SI units except for `send_deg_command`. `change_motor_constants` does not return anything.

# Supported Motor Configurations:

- AK80-6 (From Cubemars, Firmware versions V1, V1.1, and V2): `motor_type='AK80_6_V1'`, `motor_type='AK80_6_V1p1'` and `motor_type='AK80_6_V2'`
- AK80-9 (From Cubemars, Firmware version V1.1 and V2): `motor_type='AK80_9_V1p1'` and `motor_type='AK80_9_V2'`
- AK70-10 (From Cubemars, Firmware version V1.1): `motor_type='AK70_10_V1p1'`
- AK10-9 (From Cubemars, Firmware version V1.1): `motor_type='AK10_9_V1p1'`. **TODO:** The temperature and error codes are received but not yet decoded for the new firmware for this motor.

```
# Working parameters for AK80-6 V1.0 firmware
AK80_6_V1_PARAMS = {
                "P_MIN" : -95.5,
                "P_MAX" : 95.5,
                "V_MIN" : -45.0,
                "V_MAX" : 45.0,
                "KP_MIN" : 0.0,
                "KP_MAX" : 500,
                "KD_MIN" : 0.0,
                "KD_MAX" : 5.0,
                "T_MIN" : -18.0,
                "T_MAX" : 18.0,
                "AXIS_DIRECTION" : -1
                }

# Working parameters for AK80-6 V1.1 firmware
AK80_6_V1p1_PARAMS = {
                "P_MIN" : -12.5,
                "P_MAX" : 12.5,
                "V_MIN" : -22.5,
                "V_MAX" : 22.5,
                "KP_MIN" : 0.0,
                "KP_MAX" : 500,
                "KD_MIN" : 0.0,
                "KD_MAX" : 5.0,
                "T_MIN" : -12.0,
                "T_MAX" : 12.0,
                "AXIS_DIRECTION" : -1
                }

# Working parameters for AK80-6 V2.0 firmware
AK80_6_V2_PARAMS = {
                "P_MIN" : -12.5,
                "P_MAX" : 12.5,
                "V_MIN" : -38.2,
                "V_MAX" : 38.2,
                "KP_MIN" : 0.0,
                "KP_MAX" : 500.0,
                "KD_MIN" : 0.0,
                "KD_MAX" : 5.0,
                "T_MIN" : -12.0,
                "T_MAX" : 12.0,
                "AXIS_DIRECTION" : 1
                }

# Working parameters for AK80-9 V1.1 firmware
AK80_9_V1p1_PARAMS = {
                "P_MIN" : -12.5,
                "P_MAX" : 12.5,
                "V_MIN" : -22.5,
                "V_MAX" : 22.5,
                "KP_MIN" : 0.0,
                "KP_MAX" : 500,
                "KD_MIN" : 0.0,
                "KD_MAX" : 5.0,
                "T_MIN" : -18.0,
                "T_MAX" : 18.0,
                "AXIS_DIRECTION" : 1
                }

# Working parameters for AK80-9 V2.0 firmware
AK80_9_V2_PARAMS = {
                    "P_MIN" : -12.5,
                    "P_MAX" : 12.5,
                    "V_MIN" : -25.64,
                    "V_MAX" : 25.64,
                    "KP_MIN" : 0.0,
                    "KP_MAX" : 500.0,
                    "KD_MIN" : 0.0,
                    "KD_MAX" : 5.0,
                    "T_MIN" : -18.0,
                    "T_MAX" : 18.0,
                    "AXIS_DIRECTION" : 1
                    }

// Working parameters for AK70-10 V1.1 firmware
AK70_10_V1p1_params = {
                      "P_MIN" :  -12.5,
                      "P_MAX" :  12.5,
                      "V_MIN" :  -50,
                      "V_MAX" :  50,
                      "KP_MIN" :  0,
                      "KP_MAX" :  500,
                      "KD_MIN" :  0,
                      "KD_MAX" :  5,
                      "T_MIN" :  -24.0,
                      "T_MAX" :  24.0,
                      "AXIS_DIRECTION" :  1
                    }

# Working parameters for AK10-9 V1.1 firmware
AK10_9_V1p1_PARAMS = {
                "P_MIN" : -12.5,
                "P_MAX" : 12.5,
                "V_MIN" : -50.0,
                "V_MAX" : 50.0,
                "KP_MIN" : 0.0,
                "KP_MAX" : 500,
                "KD_MIN" : 0.0,
                "KD_MAX" : 5.0,
                "T_MIN" : -65.0,
                "T_MAX" : 65.0,
                "AXIS_DIRECTION" : -1
                }

```

To add a new constants configuration use the `change_motor_constants` function or create an issue with the constants and motor information on the GitHub page to be added to the driver.

# Known Issues

**Issue Fixed**: When having 2 motors on the CAN bus with either PCAN CAN-USB or ESD CAN-USB/2, sometimes the motors experience an initial short *kick/impulse* at when they are enabled again after being disabled. This was fixed.

As this is experimental software, there might be other unknown issues.
