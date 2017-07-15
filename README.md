Instructions:

How to run Front End:

On terminal run: python frontEnd.py

Open up web browser and go to: http://localhost:8080

How to run Back End:

To change the depth of the crawler, go to the backEnd.py.
After the entering command to run on the terminal, the program will prompt you to enter the depth. Enter a digit on the commandline to set the depth. 

To change the links, go to urls.txt. 
Add the desired url to crawl in a new line with no trailing or leading spaces. 
The url must begin with http:// or https://

On terminal run: python backEnd.py


How to run Test:

Install nose.py if not available on environment. On linux run on terminal: pip install nose

Inside backEnd_test.py, the comments are written for what is being tested. 

There are 3 screenshots with words on the webpage.

Bing image - www.bing.com has words 'images' and 'explore'.

Google Chromium page image - www.google.com has words 'images', 'gmail', and 'privacy'

Google Chromium Privacy and Policy page image - https://www.google.com/intl/en/policies/privacy/?fg=1 has words 'welcome' and 'policy'

The test should take 20 seconds to run.

On terminal run: nosetests backEnd_test.py
