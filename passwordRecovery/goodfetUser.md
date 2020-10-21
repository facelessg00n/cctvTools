## User guide for the goodfet 42

https://github.com/travisgoodspeed/goodfet

http://goodfet.sourceforge.net/apps/spi/

SPI Pinout

http://goodfet.sourceforge.net/clients/goodfetspiflash/


## Installation

`git clone https://github.com/travisgoodspeed/goodfet/`

`cd goodfet`

`(cd client && sudo make link)`

Not you should be able to run `goodfet` from your command line. 
## Commands

### **Chip info**
`goodfet.spiflash info` 
### **Dump Flash**
Dump the flash memory

`goodfet.spiflash dump $foo.bin`
