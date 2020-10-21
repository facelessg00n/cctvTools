## User guide for the goodfet 42

Installation

`git clone https://github.com/travisgoodspeed/goodfet/`

`cd goodfet`

`(cd client && sudo make link)`

Not you should be able to run `goodfet` from your command line. 

### **Chip info**
`goodfet.spiflash info` 
### **Dump Flash**
Dump the flash memory

`goodfet.spiflash dump $foo.bin`
