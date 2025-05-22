[Chessboard-Hardware](https://github.com/UnsignedArduino/Chessboard-Hardware) |
[Chessboard-Design](https://github.com/UnsignedArduino/Chessboard-Design) |
[Chessboard-Nano](https://github.com/UnsignedArduino/Chessboard-Nano) |
[Chessboard-Pi](https://github.com/UnsignedArduino/Chessboard-Pi)

# Chessboard-Pi

Raspberry Pi firmware for a magnetic-piece-tracking digital chessboard! WIP

This repository contains the Python project for the firmware that goes on the
Raspberry Pi. (that goes on the 2nd PCB)

## Install

For development, you can also install this on a normal PC, as it only needs a
serial connection to the chessboard.

### Dependencies

* Python (earliest version tested with is 3.11)
* `python3-cairosvg` on Debian (use `sudo apt install`) - for other OS ses the
  [cairosvg docs](https://cairosvg.org/documentation/#installation).

### Steps

1. Clone the repo.
2. Create virtual environment and install dependencies.

## Usage

Run [`main.py`](src/main.py) to start the program. Pass in the serial port with
`-p`.

```bash
python3 src/main.py -p /dev/ttyACM0
```

or on Windows:

```commandline
python src/main.py -p COM28
```
