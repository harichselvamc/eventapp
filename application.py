import streamlit as st
import time
import pyrebase


import streamlit as st
import json

# Load the Firebase configuration JSON string from the secrets
firebase_config_json = st.secrets["server"]["firebase_config"]

# Parse the JSON string into a dictionary
firebase_config = json.loads(firebase_config_json)

# Now you can access individual values from the config dictionary
# Extract values from the config dictionary
api_key = firebase_config["apiKey"]
auth_domain = firebase_config["authDomain"]
database_url = firebase_config["databaseURL"]
project_id = firebase_config["projectId"]
storage_bucket = firebase_config["storageBucket"]
messaging_sender_id = firebase_config["messagingSenderId"]
app_id = firebase_config["appId"]
measurement_id = firebase_config["measurementId"]
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

def count_down(ts):
    with st.empty():
        while ts:
            mins, secs = divmod(ts, 60)
            time_now = '{:02d}:{:02d}'.format(mins, secs)
            st.header(time_now)
            ts -= 1
            time.sleep(1)
        st.header("Time Up!")
        
        
def calculate_accuracy(user_paragraph, admin_paragraph):
    # Your accuracy calculation function
    correct_chars = sum(user_char == admin_char for user_char, admin_char in zip(user_paragraph, admin_paragraph))
    total_chars = len(admin_paragraph)
    
    if total_chars == 0:
        return 0
    
    accuracy = (correct_chars / total_chars) * 100
    return accuracy







def save_typing_stats_to_firebase(name, class_level, school, total_words, wrong_chars, accuracy):
    # Your save to Firebase function
    data = {
        "name": name,
        "class": class_level,
        "school": school,
        "total_words": total_words,
        "wrong_words": wrong_chars,
        "accuracy": accuracy
    }
    db.child("typing_data").push(data)



def main():
    st.image("image.jpeg", use_column_width=True)  # Make sure "image.jpeg" is in the same directory as your script
    
    st.markdown("<h1 style='text-align: center;'>Type Sprint</h1>", unsafe_allow_html=True)
    

    st.write("Enter your details and complete the typing challenge:")

    name = st.text_input("Name:")
    class_level = st.selectbox("Class:", list(range(1, 13)))
    school = st.text_input("School:")

    st.write("---")

    st.header("Type the Paragraph")
    user_paragraph = st.text_area("Type the following paragraph:")

    start_button = st.button("Start Timer")

    if start_button and name and class_level and school:
        st.session_state.timer_started = True
        st.write("Timer started!")
        time_in_seconds = 60
        count_down(time_in_seconds)
        st.session_state.timer_started = False

        admin_paragraph = 'I failed the first quarter of a class in middle school, so I made a fake report card. I did this every quarter that year.'
        
        user_accuracy = calculate_accuracy(user_paragraph, admin_paragraph)

        st.write("---")
        st.header("Typing Results")
        st.write(f"Student Name: {name}")
        st.write(f"Class: {class_level}")
        st.write(f"School: {school}")
        st.write(f"Total Typed Words: {len(user_paragraph)}")
        st.write(f"Accuracy: {user_accuracy:.2f}%")

        save_typing_stats_to_firebase(name, class_level, school, len(user_paragraph), 0, user_accuracy)

    else:
        st.write("Please enter your details and click 'Start Timer'.")

    if hasattr(st.session_state, "timer_started"):
        if st.session_state.timer_started:
            st.header("Timer is currently running!")

    


if __name__ == '__main__':
    main()
