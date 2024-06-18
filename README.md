# Arduino Leonardo Mouse Spoofing Tutorial

Today, I’ll share a method to spoof your Arduino to act like a real mouse. Let’s get started!

## Tools and Preparations

1. **USB Device Tree Viewer**: Download from [here](https://www.majorgeeks.com/files/details/usb_device_tree_viewer.html).
2. **Arduino Board Modification**: Follow the steps or use [this Python script](https://www.unknowncheats.me/forum/valorant/605509-automate-arduino-leonardo-spoofing-using-python.html) to automate the process.

**Important:** Make these changes on a PC without Valorant installed. Fully reset Windows afterward to remove any traces left by drivers or files.

## Step-by-Step Instructions

### 1. Identify Mouse Information

- Use [this website](https://the-sz.com/products/usbid/index.php) to find details about your mouse. Enter your VID and PID.
- For example, if you have a Logitech mouse, copy "Logitech, Inc."

### 2. Edit `boards.txt`

- Go to your `boards.txt` file and add the following lines at the end:

    ```txt
    leonardo.build.core=arduino
    leonardo.build.variant=leonardo
    leonardo.build.extra_flags={build.usb_flags}
    leonardo.build.usb_manufacturer="Logitech, Inc."
    ```

- Save and re-upload your script.

### 3. Modify USB Descriptors

- Navigate to:

    ```sh
    C:\Program Files (x86)\Arduino\hardware\arduino\avr\cores\arduino
    ```

- Open `USBcore.cpp` with Notepad++ and go to line 44. Update it to match your mouse’s VID and manufacturer:

    ```cpp
    // Example update
    ```

### 4. Change Serial Number (Optional)

- In `USBcore.cpp` at line 71, update it if your mouse has specific serial values:

    ```cpp
    0xEF = Device class
    0x02 = Device subclass
    0x01 = Device protocol
    0x100 = Version number (bcdDevice)
    Iserial = serial number
    ```

### 5. Adjust Power Consumption

- Open `USBcore.h` at line 101 and modify the power consumption to match your real mouse:

    ```cpp
    // Example adjustment
    ```

### 6. Use External Power Supply

```Ok so the thing that @itsmemadd mentioned is that if you have an external power source for your Arduino other than through the micro USB then vgc when loaded up cannot see the com port it's because when the Arduino recieves power it's in a vulnerable state where the bootloader needs time to setup correctly, so when you power on your pc and just use micro USB for power vgc is also loading and it can see the bootloader com port, you cannot see it cus for you windows UI is loading but vgc is so shit and intrusive it seems things before you do . So yea power the Arduino externally and just wait 10 seconds before you connect it to your pc while STILL HAVING IT CONNECT TO POWER ADAPTER.
```
So your pc turning on routine will be like this

Connect adapter to Arduino => power on the adapter => wait 10 seconds => connect Arduino via USB to pc => turn on your pc but keep both the usb and adapter connected all the time => you're good to go but to trigger the bootloader you will have to use the button on Arduino```

### 7. Secure Your Script

- If distributing, send a hex file instead of the sketch file for security.
- Use a hash changer for your .exe to enhance security.

---

## Fully Disable COM Port and Use HID Mouse

### Requirements

- Brain
- Arduino Leonardo
- USB Host Shield
- Notepad++
- Backup system restore

### Steps

1. **Backup Your System**: Create a system restore point.
2. **Open `USBCore.cpp` in Notepad++**: Navigate to:

    ```sh
    C:\Program Files (x86)\Arduino\hardware\arduino\avr\cores\arduino
    ```

3. **Modify `ClassInterfaceRequest`**:

    - Around line 373, comment out the `CDC_ACM_INTERFACE` check:

        ```cpp
        // if (CDC_ACM_INTERFACE == i)
        //     return CDC_Setup(setup);
        ```

4. **Modify `SendInterfaces`**:

    - Around line 65, comment out the `CDC_GetInterface` line:

        ```cpp
        // CDC_GetInterface(&interfaces);
        ```

5. **Save Changes**: Save `USBCore.cpp`.

6. **Update `boards.txt`**:

    - Add the following line at the end of the section for the Leonardo board:

        ```txt
        leonardo.build.extra_flags={build.usb_flags} -DCDC_DISABLED
        ```

7. **Configure Arduino IDE**:

    - Open Arduino IDE (version 1.8.9).
    - Go to `File` > `Preferences`.
    - Check "Show verbose output during: compilation" and "upload".

8. **Upload .hex File**:

    - Place the necessary library file in:

        ```sh
        C:\Program Files (x86)\Arduino\hardware\tools\avr\bin
        ```

    - Open Command Prompt as administrator and run:

        ```cmd
        cd C:\Program Files (x86)\Arduino\hardware\tools\avr\bin
        ```

    - Select and upload the .hex file. If you see "_avrdude.exe done. thank you._", everything went smoothly.

---

## Conclusion

If you have any questions, feel free to ask. I can also show you how to use HID and fully turn off your COM port. Have a great day!
