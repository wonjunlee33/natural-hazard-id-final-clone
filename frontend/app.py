import json
import streamlit as st
import pandas as pd
import requests
from collections import OrderedDict
from st_draggable_list import DraggableList
import os

# Initialize session state variables if they don't exist
if "confirmed" not in st.session_state:
    st.session_state.confirmed = []
if "rejected" not in st.session_state:
    st.session_state.rejected = []
if "user_report" not in st.session_state:
    st.session_state.user_report = ""
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False
if "in_classification_type" not in st.session_state:
    st.session_state.in_classification_type = False


# Load hazard data from Excel file
@st.cache_resource
def load_hazard_data():
    return pd.read_excel('hazard_definitions.xlsx')

hazard_data = load_hazard_data()

def map_hazard_codes_to_names(codes):
    # Iterate over each code and find the corresponding name in the hazard_data DataFrame
    return [hazard_data[hazard_data['code'] == code]['name'].iloc[0] for code in codes]

# Info button for hazard description
def info_button(index):
    if st.button("ℹ️", key=f"info_{index}", help="Click for hazard description"):
        st.session_state[f"show_def_{index}"] = not st.session_state.get(f"show_def_{index}", False)

# Toggle for showing the definition
def defintion_expander(index, hazard_description):
    if st.session_state.get(f"show_def_{index}", False):
        with st.expander("Definition:", expanded=True):
            st.write(hazard_description)


def login():
    """
    Displays the login page and prompts the user to enter their credentials.
    """
    st.title("Welcome to NLP/LLM-Guided Natural Hazard Taxonomisation! 🎉")
    st.image("https://images.unsplash.com/photo-1675116516161-12c0a3f6e5a5?q=80&w=3474&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", use_column_width=True, caption="photo by CrowN")
    st.subheader("Please enter your credentials to proceed. 🤫")

    # Get the username and password from the user
    username = st.text_input("Username:", key="username_input")
    password = st.text_input("Password:", type="password", key="password_input")
    st.toast('Beta version, please do not use for any real world applications.')

    if st.button("Login"):
        users = os.environ.get("USERNAMES").split(',')
        answer = os.environ.get("PASSWORD")
        if username.lower() in users and password == answer:
            st.session_state.is_authenticated = True
            # st.snow()
            st.success("Login successful! Welcome aboard! 🚀")
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again. 😥")


def classification_type():
    """
    Displays a classification type selection interface and handles user choices.
    """
    st.title("Classification Type")

    st.markdown("#### Please select the classification type you want to use: 🤔", unsafe_allow_html=True)
    classification_type = st.selectbox("Select Classification Type:", ["🤖 Rules-Based Model", "🧠 Machine Learning Model"])

    st.write("")
    if classification_type == "🤖 Rules-Based Model":
        st.session_state.classification_type = "rules"
        st.markdown("You've selected the **Rules-Based Model**! 🏁", unsafe_allow_html=True)
    else:
        st.session_state.classification_type = "ml"
        st.markdown("You've selected the **Machine Learning Model**! 🏎️", unsafe_allow_html=True)

    st.write("")
    if st.button("🎯 Submit Choice", key="submit_choice"):
        st.session_state.in_classification_type = True
        st.success("Thank you! Your choice has been submitted! 🎉")
        st.rerun()

    st.write("----")
    st.markdown("#### How does the classification work? 🧐")
    st.markdown("* **Rules-Based Model**: This model works by loading hazard definitions from a JSON file and an Excel file. It then tokenizes an event report, identifies hazards based on the hazard definitions and user input, and prints the identified hazards. The model uses a set of predefined rules and prompts the user for input to determine if a hazard is present in the report.")
    st.markdown("* **Machine Learning Model**: Utilizes OpenAI's GPT-3.5 API to analyze event reports and identify potential hazards through natural language processing. Unlike the rules-based approach, it dynamically interprets report content, generating a preliminary list of hazards. It then asks the user targeted questions to confirm these hazards. This model offers a flexible and evolving hazard identification system.")


def user_report():
    """
    Displays a user interface for entering and submitting a report.

    This function creates a Streamlit user interface that allows the user to enter a report
    either by typing it manually or by uploading a text file. The entered report is then
    displayed in a preview section. When the user clicks the "Submit Report" button, the
    report is stored in the session state and a success message is displayed.
    """
    st.title("Enter Your Report 📝")
    st.subheader("Please enter the details of the report you want to classify or upload a text file:")

    # Expander for default reports
    with st.expander("📖 View default report"):
        st.markdown("```In April 2023, Eleven types of hazard incidents occurred across Bangladesh, including, Boat Capsized, Bridge Collapse, Covid-19, Dengue, Fire, Heat Wave, Lightening, Nor‘wester, Riverbank Erosion, Wall Collapse, and Wild Animal Attacks. According to the daily newspaper, 18 Lightning events occurred in sixteen districts which caused 26 people to die from different age and gender groups. Three incidents of Boat Capsized occurred in 3 districts including Lalmonirhat, Narayanganj, and Patuakhali districts. Due to these incidents, six people died and one person was missing in the districts. With reference to the daily hazard situation report of MoDMR and DDM, a total of 970 Fire incidents took place in 17 districts, resulting in five death, sixty-two injured, and 9,095 shops, one warehouse, and 63 houses were burnt. etc. due to Fire incidences in April 2023. The estimated losses were 1,004 crores 20 lakh and 50 thousand takas. Based on the DGHS daily situation report, Dengue was slightly more severe in April 2023 with compare to March 2023. It caused the death of five people, and 143 confirmed cases were identified throughout 11 districts this month. Three events of the Wild Elephant Attacks happened in Mymensingh and Sherpur districts respectively on the 14th, 22nd, and 28th of April 2023. two people were killed by a Wild Elephant Attack in the mentioned districts. On the other hand, a wall collapse incident occurred in Madaripur district. During this incident, one child died and four were injured. A Bridge collapsed in Mymensingh which caused a car damaged and three people injured. In the district of Shariatpur, one incident of Riverbank Erosion occurred which resulted in of 100-meter embankment collapse due to erosion. In this month, seven nor ‘wester incidents hit Patuakhali, Bagerhat, Cox's Bazar, Dhaka, Satkhira, Mymensingh, and Gazipur districts which caused damage to 1050 houses, 100 shops, 1,000 tin-roofed structures, 200 hectares of land at the affected areas. Covid-19 affected a total number of 204 people in 7 districts in April 2023. According to the national report published by DGHS in April 2023, due to Covid-19, no death is reported and 108 recovered. The devastating activity of Covid-19 decreased compared to March 2023, but the infected rate slightly increased in April compared to March 2023. Besides, the country has experienced a total of 29 different levels of heat wave in 64 four districts where Mild, mild to moderate, and extreme heat wave was 3, 2, and 1 respectively. The maximum temperature was recorded at 43 degrees Celsius at Ishdardi (Pabna) during heat wave situations on 18 April 2023. No casualties were recorded due to the heat wave.```")

    # Manual text input for report
    manual_report = st.text_area("Your Report:", value='', placeholder='Enter your report here...', height=300, key="manual_report")

    # File uploader
    uploaded_file = st.file_uploader("📎 Or upload a text report file:", type=['txt'])

    # Handling file upload
    if uploaded_file is not None and uploaded_file.type == "text/plain":
        # Read text file
        manual_report = str(uploaded_file.read(), "utf-8")

    # Preview report
    if manual_report:
        with st.expander("🔍 Report Preview:"):
            st.write(manual_report)

    if st.button("Submit Report"):
        st.session_state.user_report = manual_report
        st.session_state.in_report_submission = True
        st.success("🎉 Report submitted successfully!")
        st.rerun()


def display_question(index, question, hazard_description, use_toggle):
    st.write("Question:", question['question'])
    key_base = f"answer_{index}_{question['hazardCode']}"

    if use_toggle:
        col1, col2 = st.columns([9, 1], gap="small")

        with col1:
            answer = st.radio("Your answer:", ["Yes", "No"], key=key_base, horizontal=True)

        with col2:
            info_button(index)

        defintion_expander(index, hazard_description)

    else:
        col1, col2 = st.columns([9, 1], gap="small")
        answer = col1.text_input("Your answer (y/n):", key=key_base).strip().lower()

        with col2:
            info_button(index)

        defintion_expander(index, hazard_description)

    return answer

def process_answers(questions_data, confirmed_hazard_codes, rejected_hazard_codes, use_toggle):
    all_answers_filled = True

    for index, question in enumerate(questions_data):
        hazard_description = hazard_data[hazard_data['code'] == question['hazardCode']]['description'].iloc[0]
        answer = display_question(index, question, hazard_description, use_toggle)

        if answer.lower() in ["y", "yes", "1"]:
            confirmed_hazard_codes.append(question['hazardCode'])
        elif answer.lower() in ["n", "no", "2"]:
            rejected_hazard_codes.append(question['hazardCode'])
        else:
            all_answers_filled = False

    return all_answers_filled


def question():
    """
    Displays a set of questions based on the classification type and user report.

    If the classification type is "ml", it displays the title as "LLM-Based Model".
    If the classification type is not "ml", it displays the title as "Rules-Based Model".

    The questions are displayed in an information message and the user is expected to answer
    them with a yes (y/1) or no (n/2).

    If the "questions_data" is not present in the session state, it fetches the API URLs based
    on the classification type and user report. It then sends a POST request to the API and
    stores the response in the session state.

    The user can choose to use a toggle for the questions by checking the "Use Toggle for Questions"
    checkbox.

    After the user answers all the questions and clicks the "Submit Answers" button, it checks if
    all the answers are filled. If they are, it displays a success message, stores the confirmed
    and rejected hazard codes in the session state, sets the "in_refined_question" flag to True,
    and reruns the app.

    If all the answers are not filled, it displays an error message.
    """

    if st.session_state.classification_type == "ml":
        st.title("LLM-Based Model")
    else:
        st.title("Rules-Based Model")
    st.info("Based off the report provided please answer the following questions with a yes (y/1) or no (n/2)")

    if "questions_data" not in st.session_state:
        api_url_ml = os.environ.get("API_URL_ML")
        api_url_rules = os.environ.get("API_URL_RB")
        api_url = api_url_ml if st.session_state.classification_type == "ml" else api_url_rules
        report = st.session_state.user_report if st.session_state.user_report else "In April 2023, Eleven types of hazard incidents occurred across Bangladesh, including, Boat Capsized, Bridge Collapse, Covid-19, Dengue, Fire, Heat Wave, Lightening, Nor‘wester, Riverbank Erosion, Wall Collapse, and Wild Animal Attacks. According to the daily newspaper, 18 Lightning events occurred in sixteen districts which caused 26 people to die from different age and gender groups. Three incidents of Boat Capsized occurred in 3 districts including Lalmonirhat, Narayanganj, and Patuakhali districts. Due to these incidents, six people died and one person was missing in the districts. With reference to the daily hazard situation report of MoDMR and DDM, a total of 970 Fire incidents took place in 17 districts, resulting in five death, sixty-two injured, and 9,095 shops, one warehouse, and 63 houses were burnt. etc. due to Fire incidences in April 2023. The estimated losses were 1,004 crores 20 lakh and 50 thousand takas. Based on the DGHS daily situation report, Dengue was slightly more severe in April 2023 with compare to March 2023. It caused the death of five people, and 143 confirmed cases were identified throughout 11 districts this month. Three events of the Wild Elephant Attacks happened in Mymensingh and Sherpur districts respectively on the 14th, 22nd, and 28th of April 2023. two people were killed by a Wild Elephant Attack in the mentioned districts. On the other hand, a wall collapse incident occurred in Madaripur district. During this incident, one child died and four were injured. A Bridge collapsed in Mymensingh which caused a car damaged and three people injured. In the district of Shariatpur, one incident of Riverbank Erosion occurred which resulted in of 100-meter embankment collapse due to erosion. In this month, seven nor ‘wester incidents hit Patuakhali, Bagerhat, Cox's Bazar, Dhaka, Satkhira, Mymensingh, and Gazipur districts which caused damage to 1050 houses, 100 shops, 1,000 tin-roofed structures, 200 hectares of land at the affected areas. Covid-19 affected a total number of 204 people in 7 districts in April 2023. According to the national report published by DGHS in April 2023, due to Covid-19, no death is reported and 108 recovered. The devastating activity of Covid-19 decreased compared to March 2023, but the infected rate slightly increased in April compared to March 2023. Besides, the country has experienced a total of 29 different levels of heat wave in 64 four districts where Mild, mild to moderate, and extreme heat wave was 3, 2, and 1 respectively. The maximum temperature was recorded at 43 degrees Celsius at Ishdardi (Pabna) during heat wave situations on 18 April 2023. No casualties were recorded due to the heat wave."

        payload = {"report": report}
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            st.session_state.questions_data = response.json()
        else:
            st.error(f"Error fetching data. Status Code: {response.status_code}")
            return

    confirmed_hazard_codes = []
    rejected_hazard_codes = []
    use_toggle = st.checkbox("Use Toggle for Questions:", key="use_toggle")

    all_answers_filled = process_answers(st.session_state.questions_data, confirmed_hazard_codes, rejected_hazard_codes, use_toggle)

    if st.button("Submit Answers"):
        if all_answers_filled:
            st.success("Thanks for your answers! 🎉")
            st.session_state.confirmed = confirmed_hazard_codes
            st.session_state.rejected = rejected_hazard_codes
            st.session_state.in_refined_question = True
            st.rerun()
        else:
            st.error("Please answer all questions before submitting.")


def refined_question():
    """
    This function handles the refined question flow in the application.
    It displays refined questions based on the classification type and user responses.
    It also handles the submission of answers and updates the session state accordingly.
    """

    if st.session_state.classification_type == "ml":
        st.title("LLM-Based Model")
    else:
        st.title("Rules-Based Model")

    if "refined_questions_data" not in st.session_state:
        api_url = os.environ.get("API_URL_REFINE")
        payload = {"confirmed": st.session_state.confirmed, "rejected": st.session_state.rejected}
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            st.session_state.refined_questions_data = response.json()
        else:
            st.error(f"Error fetching data. Status Code: {response.status_code}")
            return

    if not st.session_state.refined_questions_data:
        st.success("No further questions to ask. Thank you!")
        confusion()
        display_confirmed_hazards()
        export_hazard_data()
        rank_buttons()
        switch_model()
        restart()
        return

    if st.session_state.refined_questions_data:
        st.warning("Thank you for your response. I have a few more questions. Sorry!")
        st.info("Please answer the following questions with a yes (/y/1) or no (/n/2)")

    confirmed_hazard_codes = st.session_state.confirmed
    rejected_hazard_codes = st.session_state.rejected
    use_toggle = st.checkbox("Use Toggle for Questions:", key="use_toggle")

    all_answers_filled = process_answers(st.session_state.refined_questions_data, confirmed_hazard_codes, rejected_hazard_codes, use_toggle)

    if st.button("Submit Answers"):
        if all_answers_filled:
            st.success("Thanks for your answers! 🎉")
            st.session_state.confirmed = confirmed_hazard_codes
            st.session_state.rejected = rejected_hazard_codes
            st.session_state.in_refined_question = True
            st.session_state.refined_questions_data = None
            st.rerun()
        else:
            st.error("Please answer all questions before submitting.")


def display_confirmed_hazards():
    """
    Displays the confirmed hazard codes and names.

    This function retrieves the confirmed hazard codes from the session state and displays them along with their names and additional information.
    It also provides an option to toggle the display of often confused hazard codes and names.
    """
    if st.session_state.confirmed:
        st.markdown("## 🚨 Confirmed Hazard Codes and Names:")
        # Remove duplicates while preserving order
        unique_confirmed = sorted(list(OrderedDict.fromkeys(st.session_state.confirmed)))
        confusion()
        confused_hazards = st.session_state.confused
        i = 0

        for index, code in enumerate(unique_confirmed):
            name = map_hazard_codes_to_names([code])[0]

            # Extracting hazard description based on the current code
            hazard_description = hazard_data[hazard_data['code'] == code]['description'].iloc[0]

            # Create a four-column layout
            col1, col2, col3, col4 = st.columns([1, 3, 1, 1])

            # Use the first column for the hazard code with a background color
            col1.markdown(f"<div style='background-color:#f0f2f6; padding:10px; border-radius:8px;'>{code}</div>", unsafe_allow_html=True)

            # Use the second column for the hazard name
            col2.write(name)

            # Info button in the third column
            with col3:
                info_button(code)

            defintion_expander(code, hazard_description)

            with col4:
                question_text = '[❓](#)'
                if st.button(question_text, key=f"question_{index}", help="Click for confused hazards"):
                    st.session_state[f"question_{code}"] = not st.session_state.get(f"question_{code}", False)

            # Toggle for showing the definition
            if st.session_state.get(f"question_{code}", False):
                with st.expander("Often Confused With:", expanded=True):

                    confused_code = [code.strip() for code in confused_hazards[i].split(",")]
                    # Create a two-column layout for code and name
                    col1, col2 = st.columns([1, 3])
                    # Use the first column for the hazard code
                    for x in range(len(confused_code)):
                        col1.markdown(f"<div style='background-color:#f0f2f6; padding:10px; border-radius:8px; margin-bottom: 2px;'>{confused_code[x]}</div>", unsafe_allow_html=True)
                        # Use the second column for the hazard name
                        col2.write(map_hazard_codes_to_names([confused_code[x]])[0])

            i += 1
            st.markdown("---")
    else:
        st.markdown("### No confirmed hazards at this time. ✅")

def rank_hazards(option):
    st.write(" ")
    key = f'rank_hazards_{option}'

    if key not in st.session_state:
        st.session_state[key] = False

    if st.button(f'Rank Hazards by {option}'):
        st.session_state[key] = not st.session_state[key]

    if st.session_state[key]:
        if "confirmed" in st.session_state:
            unique_confirmed = sorted(list(OrderedDict.fromkeys(st.session_state.confirmed)))
            data = []  # format is {"id": "oct", "order": 10, "name": "Oct"}
            for index, code in enumerate(unique_confirmed):
                name = map_hazard_codes_to_names([code])[0]
                data.append({"id": code, "order": index, "name": name})
            st.write(f"Drag and drop the hazards to rank them in order of {option}.")

            slist = DraggableList(data, width="100%", key=f"draggable_list_{option}")

            if st.button(f'Export hazard {option} rankings', key=f'export_{option}'):
                json_data = json.dumps(slist)  # Convert your data to a JSON string
                st.download_button(
                    label="Download data as JSON",
                    data=json_data,
                    file_name=f'{option}_rankings.json',
                    mime='application/json',
                    key=f'download_{option}'
                )
        else:
            st.write("No hazards confirmed for ranking.")

# And then in your rank_buttons function or wherever you're calling rank_hazards from:
def rank_buttons():
    col1, col2 = st.columns(2)

    with col1:
        rank_hazards('occurrence')

    with col2:
        rank_hazards('impact')


def confusion():
    # button to get confused hazards
    if "confusion" not in st.session_state:
        # Make a POST request to the Google Cloud Function API
        api_url = os.environ.get("API_URL_CONFUSION")
        payload = {"hazardCodes": st.session_state.confirmed}
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            confusion_data = response.json()
            confusion_data.sort(key=lambda x: x["Hazard_Code"])  # Sort the list based on hazard_code
            confused_hazards = [hazard["Confused_Hazards"] for hazard in confusion_data]  # Create a list of confused_hazards
            st.session_state.confused = confused_hazards
            st.session_state.confusion = confusion_data
        else:
            st.error(f"Error fetching data. Status Code: {response.status_code}")
            return

def export_hazard_data():
    # button to export the hazard data
    if st.button('Export Data'):
        data_to_export = pd.DataFrame({
            'Hazard Code': st.session_state.confirmed,
            'Hazard Name': map_hazard_codes_to_names(st.session_state.confirmed)
        })
        st.download_button(
            label="Download data as CSV",
            data=data_to_export.to_csv(index=False),
            file_name='hazard_data.csv',
            mime='text/csv',
        )
        st.balloons()

def restart():
    # button to go back to report page
    st.write(" ")
    if st.button("🔄 New Report"):
        # Reset all session states
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.is_authenticated = True
        st.rerun()

def switch_model():
    # button to run same report with the other model
    st.write(" ")
    report = st.session_state.user_report
    model = st.session_state.classification_type
    if model == "ml":
        if st.button("🔄 Run with Rules Based Model"):
            # Reset the session states
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.is_authenticated = True
            st.session_state.in_report_submission = True
            st.session_state.user_report = report
            st.session_state.classification_type = "rules"
            st.rerun()
    else:
        if st.button("🔄 Run with LLM Based Model"):
            # Reset the session states
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.is_authenticated = True
            st.session_state.in_report_submission = True
            st.session_state.user_report = report
            st.session_state.classification_type = "ml"
            st.rerun()


def main():
    # Check if the user is logged in
    if "is_authenticated" not in st.session_state:
        st.session_state.is_authenticated = False

    # Display login page or the main content based on authentication status
    if st.session_state.is_authenticated:
        # Check the session state to determine which function to call
        if 'in_refined_question' in st.session_state and st.session_state.in_refined_question:
            refined_question()
        elif 'in_report_submission' in st.session_state and st.session_state.in_report_submission:
            question()
        else:
            if not st.session_state.in_classification_type:
                classification_type()
            else:
                user_report()
    else:
        login()

if __name__ == "__main__":
    main()