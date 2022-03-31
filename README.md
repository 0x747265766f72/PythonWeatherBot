# WeatherBot

## About  
I made this program as a personal automation script, but I want to make it available for anyone to use.  
The main goal of this project was to notify me whenever there is a good probability of viewing the Northern Lights (Aurora Borealis)  
This project was completed over two days and supports the functionality of sending emails to multiple people at customizable times of the day.  
I speculate that due to the AccuWeather API, some functionality (Snow Forecasting) is restricted to the United States.  
  
Full project functionality includes:  
 - The ability to notify someone if there is a good probability for seeing the Northern Lights within the next 3 hours based on their current location.  
 - The ability to notify someone if there is a good viewing of a full moon/night sky.  
 - The ability to have a current weather condition report sent. (currently configured with custom "Good Morning" message)  
 - The ability to notify you if there is snow, and send a corresponding 12-hour forecast.  
 - The ability to notify you if today is an optimal day to view a metoer shower

## **Required Libraries**  
```pip install -r requirements.txt```

## **Credential Setup**

  Create a new file in the main directory called ``creds.json``

  Format the ``creds.json`` file as follows:
	```{
	"openWeather_API_Key":"YOUR API KEY HERE",
	"accuWeather_API_Key":"YOUR API KEY HERE",
	"bot_password":"YOUR BOT GMAIL PASSWORD HERE",
	"toList":
	[
	"email1@email.com",
	"email2@email.com"
	]
	}```



## **APIs Setup**

  https://openweathermap.org/price#weather (Free Edition)  
    This API key is for the ``openWeather_API_Key`` variable  
    Generated with default settings  

  https://developer.accuweather.com/user/me/apps (limited to 50 requests/ day)   
    This API key is for the ``accuWeather_API_Key`` variable  
    API key generated with these settings:
| Setting | Value |
| :---: | :---: |
| Application Name 	                                                | [Can be whatever you want] |
| API Products 	                                                    | Limited Trial |
| Where will the API be used? 	                                    | Other |
| What will you be creating with this API?                          | Internal App |
| What programming language is your APP written in? 	              | Python |
| Is this for Business to Business or Business to Consumer use? 	  | Business to Consumer |
| Is this Worldwide or Country specific use? 	                      | Country |
| Country 	                                                        | United States |
| What is the public launch date? 	                                | [Cannot Change Date] |
    
## **E-mail setup**
 - Make a new gmail account and change the settings to allow it to run in untrusted apps
 - Update the ``bot_email`` variable with whatever email you have for this new account
 - In ``creds.json`` update the ``bot_password`` Variable with the password for this gmail account
 - Update the "toList" array in ``creds.json`` to be a list of emails you wish to send to  
	  
  **(ONLY USE PERSONAL EMAILS OR EMAILS OF PEOPLE WHO HAVE EXPRESSLY CONSENTED TO HAVE AUTOMATED EMAILS SENT TO THEM)**  
	  
  Update the ``sendList`` Variables the ``GoodMorningVietnam()``, ``NorthernFuckingLights()``, and ``WhiteShitFallingFromTheSky()`` methods in ``WeatherBot.py`` to reflect the specific indexes in the ``toList`` array for which emails each account should recieve or be subscribed to.

*Regards,*  
*Trevor* 
