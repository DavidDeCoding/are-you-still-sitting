# are-you-still-sitting

This App takes input from a RTSP server can be IP Camera or just your iPhone and call you when you are sitting more than 30 mins at a stretch.

It has 2 main parts:
1. Frontend App - This is a simple app that sits on your computer. Uses OpenCV and Pytorch to read from a RTSP stream (The chair under monitor), uses YoloV7 model to detect if you are sitting or not, and sends a request to the backend when the you sit down or get up.
2. Backend - This another simple app that receives the sitting state from Frontend. And also starts and stops timer when you sit down, and when you go over 30 mins of sitting calls you using Twilio.
