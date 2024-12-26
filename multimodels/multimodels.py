import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import os, fitz, PIL.Image, time
from dotenv import load_dotenv

load_dotenv()
path2 = '/Users/....'

def page_setup():
    st.header("Chat with different types of media/files!", anchor=False, divider="blue")

    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)


def get_typeofpdf():
    st.sidebar.header("Select type of Media", divider='rainbow')
    typepdf = st.sidebar.radio("Choose one:",
                               ("PDF files",
                                "Images",
                                "Video, mp4 file",
                                "Audio files"))
    return typepdf


def get_llminfo():
    st.sidebar.header("Model Options", divider='rainbow')
    tip1="Select a model you want to use."
    model = st.sidebar.radio("Choose LLM:",
                                  ("gemini-1.5-pro",
                                   "gemini-1.5-flash",
                                   "gemini-2.0-flash-exp"
                                   ), help=tip1)
    tip2="Lower temperatures are good for prompts that require a less open-ended or less creative response, while higher temperatures can lead to more diverse or creative results. A temperature of 0 means that the highest probability tokens are always selected."
    temp = st.sidebar.slider("Temperature:", min_value=0.0,
                                    max_value=2.0, value=1.0, step=0.25, help=tip2)
    tip3="Used for nucleus sampling. Specify a lower value for less random responses and a higher value for more random responses."
    topp = st.sidebar.slider("Top P:", min_value=0.0,
                             max_value=1.0, value=0.94, step=0.01, help=tip3)
    tip4="Number of response tokens, 8194 is limit."
    maxtokens = st.sidebar.slider("Maximum Tokens:", min_value=100,
                                  max_value=5000, value=1800, step=100, help=tip4)
    return model, temp, topp, maxtokens


def delete_files_in_directory(directory_path):
   try:
     files = os.listdir(directory_path)
     for file in files:
       file_path = os.path.join(directory_path, file)
       if os.path.isfile(file_path):
         os.remove(file_path)
   except OSError:
     print("Error occurred while deleting files.")


def setup_documents(pdf_file_path):
    to_delete_path = path2
    delete_files_in_directory(to_delete_path)
    doc = fitz.open(pdf_file_path)
    os.chdir(to_delete_path)
    for page in doc: 
        pix = page.get_pixmap(matrix=fitz.Identity, dpi=None, 
                              colorspace=fitz.csRGB, clip=None, alpha=False, annots=True) 
        pix.save("pdfimage-%i.jpg" % page.number)  # Save each page as an image


def main():
    page_setup()
    typepdf = get_typeofpdf()
    model, temperature, top_p,  max_tokens = get_llminfo()
    
    if typepdf == "PDF files":
        uploaded_files = st.file_uploader("Choose 1 or more PDF", type='pdf', accept_multiple_files=True)
           
        if uploaded_files:
            text = ""
            for pdf in uploaded_files:
                pdf_reader = PdfReader(pdf)
                for page in pdf_reader.pages:
                    text += page.extract_text()

            generation_config = {
              "temperature": temperature,
              "top_p": top_p,
              "max_output_tokens": max_tokens,
              "response_mime_type": "text/plain",
              }
            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel(
              model_name=model,
              generation_config=generation_config,)
            st.write(model.count_tokens(text)) 
            question = st.text_input("Enter your prompt and hit enter.")
            if question:
                start_time = time.time()  # Start time before the model generates content
                response = model.generate_content([question, text])
                end_time = time.time()  # End time after the response is received
                response_time = end_time - start_time  # Calculate response time
                st.write(f"Response time: {response_time:.2f} seconds")  # Display response time
                st.write(response.text)
                
    elif typepdf == "Images":
      image_file_name = st.file_uploader("Upload your image file.", type=['jpg', 'jpeg', 'png', 'tif'])
      if image_file_name:
        # Use a local temp directory to store the file temporarily
        temp_dir = '/tmp'  # Use a temp directory on the local system
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save the uploaded file to a temporary location
        fpath = os.path.join(temp_dir, image_file_name.name)
        with open(fpath, 'wb') as f:
            f.write(image_file_name.getbuffer())  # Save the uploaded file content

        # Upload the file to GenAI
        image_file = genai.upload_file(path=fpath)
        
        while image_file.state.name == "PROCESSING":
            time.sleep(10)
            image_file = genai.get_file(image_file.name)
        
        if image_file.state.name == "FAILED":
            raise ValueError(image_file.state.name)
        
        # Prompt for the image analysis
        prompt2 = st.text_input("Enter your prompt.") 
        if prompt2:
            generation_config = {
                "temperature": temperature,
                "top_p": top_p,
                "max_output_tokens": max_tokens,
            }
            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel(model_name=model, generation_config=generation_config)
            
            start_time = time.time()  # Start time before the model generates content
            response = model.generate_content([image_file, prompt2], request_options={"timeout": 600})
            end_time = time.time()  # End time after the response is received
            response_time = end_time - start_time  # Calculate response time
            st.write(f"Response time: {response_time:.2f} seconds")  # Display response time
            st.markdown(response.text)
            
            # Clean up by deleting the file after use
            genai.delete_file(image_file.name)
            print(f'Deleted file {image_file.uri}')
           
    elif typepdf == "Video, mp4 file":
      video_file_name = st.file_uploader("Upload your video")
      if video_file_name:
        # Use a local temp directory to store the video file temporarily
        temp_dir = '/tmp'  # Use a temp directory on the local system
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save the uploaded video to a temporary location
        fpath = os.path.join(temp_dir, video_file_name.name)
        with open(fpath, 'wb') as f:
            f.write(video_file_name.getbuffer())  # Save the uploaded file content

        # Upload the file to GenAI
        video_file = genai.upload_file(path=fpath)
        
        while video_file.state.name == "PROCESSING":
            time.sleep(10)
            video_file = genai.get_file(video_file.name)
        
        if video_file.state.name == "FAILED":
            raise ValueError(video_file.state.name)
        
        # Prompt for the video analysis
        prompt3 = st.text_input("Enter your prompt.") #"what is said in this video in the first 20 seconds?"
        if prompt3:
            start_time = time.time()  # Start time before the model generates content
            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel(model_name=model)
            
            response = model.generate_content([video_file, prompt3], request_options={"timeout": 600})
            end_time = time.time()  # End time after the response is received
            response_time = end_time - start_time  # Calculate response time
            st.write(f"Response time: {response_time:.2f} seconds")  # Display response time
            st.markdown(response.text)
            
            # Clean up by deleting the file after use
            genai.delete_file(video_file.name)
            print(f'Deleted file {video_file.uri}')
      
    elif typepdf == "Audio files":
      audio_file_name = st.file_uploader("Upload your audio")
      if audio_file_name:
        # Use a local temp directory to store the file temporarily
        temp_dir = '/tmp'  # Use a temp directory on the local system
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save the uploaded audio to a temporary location
        fpath = os.path.join(temp_dir, audio_file_name.name)
        with open(fpath, 'wb') as f:
            f.write(audio_file_name.getbuffer())  # Save the uploaded file content

        # Upload the file to GenAI
        audio_file = genai.upload_file(path=fpath)
        
        while audio_file.state.name == "PROCESSING":
            time.sleep(10)
            audio_file = genai.get_file(audio_file.name)
        
        if audio_file.state.name == "FAILED":
            raise ValueError(audio_file.state.name)
        
        # Prompt for audio analysis
        prompt3 = st.text_input("Enter your prompt.")  # Example: "What is said in this audio file?"
        if prompt3:
            start_time = time.time()  # Start time before the model generates content
            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel(model_name=model)
            
            response = model.generate_content([audio_file, prompt3], request_options={"timeout": 600})
            end_time = time.time()  # End time after the response is received
            response_time = end_time - start_time  # Calculate response time
            st.write(f"Response time: {response_time:.2f} seconds")  # Display response time
            st.markdown(response.text)
            
            # Clean up by deleting the file after use
            genai.delete_file(audio_file.name)
            print(f'Deleted file {audio_file.uri}')


if __name__ == '__main__':
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    main()
