Today i will share some method to spoof your arduino same as your real mouse let's start :  
  
We need this [Usb device tree viewer](https://www.majorgeeks.com/files/details/usb_device_tree_viewer.html)  
Do simple spoof to your **board.txt** or use [This](https://www.unknowncheats.me/forum/valorant/605509-automate-arduino-leonardo-spoofing-using-python.html "Automate Arduino Leonardo Spoofing Using Python")  
  
After you spoof and make sure everything works let's do the hard work  
  
**Before we do any of those steps make this changes on a pc without valorant installed! and make sure to fully reset windows when you finish because VGK can see tracers of drivers same as file tracers. So upload ur scripts and spoof ur arduino on another pc and come to main pc and cheat ![](https://www.unknowncheats.me/forum/images/smilies/big_smile.png "Smilie"). Here is proof that ur drivers are not fully deleted

Code:

1. device manger>view>view hiden devices





**  
  
1-We gonna use this website to pull info about our mices [This](https://the-sz.com/products/usbid/index.php) Put your vid and pid and hit search for me i have logitech mouse So i need copy this **Logitech, inc.**  
Go to your board.txt and do this on last line  

Code:

1. leonardo.build.core=arduino
2. leonardo.build.variant=leonardo
3. leonardo.build.extra_flags={build.usb_flags}
4. leonardo.build.usd_manufacturer="Logitech, inc."

Save and reupload your script  
2-Modify device descriptors easy as it says first go here

Code:

1. C:\Program Files (x86)\Arduino\hardware\arduino\avr\cores\arduino

Look for USBcore.cpp Open it with notepad++ and go to line 44 [https://i.imgur.com/SRXPPL0.png](https://i.imgur.com/SRXPPL0.png) change it to match your mouse put your vid of real mouse and change the manufactor same as step 1 for me it was so mething like this [https://i.imgur.com/JfyYFMr.png](https://i.imgur.com/JfyYFMr.png)  
3-Here we can change serial of the arduino to match our mouse serial but this step will be 100% for everyone because some mouses has value of 0x0 so we dont really have use for it but im gonna share it anyways  
Go here

Code:

1. C:\Program Files (x86)\Arduino\hardware\arduino\avr\cores\arduino

USBcore.cpp line 71 here [https://i.imgur.com/Dsgqu9v.png](https://i.imgur.com/Dsgqu9v.png) change this to match your real mouse (again use the app i shared to find your exact value in case you have 0x0 in everything dont change nothing  

Code:

1. 0xEF = Device class
2. 0x02 = Device subclass
3. 0x01 = Device protocol
4. 0x100 = Version number (bcdDevice)
5. Iserial = serial number

3-Changing power consumption It's easy go here

Code:

1. C:\Program Files (x86)\Arduino\hardware\arduino\avr\cores\arduino

this time USBcore.h line 101 my real mouse > [https://i.imgur.com/VUsALiW.png](https://i.imgur.com/VUsALiW.png) this is my arduino spoofed > [https://i.imgur.com/lpIKG90.png](https://i.imgur.com/lpIKG90.png) you can see that both doesnt have same power consumption mA we can change this on USBcore.h as i showed  
4-Using external power supply Read here i already explain it [Here](https://www.unknowncheats.me/forum/4066011-post17.html)  
5-In case you sell your p2c make sure you send your clients a hex file not the skeatch file just to be safe  
6-Use hash changer to your .exe little security doesnt hurt  
  
If you have any question send it and if you guys want i can show you how to use HID and fully turn off your com port until than Have good day

__________________



## Tutorial: Fully Disable COM Port and Use HID Mouse  
  
The only credit goes to ChatGPT, GitHub, the UC forum, and Google.  
Credit also goes to khanxbahria for making MouseInstruct on github  
  
### Requirements:  
- Brain  
- Arduino Leonardo  
- USB Host Shield  
- Notepad++  
- Backup system restore  
  
### Steps:  
  
1. ****Backup Your System:****  
- Make sure to create a system restore point before making any changes.  
  
2. ****Open `USBCore.cpp` in Notepad++:****  
- Navigate to the following location:

Code:

1. `C:\Program Files (x86)\Arduino\hardware\arduino\avr\cores\arduino`

- Open `USBCore.cpp` with Notepad++.  
  
3. ****Modify `ClassInterfaceRequest`:****  
- Locate the `ClassInterfaceRequest` function, which starts around line 373.  
- You will see these lines:  
  

Code:

1. ```cpp
2. static bool ClassInterfaceRequest(USBSetup &setup) {
3.     u8 i = setup.wIndex;
4.     if (CDC_ACM_INTERFACE == i)
5.         return CDC_Setup(setup);
6. #ifdef PLUGGABLE_USB_ENABLED
7.         return PluggableUSB().setup(setup);
8. #endif
9.     return false;
10. }
11. ```

- Comment out the `CDC_ACM_INTERFACE` check and its associated line like this:  
  

Code:

1. ```cpp
2. // if (CDC_ACM_INTERFACE == i)
3. //     return CDC_Setup(setup);
4. ```

4. ****Modify `SendInterfaces`:****  
- Locate the `SendInterfaces` function around line 65.  
- You will see these lines:  

Code:

1. ```cpp
2. static u8 SendInterfaces() {
3.     u8 interfaces = 0;
4.     CDC_GetInterface(&interfaces);
5. #ifdef PLUGGABLE_USB_ENABLED
6.         PluggableUSB().getInterface(&interfaces);
7. #endif
8.     return interfaces;
9. }
10. ```

- Comment out the `CDC_GetInterface` line like this:  
  

Code:

1. ```cpp
2. // CDC_GetInterface(&interfaces);
3. ```

5. ****Save `USBCore.cpp`:****  
- Make sure to save the changes to `USBCore.cpp`.  
  
6. ****Update `boards.txt`:****  
- Open `boards.txt` located in the Arduino installation directory.  
- Add the following line at the end of the section for the Leonardo board:  

Code:

1.      ```txt
2.      leonardo.build.extra_flags={build.usb_flags} -DCDC_DISABLED
3.      ```

- Ensure that `leonardo` matches the name you use for your mouse. If not, this may cause bugs in the Arduino IDE.  
  
7. ****Configure Arduino IDE:****  
- Open Arduino IDE version 1.8.9.  
- Go to `File` > `Preferences`.  
- Check both "Show verbose output during: compilation" and "upload".  
  
8. ****Upload .hex file:****  
- You don't need to install any libraries; all necessary libraries are inside the .hex file.  
- Choose one of the libraries I shared (some may not be compatible with your mouse, but I will share more libraries later).  
- Select one of the libraries and navigate to: `C:\Program Files (x86)\Arduino\hardware\tools\avr\bin`  
- Paste the library file in this folder.  
- Open Command Prompt as an administrator and run the following command:  

Code:

1.      ```cmd
2.      cd C:\Program Files (x86)\Arduino\hardware\tools\avr\bin
3.      ```

- Select the .hex file by pressing Tab, then press Enter.  
- If you see the message `_avrdude.exe done. thank you._`, it means everything went smoothly.  
  
****Note:**** I won't be able to help with troubleshooting errors. You can follow the steps and use resources like Google and GitHub for assistance. Stay tuned for the 2PC method!  
  
Make sure you fully spoofed your arduino as it show here [Swoof arduino](https://www.unknowncheats.me/forum/valorant/641022-arduino-ud.html "Make your arduino UD again")

__________________