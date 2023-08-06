# Karol Krizka's Blinka Additions

Helpful addtions to the [Blinka](https://circuitpython.org/blinka) library.

## SPI via Big Banging IO Pins
The `SPIBitBanger` class implements SPI using digital IO pins defined via the `digitalio` library.

### Example with MAX31865
The `example.py` script shows how to use the MAX31865 Pt100 controller with the AdaFruit FT232H dongle. The MAX31865 board uses SPI phase 1 and control is thus not available via the `busio.SPI` package. However the FT232H can still use it by doing SPI via the generic IO pins.

Connect the following pins between your AdaFruit FT232H dongle and the MAX31865 board.
- `C0` to `CLK`
- `C1` to `SDO`
- `C2` to `SDI`
- `C3` to `CS`

Install the `adafruit-circuitpython-max31865` library and execute the example Python script.
```shell
pip install adafruit-circuitpython-max31865
BLINKA_FT232H=1 python example.py
```
