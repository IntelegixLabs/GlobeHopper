<h1 align="center">GlobeHopper</h1>

### PROBLEM STATEMENT

In the realm of travel planning, the process of <b>curating packages, crafting itineraries, and making informed decisions</b> about the <b>best times for travel and economical transportation</b> options can be <b>intricate and time-consuming.</b> 

The existing challenges in the travel industry <b>need to include the need for quicker, more efficient solutions</b> that <b>enhance the overall experience for travelers,</b> ensuring they <b>receive personalized, cost-effective, and well-planned journeys.</b>

## Package Builder & Dynamic Itinerary Generator 
- Take input as User preferences.
- Select destination, i.e Europe -> and then select the cities you want to travel, our Gen AI App, will create a travel 
  itinerary for you that you can customize according to your needs.
- Customized map plan with given dates.
- Chatbot, trained on TBO hotels data.
- Curate personalized travel packages using GenAI.
- Weather conditions.
- Local events.
- Suggest the Best time to travel.
- Modify itineraries, and the AI will adjust recommendations accordingly.
- Book hotels, using TBO APIs.


### SOLUTION

<p> We’ve designed a Flask backend & React frontend-based client-server architecture to develop a website with state-of-the-art Generative AI technology to prompt the Large Language Model to make API calls to give outputs based on user inputs to customize trip plans. 
</p>



## 1. Project Architecture

<p align="center">
  <img src="data/globehopper.png" />
</p> 

## 2. Chatbot Generative AI RAG (Retrieval Augment Generation) Architecture

<p align="center">
  <img src="data/RAG.png" />
</p> 

## 3. Getting Started With The Flask API Application

```sh
$ git clone https://github.com/IntelegixLabs/GlobeHopper.git
$ cd GlobeHopper
$ pip install -r requirements.txt
$ python app.py
```

Note: Add the keys in .env file

### Delete the current db/chroma_db folder inside root directory and then download the chroma_db.zip from the given url and extract and copy the chroma_db folder in db folder

```sh
$ cd db 
$ rm chroma_db
$ wget https://drive.google.com/file/d/1cajdpavDIFgMFwpi2nrn9j7mxvaxzBou/view?usp=sharing
$ unzip chroma_db.zip
$ rm chroma_db.zip
```

### To run this project with docker locally
```sh
$ git clone https://github.com/IntelegixLabs/GlobeHopper.git
$ cd GlobeHopper
$ docker-compose -f docker/globehopper/docker-compose.yml up -d --build
```
Note: make sure you have secrets in the root folder

## 4. Getting Started With React UI Application

```sh
$ git clone https://github.com/IntelegixLabs/GlobeHopperUI.git
$ cd GlobeHopperUI
$ npm i
$ npm run dev
```

Note: Add the keys in .env file

## 5. Project Requirements

<h4>Languages</h4>
<ul>
  <li>JavaScript</li>
  <li>Python 3.10.5</li>
</ul>

<h4>Frameworks</h4>
<ul>
  <li>Node v18.13.0</li>
  <li>Flask v2.3.2</li>
  <li>npm v8.11.0</li>
</ul>

## 6. Application Screenshots / <a href="">Demo.</a>

[//]: # ([![Talk SynthSeg]&#40;data/GlobeHopper_youtube.png&#41;]&#40;https://www.youtube.com/watch?v=iJRNFXWZXf0&#41;)

<p align="center">
  <a href="https://www.youtube.com/watch?v=iJRNFXWZXf0"><img src="data/GlobeHopper_youtube.png" /></a>
</p>

<br />
<hr />
<br />

<p align="center">
  <img src="data/Screenshots/1.png" width="400"/>
  <img src="data/Screenshots/2.png" width="400"/>
  <img src="data/Screenshots/3.png" width="400"/>
  <img src="data/Screenshots/4.png" width="400"/>
  <img src="data/Screenshots/5.png" width="400"/>
  <img src="data/Screenshots/6.png" width="400"/>
</p>



## 6. Components to be built (Work In Progress)
* [x] UI improvement
* [x] Adding Voice Chat and voice response functionality, using Gen AI.
* [x] TBO Flight Integration.
