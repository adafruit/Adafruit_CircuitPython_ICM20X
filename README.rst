Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-icm20x/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/icm20x/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_ICM20X/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_ICM20X/actions
    :alt: Build Status

Library for the ST ICM-20X Wide-Range 6-DoF Accelerometer and Gyro Family


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-icm20x/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-icm20x

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-icm20x

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-icm20x

Usage Example
=============

For use with the ICM20649:

.. code-block:: python3

    import time
    import board
    import adafruit_icm20x

    i2c = board.I2C()   # uses board.SCL and board.SDA
    icm = adafruit_icm20x.ICM20649(i2c)

    while True:
        print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (icm.acceleration))
        print("Gyro X:%.2f, Y: %.2f, Z: %.2f rads/s" % (icm.gyro))
        print("")
        time.sleep(0.5)

For use with the ICM20948:

.. code-block:: python3

    import time
    import board
    import adafruit_icm20x

    i2c = board.I2C()  # uses board.SCL and board.SDA
    icm = adafruit_icm20x.ICM20948(i2c)

    while True:
        print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (icm.acceleration))
        print("Gyro X:%.2f, Y: %.2f, Z: %.2f rads/s" % (icm.gyro))
        print("Magnetometer X:%.2f, Y: %.2f, Z: %.2f uT" % (icm.magnetic))
        print("")
        time.sleep(0.5)

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/icm20x/en/latest/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_ICM20X/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
