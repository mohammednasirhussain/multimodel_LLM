# Chat with Different Types of Media Files
This is a Streamlit-based web application that allows users to interact with different types of media (PDF files, images, videos, and audio files) and generate responses using Google's Generative AI models.

## Features
Upload and process PDF files to extract text and interact with the content.
Upload image files and interact with the image content.
Upload video and audio files for content generation based on the uploaded media.
Configure model parameters such as temperature, top_p, and maximum tokens for controlling the model's response generation.
Support for multiple media types in a user-friendly interface.

## Technologies Used
Streamlit: For creating the interactive web interface.
Google Generative AI: For generating content based on the uploaded media.
PyPDF: For extracting text from PDF files.
PyMuPDF: For converting PDF pages to images.
Pillow (PIL): For handling image processing.
pydotenv: For managing environment variables (e.g., Google API key).

## How It Works
PDF files: Upload one or more PDF files. The app will extract the text from these PDFs and use the text as input for a generative AI model. You can ask questions based on the PDF content, and the model will generate a response.

Images: Upload an image and enter a prompt. The app will upload the image to Google Generative AI and generate content based on the image.

Videos: Upload an MP4 video file and enter a prompt. The app will process the video content and generate a response based on the content of the video.

Audio files: Upload an audio file and provide a prompt. The app will process the audio and generate content based on the audio file.

## Model Options
The app provides several generative model options, which can be selected in the sidebar:

gemini-1.5-pro
gemini-1.5-flash
gemini-2.0-flash-exp
You can also adjust the following model parameters:

Temperature: Controls the creativity of the response. Lower values make the response more deterministic, while higher values make it more diverse.
Top P: Used for nucleus sampling to control randomness.
Maximum Tokens: The maximum length of the generated response.
