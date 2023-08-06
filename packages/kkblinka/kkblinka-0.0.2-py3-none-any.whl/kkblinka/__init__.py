from adafruit_blinka import Lockable
import digitalio

import sys

class SPIBitBanger(Lockable):
    """
    A bit-banged SPI implementation using GPIO.
    """
    def __init__(self, clk, mosi, miso):
        """
        The I/O state of the pins will be set here.

        Parameters
        ----------
        clk : digitalio.DigitalInOut
            The clock pin.
        mosi : digitalio.DigitalInOut
            The MOSI pin.
        miso : digitalio.DigitalInOut
            The MISO pin.
        """
        self.clk = clk
        self.clk.direction = digitalio.Direction.OUTPUT

        self.mosi = mosi
        self.mosi.direction = digitalio.Direction.OUTPUT

        self.miso = miso
        self.miso.direction = digitalio.Direction.INPUT

        self.polarity=0
        self.phase=1
        self.bits=8

    def configure(self, baudrate=100000, polarity=0, phase=0, bits=8):
        """
        Update the configuration.
        """
        if self._locked:
            self.baudrate=baudrate
            self.polarity=polarity
            self.phase=phase
            self.bits=bits

            self.clk.value=self.polarity
        else:
            raise RuntimeError("First call try_lock()")

    def __sendbyte(self, byte):
        """
        Send a single byte on the SPI bus and return received data.

        Parameters
        ----------
        int : byte
            The byte to send, MSB first

        Returns the received byte during transmission.
        """
        # Initialize the state of the SPI bus.
        self.clk.value = self.polarity

        # Send the data, byte at a time.
        ibyte=0
        for bit in range(7,-1,-1):
            if self.phase==0:
                # Set value
                self.mosi.value = (byte>>bit) & 0x1
                # Leading edge to send/save
                self.clk.value = ~self.polarity
                ibyte=ibyte|(self.miso.value<<bit)
                # Falling edge for the next bit
                self.clk = self.polarity
            elif self.phase==1:
                # Set value
                self.mosi.value = (byte>>bit) & 0x1
                self.clk.value = ~self.polarity
                # Send it and save
                self.clk.value = self.polarity
                ibyte=ibyte|(self.miso.value<<bit)

        # Idle state
        self.clk.value = self.polarity

        return ibyte

    def write(self, buffer, start=0, end=sys.maxsize):
        """
        Write the data contained in `buffer`.

        Parameters
        ----------
        buffer : ReadableBuffer
            write out bytes from this buffer
        start : int
            beginning of buffer slice
        end : int
            end of buffer slice; if not specified, use `len(buffer)`
        """
        if not self._locked:
            raise RuntimeError("First call try_lock()")

        if end==sys.maxsize:
            end=len(buffer)

        for i in range(start,end):
            self.__sendbyte(buffer[i])
        #asf
        #self.send([address|0x80, value&0xFF])

    def readinto(self, buffer, start=0, end=sys.maxsize, write_value=0):
        """
        Read into `buffer` while writing `write_value` for each byte read. The
        SPI object must be locked. If the number of bytes to read is 0, nothing
        happens.

        If `start` or `end` is provided, then the buffer will be sliced as if
        `buffer[start:end]` were passed. The number of bytes read will be the
        length of `buffer[start:end]`.

        Parameters
        ----------
        buffer : WriteableBuffer
            read bytes into this buffer
        start : int
            beginning of buffer slice
        end : int
            end of buffer slice; if not specified, it will be the equivalent
            value of `len(buffer)` and for any value provided it will take the
            value of `min(end, len(buffer))`
        write_value : int
            value to write while reading
        """
        if not self._locked:
            raise RuntimeError("First call try_lock()")

        if end==sys.maxsize:
            end=len(buffer)

        for i in range(start,end):
            buffer[i]=self.__sendbyte(write_value)

    def write_readinto(self, out_buffer, in_buffer, out_start=0, out_end=sys.maxsize, in_start=0, int_end=sys.maxsize):
        """
        Write out the data in `out_buffer` while simultaneously reading data
        into `in_buffer`. The SPI object must be locked.

        If `out_start` or `out_end` is provided, then the buffer will be sliced
        as if `out_buffer[out_start:out_end]` were passed, but without copying
        the data. The number of bytes written will be the length of
        `out_buffer[out_start:out_end]`.

        If `in_start` or `in_end` is provided, then the input buffer will be
        sliced as if `in_buffer[in_start:in_end]` were passed, The number of
        bytes read will be the length of `out_buffer[in_start:in_end]`.

        The lengths of the slices defined by `out_buffer[out_start:out_end]` and
        `in_buffer[in_start:in_end]` must be equal. If buffer slice lengths are
        both 0, nothing happens.

        Parameters
        ----------
        out_buffer : ReadableBuffer
            write out bytes from this buffer
        in_buffer : WriteableBuffer
            read bytes into this buffer
        out_start : int
            beginning of out_buffer slice
        out_end : int
            end of out_buffer slice; if not specified, use `len(out_buffer)`
        in_start : int
            beginning of in_buffer slice
        in_end : int
            end of in_buffer slice; if not specified, use `len(in_buffer)`
        """
        if not self._locked:
            raise RuntimeError("First call try_lock()")

        if out_end==sys.maxsize:
            out_end=len(out_buffer)

        if in_end==sys.maxsize:
            in_end=len(in_buffer)

        if out_end-out_start != in_end-in_start:
            raise RuntimeError("Input and output slices must be of equal length!")

        for o,i in zip(range(out_start,out_end), range(in_start,in_end)):
            out_buffer[o]=self.__sendbyte(in_buffer[i])
