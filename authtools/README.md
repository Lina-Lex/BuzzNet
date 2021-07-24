# authtools

A library that helps in generating and sending autentication tokens and OTP via SMS

Need to install ```python 3.7+``` and ```twilio``` for proper functioning.

## Settings
Export all the environmental variable and Populate in ```env.py``` file by using the **os.environ** 
* ENV setting : 
    * Otp services: Create a twilio account and download twilio with ```pip install twilio```
    * export the accout SId , sender phonenumber  and the auth token for twilio as per the os into the below env variables 
      ```
      TWILIO_ACCOUNT_SID = account sid
      TWILIO_AUTH_TOKEN = Auth token
      SENDER_NUMBER =  number to send from 
      ```
    * set/export the otp expired timer env variable ```default 300 seconds```  **type intiger** 
      ```
      OTP_DURATION = 300 # As per requirement this flag determins the otp validity duration``` 
* ***Note these flags can be changed as per requirement but that might need changes to the env.py file as well***

### General usage ###

```
from authtools import send_otp,verify_otp

send_otp(to='+91736273839')  # return type is bool

    # the otp will be sent as per the setting mentions in the env.py file
    # to verify the otp 

verify_otp(otp = '627282',ph = '+917363527382') # return type is bool
```


## API Reference

* The most two usefull functions are ```send_otp``` and ```verify_otp``` 

**otpstore.send_otp(to : str = None,sender: str = None, otp_len= 6)**<br />

&nbsp;&nbsp;&nbsp;&nbsp;Checks ,maps and send the otp to the provided number,Avoid passing the sender information to the fuction directly . Please use the env.py file for setting the sender info<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return type is a boolian value 


**otpstore.verify_otp(otp : str = '', ph : str = '')**<br />

&nbsp;&nbsp;&nbsp;&nbsp;Verifies the provided otp.<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return type is a boolian value


**otpstore.purgeOtpDb**<br />
 
&nbsp;&nbsp;&nbsp;&nbsp;This is function is usefull for purging hte otp cache database which can be scheduled at a periodic time.<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return type is a None 

