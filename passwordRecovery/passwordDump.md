# Stop looking at me SWANN
## CCTV system password recovery.

Whilst it is possible to play video from many CCTV systems utilising solutions such as DME Forensics DVR examiner it can often be beneficial to recover a password for a system.
This can:-
- Allow access to system logs
- Show the user locked it with a unique password and not a system password. 
- Show ownership, for example email address and name associated to the device. 
- Allow access to non suported systems quickly. 


## Contents.
1. Intro
2. Built in recovery options. 
	- Utilising baked in recovery options against the system.
3. Flash Based Recovery - Tools Required. 
4. Software required. 
5. Extracting the device.
6. Dissasembling the firmware.
- Examples 
	- Anran Unit  - hashed password
	- Swann Unit - plaintext password in binary 

Many CCTV systems are based off of similar architecture commonly featuring HiSilicon Chipsets.
These systems typically run on a linux based operating system. In many cases this is stored on a SOIC-8 Flash IC chip. The underlying operating systems are also often common with only logos and graphics changing between some brands.

The aim of this aricle is to provide some examples of how to access further data and retrieve passwords from some of these systems. This knowledge and approach can then be built upon to access more systems.



# 2. Built in recovery options. 
There are often factory reset options which allow and administraytor password to be reset but this makes changes to the exhibit.
1. Swann MAC address by-pass. with many older Swann systems the MAC address of the device is the master password reset for the device. If you follow the fogot passowrd prompts it will state that it will send you an email (which it cant do as its disconnected on your bench). You will then be greeted by a screen to enter a password, if this is limited to Hex digits 0-F chances are the MAC address of the device is the master reset password.

The MAC can be discoveed utilising SWANN'S own tools or utilising tools such as netdiscover 
Plug your machine into the target device and utilise netdiscover.

`netdiscover -p`

Utilise the `-p` switch for passive mode, will detect the device when it is plugged into your machine and show its MAC address.

Wireshark can also be utilsied for this task.

2. Later SWANN systems require you to call them and provide a serial number of the unit and they will then provide you with a master reset password.

3. SPD Tool app. Cheaper brands such as ZOSI have a QR code embedded onto them. This can be scanned with the "SPD Tool" app to provide a reset password.

This has been removed from the play store and app store so use at your own risk

https://apkpure.com/spd/com.uuch.android_zxinglibrary


# 3. Flash Based Recovery - Hardware required. 

The operating system on a large number of CCTV systems is stored on a SOIC-8 form factor flash IC. This IC can commonly be read whilst in situ on the board. Common brands seen are often MXIC or Winbond based chips.

1. Commercial Flash memory readers. 

2. Non commercial options.
I reccomend purchasing a Raspberry Pi for this task. It is a small portable device which can perfom the exctraction and later dissasembly of the firmware. 

__SOIC -8 IC clip__. This allows the Target IC to be connected to whilst remaining on its target board. often the "nose" of these clips is required to be filed down to ensure a good conection.

__CH341A Programmer__ Commonly available on e-bay and other websites, this device is so cheap it could be considered disposable. Without modification however it utlises a 5v logic level to communicate with the Flash IC which is above the 3.3V logic level required. There is a slim chance this may damage the IC in the process.

![CH341A](/hardware/cctvTools-1.jpg)

__Raspberry PI SPI pins__. The Raspberry Pi has SPI bus pins exposes which can be utilised to communicate directly with a Flash IC. A power regulator should be ued however as the 3.3v rail on the Pi cannot supply neccicary current to the target board without risk. I have designed a PCB to break out these pins and make it compatible with common SOIC-8 Clips.  

__GOODFET42__ by Travis Goodspeed. Slightly more difficult to setup than the CH341A but a hightly versatile tool for reading flash memory devices. 

GOODFET42 info.

http://goodfet.sourceforge.net/hardware/goodfet42/

Assembled version

https://www.adafruit.com/product/1279


# 4. Software required
If you are utilising the non commercial flash reading options the below will be required.

**Flashrom**  - Utilised for reading the memory of the IC
https://flashrom.org/Flashrom


**Binwalk** - Utlisied for extracting the filesystem of the target.

Ensure you follow the full instructions for installing binwalk and ensure all the extras are istalled to suport SquashFS and JFFS or extraction of the full filesystem is unlikely.
https://github.com/ReFirmLabs/binwalk

Follow these install instructions.
https://github.com/ReFirmLabs/binwalk/blob/master/INSTALL.md


**A Hex editor** - if you are running the reccomended Pi, Bless can be installed.

`sudo apt-get install bless`

For other machines any standard hex editor such as HxD or Winhex will be fine.

**John the Ripper** - In the case of units where the passwork is hashed.
You will need the jumbo version to support the Dahua hash type.

https://www.openwall.com/john/

Knowledge of commands such as grep and strings.

# 5. Extracting the device. 
In most cases the IC can be read in stiu and will not need to be removed from the board.
Open the case of the target unit and and disconnect the hard drive. If the hard drive remains connected too much power may be be drawn and your extraction equipment may fail or be damaged.


Locate the flash IC chip and confirm its identity via its part number. Commonly seen manufacturers include Winbond and MXIC. This IC is usually close to the CPU of the target device and often on the top side of the board. However if you cannot locate it some manufacturers such as Techview have been known to locate them on the bottom  side of the board. When you locate the IC It is then also good practice to check the voltage of the VCC pin on the IC to ensure it is operating at the same voltage as your extraction tool. This is commonly 3.3v.

As a word if caution there is often power supply components with the same form factor as the Flash IC. Do not connect your extraction equipment to them or damage may be caused to the target unit and your extraction equipment.

Pin one on the flash IC can then be identified by a dot on the pin and usually also a marking on the PCB.

### **Utilising FLASHROM and a SOIC 8 clip to extract in-situ**
Connect the SOIC-8 clip to the IC and your flash reading tool of choice making sure PIN 1 connects to PIN 1 on the IC. If you have connected the clip correctly the LED’s on the PCB should light up. It may take a few attempts to get the clip to sit correctly and it may need to be held in place for the duration of the extraction
If you are utilising Flashrom to perform the extraction it will likely require SUDO access to operate correctly.

To simplify testing the connection run Flashrom with the watch command.

**CH341A**

`sudo watch flashrom -p ch341A`

**Raspberry Pi**
You will need to ensure you have enabled the SPI interface on your Pi.

`sudo watch flashrom -p linux_spi:dev=/dev/spidev0.0, spispeed=2000`

If the connection is correct a flash memory chip will be idenfied.

If you cannot get the IC clip to secure to the device you may need to solder wires to the legs or use a probe station to connect to it.

If the IC cannot be identified after repeated attempts and you are sure the IC clip connected properly you may have to remove the IC to communicate with it. Issues can be caused by the oboard CPU attempting to communicate with the IC as the same time as the flash reader. 

### Read the flash memory chip.
For example utilising the CH431A programmer, an output file of cctv.bin and a log file.

`sudo flashrom -p ch341a -r cctv.bin -o log.txt`

This will save the dump to a file called cctv.bin.
I often perfom more than one extraction to ensure data integrity.


# 6. Disassembling the firmware.
As above you need to make sure Binwalk is installed correctly or this is unlikley to work. There may be other tools which can perform these actions but this is what I used. 



# Example 1. 
## Anran Unit.
The passwords for this particular unit was stored in a “Dahua” hash format. At this time I only know of support in John the Ripper for craching this hash format. It is similar to MD5 and therefore you should be able to achieve a high hash rate with basic hardware. For example utilising the rockyou wordlist on an basic i5 office machine with no GPU John was able to crack the admin and user passwords in 0 seconds. Brute forcing is also highly feasable as the keyspace is often reduced to alphanumeric characters only and the hash rate is extremely high.

Extract the file with binwalk
We will utilise `-f` to generate a log file and `-e` to extract the files.

`binwalk -f log.txt -e anran.bin`

You will be presented with a large amount of output as bin walk extracts the various file systems.

Once this is complete you will have a folder called **_anran.bin.extracted.**

When you navigate this folder structure you should have the following path.
**anran.bin.extracted/jffs2-root/fs_1/Config**
In this Config folder there will be JSON files titled “Account1” “Account2” etc. 

Within these JSON files you will locate the password hashes stored at the bottom per the following example.

 "Password" : “6QNMIQGe"

Open a new terminal window and create a folder called hash to work in.

`mkdir hash`

Then create text file called **hash.txt** in the following format which will be recognised by John. The name is not important but will simplfiy the excercise. 

`nano hash.txt`

Enter the hashes into the file, prefixed by $dahua$, with each hash on a new line for example.

$dahua$6QNMIQGe

$dahua$tlJwpbo6

If you are going to run a wordlist or dictionary against the file you can also place it in this folder. The location of the word list does not matter but it makes the commands easier to work with when you are starting out if it is in the same location.

Open a terminal from within the Hash folder and run John the Ripper against the hashes.

Brute force attack.
`john hash.txt`

Dictionary Attack - in the case of a dictionary called rockyou.txt located in the same directory as the hash.txt file.

`john --wordlist=rockyou.txt hash.txt`

You should then be presented with a login password for the device.

$dahua$6QNMIQGe - "admin"

$dahua$tlJwpbo6 - Blank password

# Example 2. 
## Swann DVR.

**SWDVK-845806WL** and likley similar units. 

You can often discover user names by powering the system. The system will often populate the username field, this can speed up the process of locating a password for these systems.

In this example the passcode is stored in plain text in a configuration file. This unit had the latest firmware and reqired a serial number to be sent to SWANN for a Master Reset password. 

Extract the bin file using binwalk.

`binwalk -f log.txt -e swann.bin`

Locate the file devCfg.bin which should be located at the following path.

**/swann/_dump.bin-1.extracted/jffs2-root/fs_1**

This file contains the usernames and passwords stored in plaintext along with the name of the DVR.

You can then extract the password from the file in a number of ways.

### **Open in hex editor.**

`sudo bless devCfg.bin`

Scroll through and locate the username and password.

You can try searching for “admin” and the user name password will be stored next to that. Ensure you are searching for ASCII characters or you will return no results.

### **Utilise strings**
This will present printable characters contained in the file and present you with the usernames and passwords below them.

`strings devCfg.bin`
### ** Utilise Strings and GREP**
If a username, for example "Scott" is known you can pipe the output of strings into grep to search for the username and return the password which is stored next to it.
A2 and B2 return lines above and below the desired search term.

` strings devCfg.bin | grep -A2 -B2 "Scott"`