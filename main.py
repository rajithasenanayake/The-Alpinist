import requests
import os 
import streamlit as st
from dotenv import load_dotenv
import pyautogui



# load_dotenv(override=True)

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "89489223-f738-402c-b44c-55c575309b2c"
FLOW_ID = "e7169340-8add-4261-bf70-5a3a6885195d"
# APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "watch" # The endpoint name of the flow
APPLICATION_TOKEN = st.secrets["APPLICATION_TOKEN"]


def run_flow(message: str) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


def set_background_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )



def main():

    image_url = "https://i.postimg.cc/nVNZHQPM/output-onlinepngtools.png"
    set_background_image(image_url)

    st.title("Get Your Seiko Alpinist")
    age = st.text_input(r"$\textsf{\large Please enter your age}$")
    occupation = st.text_input(r"$\textsf{\large Please enter your occupation}$")
    hobbies = st.text_area(r"$\textsf{\large Please enter some hobbies you prefer}$", placeholder="Example: Playing Cricket, Hiking, Travelling")
    diameter = st.radio(r"$\textsf{\large Select your preferred case size}$",('Mid-size', 'Large-size'),horizontal=True)
    st.write( r"$\textsf{\normalsize Preferred complications}$")

    complicatons = []

    checks = st.columns(4)
    with checks[0]:
       if st.checkbox('Date', value=True):
           complicatons.append('Date')
    with checks[1]:
         if st.checkbox('Inner Compass'):
             complicatons.append('Inner Compass')
    with checks[2]:
         if st.checkbox('GMT'):
             complicatons.append('GMT')
    with checks[3]:
       if  st.checkbox('Perpetual Calendar'):
           complicatons.append('Perpetual Calendar')
    
    specifications = st.text_area(r"$\textsf{\large List your specifications}$", placeholder="Example: Blue color with a leather strap")
    # lifestyle = "My age is " + age + ". My occupation is " + occupation +". My hobbies are " + hobbies +"."

    # specifications_text = "The watch case size I prefer is " + diameter + ". Other watch Specifications I prefer :" + specifications + ". Preferred complications are " + ", ".join(complicatons)
    # message = lifestyle + specifications_text

    user_data = {
        "Age": age,
        "Occupation": occupation,
        "Hobbies": hobbies,
        "Preferred Case Size": diameter,
        "Watch Specifications": specifications,
        "Prefered complications": ", ".join(complicatons) 
    }

    message = "{" + ", ".join(f"'{key} : {value}'" for key, value in user_data.items()) + "}"
    
    if st.button("Get My Alpinist"):
        if not message.strip():
            st.error("Please enter a message")
            return
        
        try:
            with st.spinner("Finding the best match..."):
                response = run_flow(message)
            
            response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(response)
        except KeyError as ke:
            st.error("Limited free runs are over. Appreciate your patience.")
        except Exception as e:
            st.error(str(e))

    if st.button("Clear All"):
        pyautogui.hotkey("ctrl","F5")

if __name__ == "__main__":
    main()
