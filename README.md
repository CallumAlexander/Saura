# Saura
<h1>The Official Saura github repository</h1>

Installion Guide
Download this repository and save all present files in the same file location.
Ensure Python 3.5 or later is installed
Run this command within the present command prompt / terminal - pip install pyserial - and follow the onscreen instructions until completed.
Run 'main.py'

<u>Changelog</u>

1.1.0.beta - 07/03/19 // Current Build
Exports all data recieved to a .xlsx file.
Prompts the user to enter the name of the port they wish to use.
Recording works in terms of steps instead of the number of elapsed seconds.
Optimization of the data preprocessing that reduces run time.
Heisenbug, IndexError, that was periodically thrown is fixed.
Credits updated
General system optimization to reduce run time including removing testing data, comments and time.sleep statements

1.0.1.beta - 26/02/19
General cleaning up of old commented code.
Removal of debugging prints and variables.
Added comments to certain functions.
awaiting testing

1.0.0.beta
Pyserial python library implememted.
Data received from the ground reciever is parsed and displayed.
Random testdata removed.

0.3.1
ASCII art graphic of the word 'SAURA' remains at the top of the interface perpetually.

0.3.0
Simple control methods added - start recording, end program, home return.
Scrolling title - ASCII art graphic of the word 'SAURA'.

0.2.0
Further analysis of values - addition of change in value and difference arrow added altitude and temperature. 

0.1.0
Prerelease testdata generated using random values.
Orientation coordinates, altitude, temperature data structures defined and displayed.
Prints information to command line.

Contact Information:
Developer - Callum Alexander , callumalexander.personal@gmail.com
Developer - Fraser Rennie , fjrennie1@gmail.com

This project uses semantic versioning

