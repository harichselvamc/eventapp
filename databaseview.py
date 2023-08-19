import streamlit as st
import pyrebase

# Configure your Firebase credentials
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

def fetch_data():
    return db.child("typing_data").get().val()

def main():
    st.title("Firebase Data Viewer")

    data = fetch_data()

    if data:
        st.sidebar.title("Filter and Sorting Options")
        
        # Filtering options
        selected_name = st.sidebar.selectbox("Filter by Name", ["All"] + list(data.keys()))
        selected_class = st.sidebar.selectbox("Filter by Class", ["All"] + list(range(1, 13)))
        selected_school = st.sidebar.selectbox("Filter by School", ["All"] + sorted(set(value["school"] for value in data.values())))
        selected_total_words = st.sidebar.number_input("Filter by Total Words (min):", min_value=0)
        selected_accuracy_range = st.sidebar.slider("Filter by Accuracy Range", 0, 100, (0, 100))
        
        # Sorting options
        sort_by_accuracy = st.sidebar.checkbox("Sort by Accuracy")

        st.title("Data")

        filtered_data = []
        for key, value in data.items():
            if (selected_name == "All" or value["name"] == selected_name) and \
               (selected_class == "All" or value["class"] == selected_class) and \
               (selected_school == "All" or value["school"] == selected_school) and \
               (value["total_words"] >= selected_total_words) and \
               (selected_accuracy_range[0] <= value["accuracy"] <= selected_accuracy_range[1]):
                filtered_data.append((key, value))
        
        if sort_by_accuracy:
            filtered_data.sort(key=lambda x: x[1]["accuracy"], reverse=True)

        for key, value in filtered_data:
            st.write(f"Name: {value['name']}")
            st.write(f"Class: {value['class']}")
            st.write(f"School: {value['school']}")
            st.write(f"Total Words: {value['total_words']}")
            st.write(f"Accuracy: {value['accuracy']}%")
            st.write("---")

    else:
        st.write("No data available.")

if __name__ == '__main__':
    main()
