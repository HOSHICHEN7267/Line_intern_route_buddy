# Route Buddy (✪ω✪) 

An innovative route planning Line-chatbot designed for users who need real-time public transportation suggestions and love exploring. The key feature is its conversational interface for route planning: users only need to input the names of attractions or locations to receive accurate and detailed route recommendations. Our goal is to bring unparalleled convenience and enjoyment to every user, setting a new benchmark for intelligent travel.

## Features  

+ The first service that performs route planning via conversation. 
+ Provides real-time public transportation route planning.  
+ Supports route planning based on the name of "attractions" or "locations."  

## How to Use

Add the following Line chatbot as a friend.
[**LINK**](https://line.me/R/ti/p/@360jhbtt)

Send a message to the assistant with the following details: departure location, destination, and your preference (cost-saving or time-saving).  

**If the transportation method is successfully found:** </br>
The assistant will provide instructions on how to transfer using public transportation.  
**else:** </br>
The assistant will explain the issue and ask the user to resend the information.  

## Technologies Used  

+ Integrated **Line Messaging API** as the chat platform.  
+ Combined **OpenAI**, **Google Map Platform API**, and **TDX MaaS module** to generate route suggestions.
+ The service is deployed on **Render**

## Architecture  

This project uses **Line** as the chat platform and integrates **OpenAI**, **Google Maps**, and the **TDX MaaS module** to obtain public transportation route plans. The service is deployed on **Render** as a server.

### Workflow  

**Step 1:** When the chatbot receives user message, the text string is sent to **OpenAI** for natural language processing.  

**Step 2:** **OpenAI** converts the user input into a JSON format, which includes start and destination descriptions, along with user preferences. This JSON is sent to the **Google Map Geocoding API**.  

**Step 3:** Using the **Google Map Geocoding API**, the coordinates of the start and destination points are retrieved. These coordinates, combined with the user input, are passed to **TDX**.  

**Step 4:** The **TDX MaaS module** processes the user input and provides the planned routes, which are sent back to **OpenAI**.  

**Step 5:** **OpenAI** interprets the planned routes and generates natural language instructions, sending the route details back to the chatbot.  

**Step 6:** The chatbot presents the planned route to the user in a conversational format.  

## Cautions

**1.**
Since the service is currently deployed using a free account on Render, the server restart takes approximately 50 seconds. If there is a long gap between messages, you may need to wait for the server to wake up. Please re-enter your message after about 1 minute to receive a proper response.

**2.**
Currently, this service only supports Chinese and does not support other languages (additional languages are planned for the future). Please use Chinese when communicating with the chatbot.

**3.**
**(For LINE interviewers)**  During the implementation process, I accidentally used my lab mate's GitHub account to push to the repository. (The commit record of *chu-ching-liang* (cd51a3f ~ 5270680) are commits made using my lab mate's account.) I apologize for the inconvenience and kindly ask for your understanding and attention regarding this matter.

