# UW Auto Registration

**A proof of concept by Jeremy Zhang**

This python program is a demonstration of how to skip the lines of online registration and sleep in during the morning of registration. The program's purpose is to automatically register for classes in the MyUW and fills in the SLN numbers and ADD Codes. This program is developed after a slight frustrating morning and requires **Python 2.7** to run. Tested and ran successfully on Ubuntu 14.04.

## Pip Packages Dependancies

**These required packages (pip install) are required for the program to run smoothly**
* selenium
* requests

## Other Required Dependancies

**These are to be also installed from other sources**
* Python 2.7 (Can be found in various places, such as apt-get)
* PhantomJS (Can be found on npm)

## Installation

1. Attempt to install the required pip packages listed above.
2. Install PhantomJS (from locations such as npm via node)
3. Git clone the repository onto the local drive
4. Create a file `config.py` and copy the contents of `config.example.py` into the `config.py` file.
5. Edit `config.py`, populating it with personal information & courses
6. Run the program with `python uwautoregistration.py` command.

**Once successfully ran, there will be an output `registration_result.png` to show the status of the registration page after submitting the courses.**

## TODO

* Implement notifyuw to switch between plans when one is full. (Currently it just picks the plan at index 0)
