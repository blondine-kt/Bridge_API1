from fastapi import FastAPI
import uvicorn
import requests
import time

# Create FastAPI app object
app = FastAPI()

# url vers le micro service des nouvelles
EXTERNAL_LOCALNEWSAPI = "http://127.0.0.1:8035/news"

#url vers le microservice de meteo

EXTERNAL_WEATHERAPI = "http://127.0.0.1:8040/weather_info"

def get_localnews(city):
   try:
      start = time.time()
      response = requests.get(EXTERNAL_LOCALNEWSAPI,params={"city":city}) 
      
      #retourne le temps des reponse
      roundtrip = time.time() - start
      print(f"Response Time News Api {roundtrip}")
      #retourne les informations sur les nouvelles
      return response.json()
   except Exception as e:
      print(e)
      return {
                    "title": "NA",
                    "auteur": "NA",
                    "url": "NA",
                    "text": "NA"
                }

def get_weather_info(city):
   
   try:
      start = time.time()
      #retourne les informations sur la meteo
      response = requests.get(EXTERNAL_WEATHERAPI,params={"city":city})

      #retourne le temps des reponse
      roundtrip = time.time() - start
      print(f"Response Time WeatherApi {roundtrip}")
      return response.json()
   except Exception as e:
      print(e)
      return {
            'city': "NA",
            'description':"NA",
            'date': "NA",
            'temp': "NA",
            'temp_r':"NA"
            }
      


@app.get("/get_all_info/")
async def get_cityinfo(city):
   
   try:

    weather_info = get_weather_info(city)

    local_news = get_localnews(city)

   

    return {
       "weather": weather_info,
       "news": local_news
    }
   except Exception as e:
      print(e)
      return{
         "news":{
           "title": "NA",
            "auteur": "NA",
            "url": "NA",
            "text": "NA"},
            "weather":{
            'city': "NA",
            'description':"NA",
            'date': "NA",
            'temp': "NA",
            'temp_r':"NA"}
       } 




if __name__ =='__main__':
     uvicorn.run(app, host='0.0.0.0', port =8045, workers=1)


