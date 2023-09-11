import streamlit as st
import requests
import subprocess
import os
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Comprehensive System",
    page_icon="🔍",
    layout="wide"
)

# Create a Streamlit app
st.title('Comprehensive System')
st.markdown("### Menu")

# Menu selection
menu_choice = st.sidebar.selectbox("Select an Option", ["Information Transformation", "Doctor Portal"])

if menu_choice == "Information Transformation":
    # Information Transformation Section

    # Your OCR.Space API key
    api_key = 'K83235972188957'

    # Upload an image using Streamlit's file uploader widget
    uploaded_file = st.file_uploader('Upload an image', type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        st.markdown("#### Uploaded Image")
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

        # Prepare payload for API request
        payload = {
            'apikey': api_key,
            'language': 'eng',  # Specify the language
        }

        # Make API request to OCR.Space
        response = requests.post('https://api.ocr.space/parse/image',
                                files={'image': uploaded_file},
                                data=payload)

        result = response.json()

        # Extracted text from the OCR.Space API response
        extracted_text = result['ParsedResults'][0]['ParsedText']

        # Display the extracted text
        st.markdown("#### Extracted Text:")
        st.write(extracted_text)

        # Specify the full path to newman executable
        newman_executable = r'C:\Users\agorejena\AppData\Roaming\npm\node_modules\newman\bin\newman.js'

        # Specify the URL of the Postman collection on GitHub
        postman_collection_url = "https://github.com/opentext/ot-core-capture/raw/main/postman/Core%20Capture%20Services%20-%20SmokeTest.postman_collection.json"

        # Specify the local path to save the downloaded collection
        local_collection_path = "Core Capture Services - SmokeTest.postman_collection.json"

        # Specify the working directory for Newman
        working_directory = "C:\\Users\\agorejena\\Music\\HealthDataX"

        # Download the Postman collection from GitHub
        try:
            response = requests.get(postman_collection_url)
            with open(os.path.join(working_directory, local_collection_path), "wb") as file:
                file.write(response.content)
        except Exception as e:
            st.error(f"Error downloading Postman collection: {str(e)}")

        # Run the Postman collection on the uploaded document using Newman
        try:
            # Specify the local path to save the uploaded PDF
            local_pdf_path = os.path.join(working_directory, "uploaded_document.pdf")
            with open(local_pdf_path, "wb") as pdf_file:
                pdf_file.write(uploaded_file.read())

            # Change the working directory to where the Newman executable is located
            os.chdir(os.path.dirname(newman_executable))

            # Run the Postman collection on the uploaded PDF using Newman
            # Surround the file paths with double quotes to handle spaces
            command = [newman_executable, "run", f'"{os.path.join(working_directory, local_collection_path)}"', "-d", f'"{local_pdf_path}"']
            subprocess.run(command, capture_output=True, text=True, check=True, cwd=working_directory)

            # Display a success message or handle the results as needed
            st.success("Document transformation completed successfully!")

            # Remove the local uploaded PDF and collection files
            os.remove(local_pdf_path)
            os.remove(os.path.join(working_directory, local_collection_path))
        except subprocess.CalledProcessError as e:
            # Display an error message if execution fails
            st.error(f"Error during document transformation:\n{e.stderr}")

elif menu_choice == "Doctor Portal":
    # Doctor Portal Section

    # Sidebar for doctor's options
    doctor_option = st.sidebar.selectbox("Select Doctor's Option",
                                         ["Disease Prediction from CSV", "Disease Prediction from Symptoms"])

    if doctor_option == "Disease Prediction from CSV":
        # Upload the CSV file for prediction
        uploaded_csv = st.file_uploader('Upload CSV for Disease Prediction', type=['csv'])

        if uploaded_csv is not None:
            st.markdown("#### Uploaded CSV for Disease Prediction")

            # Load the CSV data
            patient_data = pd.read_csv(uploaded_csv)

            # Data preprocessing (prepare the data for prediction)

            # Make predictions using the loaded model
            # Replace the following line with your actual prediction code
            predictions = ["Disease A", "Disease B", "Disease C"]  # Example predictions

            # Display the predictions
            st.subheader("Disease Predictions")
            st.write(predictions)

    elif doctor_option == "Disease Prediction from Symptoms":
        st.markdown("#### Enter Symptoms for Disease Prediction")

        # Collect symptoms input from the doctor
        symptom_input = st.text_area("Enter symptoms (comma-separated)", "")

        if st.button("Predict Disease"):
            # Preprocess the input symptoms and make predictions using the loaded model
            if symptom_input:
                # Split the comma-separated input into a list of symptoms
                symptoms = [s.strip() for s in symptom_input.split(',')]

                # Create a feature vector based on predefined symptom vocabulary
                symptom_vocabulary = ["fever", "cough", "headache", "nausea", "fatigue", "chest_pain", "sore_throat"]

                # Initialize a feature vector with zeros
                feature_vector = [0] * len(symptom_vocabulary)

                # Count the occurrence of each symptom in the input
                for symptom in symptoms:
                    if symptom in symptom_vocabulary:
                        index = symptom_vocabulary.index(symptom)
                        feature_vector[index] += 1

                # Convert the feature vector to a NumPy array
                symptom_features = np.array(feature_vector)

                # Make predictions using the loaded model
                # Replace the following line with your actual prediction code
                prediction = "Disease X"  # Example prediction

                # Display the prediction result
                st.subheader("Disease Prediction")
                st.write(f"Predicted Disease: {prediction}")
