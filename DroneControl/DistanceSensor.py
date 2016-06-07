from Sensor import Sensor
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

class DistanceSensor(Sensor):
    SPI_PORT = 0
    SPI_DEVICE = 0

    def __init__(self, spi_port, spi_device, channel):
        mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(spi_port, spi_device)

    def read(self):     #reads value from sensor
        value = Adafruit_MCP3008.read_adc(channel)
        height = 100 + (1023 - value) * 0.44
        return height


   