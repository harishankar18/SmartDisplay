# SmartDisplay
A python framework for displaying news , images and videos on display board. Current framework allows to write plugins 
for displaying content in specific format.


An application will be running on cloud instance, accepts Teams stats and News in the format of jpeg, png, ppt and mp4.
The application will track yammer updates from the team-specific group, weather reports and traffic updates from google-maps.  

Application support to write the plugins depends on the what content needs to be displayed and how to content needs to be displayed.
E.g. weather updates stay one day on display where Teams stats can stay for more than 10 days. 
The application should display content received in web format(HTML).

Multiple clients can be connected to Cloud application and each client should receive content submitted by the users in a 
round-robin fashion.

Each TV is assisted by the raspberry-pi board, which connected to cloud application through the web browser. 
Configuration changes will be made to start web browser in full display mode, whenever raspberry is rebooted 
it will be connected to the server with the browser in full-display mode.
