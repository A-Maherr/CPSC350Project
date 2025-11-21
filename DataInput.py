import streamlit as st
from openai import OpenAI
import json
from datetime import datetime
import io
from streamlit_date_picker import date_picker, PickerType
import time
from sqlalchemy import text
from streamlit_mic_recorder import mic_recorder

ALL_CATEGORIES = [
    "Housing",
    "Transportation",
    "Groceries",
    "Utilities",
    "Clothing",
    "Healthcare",
    "PersonalCare",
    "DebtPayments",
    "Miscellaneous",
]

def page_month():
    st.title("Data Input - Select Month")
    selected_month = date_picker(
            picker_type=PickerType.month,
            value=datetime.now(),
            key="month_picker"
            ) 
    if st.button("Next", width="stretch"):
        st.session_state.selected_month = selected_month
        st.session_state.page = "datainput_income"
        st.rerun()

def page_income():
    canProceed = False
    st.title(f"Data Input - Enter Income for the month {st.session_state.selected_month}")
    income = st.text_input("Total Monthly Income", placeholder=f"e.g., your total income for the month ", key="income_input")
    st.session_state.ValidationCounter = 0
    if income:
        if check_input(income): 
            canProceed = True
    if canProceed: 
        if st.button("Use AI", icon="👽", width="content"):
            st.session_state.user_income = income
            st.session_state.page = "AI_data_input"
            st.rerun()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back", width="stretch"):
            st.session_state.page = "datainput_month"
            st.rerun()
    with col2:
        if canProceed:
            if st.button("Next", width="stretch"):
                st.session_state.user_income = income
                st.session_state.page = "datainput_expenses"
                st.rerun()


def page_expenses():
    canProceed = False
    st.title(f"Data Input - Enter Expenses for the month {st.session_state.selected_month}")
    st.session_state.ValidationCounter = 0
    Housing = st.text_input("Housing", placeholder="e.g., monthly rent or mortgage payment", key="rent_input", value = st.session_state.get("Housing", ""))
    if Housing: 
        if check_input(Housing):   
            st.session_state.ValidationCounter += 1
            st.session_state.Housing = Housing
        else: st.session_state.ValidationCounter -= 1
    transportation = st.text_input("Transportation", placeholder="e.g., gas, public transit, rideshare", key="transportation_input", value = st.session_state.get("Transportation", ""))
    if transportation: 
        if check_input(transportation): 
            st.session_state.ValidationCounter += 1
            st.session_state.Transportation = transportation
        else: st.session_state.ValidationCounter -= 1
    groceries = st.text_input("Groceries", placeholder="e.g., food, household supplies", key="groceries_input", value = st.session_state.get("Groceries", ""))
    if groceries: 
        if check_input(groceries): 
            st.session_state.ValidationCounter += 1
            st.session_state.Groceries = groceries
        else: st.session_state.ValidationCounter -= 1
    utilities = st.text_input("Utilities", placeholder="e.g., electricity, water, internet", key="utilities_input", value = st.session_state.get("Utilities", ""))
    if utilities:  
        if check_input(utilities): 
            st.session_state.ValidationCounter += 1
            st.session_state.Utilities = utilities
        else: st.session_state.ValidationCounter -= 1
    Clothing = st.text_input("Clothing", placeholder="e.g., apparel, shoes, accessories", key="clothing_input", value = st.session_state.get("Clothing", ""))
    if Clothing: 
        if check_input(Clothing): 
            st.session_state.ValidationCounter += 1
            st.session_state.Clothing = Clothing
        else: st.session_state.ValidationCounter -= 1
    Healthcare = st.text_input("Healthcare", placeholder="e.g., medical bills, prescriptions, insurance", key="healthcare_input", value = st.session_state.get("Healthcare", ""))
    if Healthcare: 
        if check_input(Healthcare): 
            st.session_state.ValidationCounter += 1
            st.session_state.Healthcare = Healthcare
        else: st.session_state.ValidationCounter -= 1
    PersonalCare = st.text_input("Personal Care", placeholder="e.g., toiletries, grooming, wellness", key="personalcare_input", value = st.session_state.get("PersonalCare", ""))
    if PersonalCare: 
        if check_input(PersonalCare):
            st.session_state.ValidationCounter += 1
            st.session_state.PersonalCare = PersonalCare
        else: st.session_state.ValidationCounter -= 1
    DebtPayments = st.text_input("Debt Payments", placeholder="e.g., credit card, student loan, personal loan", key="debtpayments_input", value = st.session_state.get("DebtPayments", ""))
    if DebtPayments: 
        if check_input(DebtPayments): 
            st.session_state.ValidationCounter += 1
            st.session_state.DebtPayments = DebtPayments
        else: st.session_state.ValidationCounter -= 1
    Miscellaneous = st.text_input("Miscellaneous", placeholder="e.g., entertainment, dining out, subscriptions", key="miscellaneous_input", value = st.session_state.get("Miscellaneous", ""))
    if Miscellaneous: 
        if check_input(Miscellaneous): 
            st.session_state.ValidationCounter += 1
            st.session_state.Miscellaneous = Miscellaneous
        else: st.session_state.ValidationCounter -= 1
        
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back", width="stretch"):
            st.session_state.page = "datainput_income"
            st.rerun()
    with col2:
        if st.session_state.ValidationCounter == 9:
            if st.button("Next", width="stretch"):
                st.session_state.page = "datainput_summary"
                st.rerun()


def page_summary():
    st.title("Summary")

    
    st.write("Month:", st.session_state.selected_month)
    st.write("Income:", st.session_state.user_income)
    st.markdown("---")
    st.subheader("Expense Breakdown")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Housing:", st.session_state.Housing)
        st.write("Transportation:", st.session_state.Transportation)
        st.write("Groceries:", st.session_state.Groceries)
        st.write("Utilities:", st.session_state.Utilities)
        st.write("Clothing:", st.session_state.Clothing)

    with col2:
        st.write("Healthcare:", st.session_state.Healthcare)
        st.write("Personal Care:", st.session_state.PersonalCare)
        st.write("Debt Payments:", st.session_state.DebtPayments)
        st.write("Miscellaneous:", st.session_state.Miscellaneous)

    st.markdown("---")
    
    if st.button("Back"):
        st.session_state.page = "datainput_expenses"
        st.rerun() 
    if st.button("Submit"):
        conn = st.connection('dataset_db', type='sql') 
        income_insertion = text(f"INSERT INTO Income (user_id, monthly_income, date) VALUES ({st.session_state.user_id}, {st.session_state.user_income}, '{st.session_state.selected_month}');")
        Housing_insertion = text(f"INSERT INTO Expenses (user_id, type_id, amount, date) VALUES ({st.session_state.user_id}, 1, {st.session_state.Housing}, '{st.session_state.selected_month}');")
        Transportation_insertion = text(f"INSERT INTO Expenses (user_id, type_id, amount, date) VALUES ({st.session_state.user_id}, 2, {st.session_state.Transportation}, '{st.session_state.selected_month}');")
        Groceries_insertion = text(f"INSERT INTO Expenses (user_id, type_id, amount, date) VALUES ({st.session_state.user_id}, 3, {st.session_state.Groceries}, '{st.session_state.selected_month}');")
        Utilities_insertion = text(f"INSERT INTO Expenses (user_id, type_id, amount, date) VALUES ({st.session_state.user_id}, 4, {st.session_state.Utilities}, '{st.session_state.selected_month}');")
        Clothing_insertion = text(f"INSERT INTO Expenses (user_id, type_id, amount, date) VALUES ({st.session_state.user_id}, 5, {st.session_state.Clothing}, '{st.session_state.selected_month}');")
        Healthcare_insertion = text(f"INSERT INTO Expenses (user_id, type_id, amount, date) VALUES ({st.session_state.user_id}, 6, {st.session_state.Healthcare}, '{st.session_state.selected_month}');")
        PersonalCare_insertion = text(f"INSERT INTO Expenses (user_id, type_id, amount, date) VALUES ({st.session_state.user_id}, 7, {st.session_state.PersonalCare}, '{st.session_state.selected_month}');")
        DebtPayments_insertion = text(f"INSERT INTO Expenses (user_id, type_id, amount, date) VALUES ({st.session_state.user_id}, 8, {st.session_state.DebtPayments}, '{st.session_state.selected_month}');")
        Miscellaneous_insertion = text(f"INSERT INTO Expenses (user_id, type_id, amount, date) VALUES ({st.session_state.user_id}, 9, {st.session_state.Miscellaneous}, '{st.session_state.selected_month}');")

        with conn.session as s:
            if float(st.session_state.user_income) > 0:
                s.execute(income_insertion)
            if float(st.session_state.Housing) > 0:
                s.execute(Housing_insertion)
            if float(st.session_state.Transportation) > 0:
                s.execute(Transportation_insertion)
            if float(st.session_state.Groceries) > 0:
                s.execute(Groceries_insertion)
            if float(st.session_state.Utilities) > 0:
                s.execute(Utilities_insertion)
            if float(st.session_state.Clothing) > 0:
                s.execute(Clothing_insertion)
            if float(st.session_state.Healthcare) > 0:
                s.execute(Healthcare_insertion)
            if float(st.session_state.PersonalCare) > 0:
                s.execute(PersonalCare_insertion)
            if float(st.session_state.DebtPayments) > 0:
                s.execute(DebtPayments_insertion)
            if float(st.session_state.Miscellaneous) > 0:
                s.execute(Miscellaneous_insertion)
            s.commit()

        st.success("Data submitted successfully!")
        time.sleep(2)
        st.session_state.page = "dashboard"
        st.rerun()

def check_input(input):
    try:
        float(input)
        return True
    except ValueError:
        st.session_state.ValidationCounter -= 1
        st.error("Please enter a valid number.")
        return False
    

def AI_input_page():
    st.title(f"Data Input - AI Assistance for Month {st.session_state.selected_month}")

    if "ai_transcription" not in st.session_state:
        st.session_state.ai_transcription = ""

    user_input = st.text_area("Describe all your expenses for the month:", placeholder="e.g., I spent $1500 on rent, $300 on groceries...", value = st.session_state.ai_transcription)

    if "recording_mode" not in st.session_state:
        st.session_state.recording_mode = False

    if not st.session_state.recording_mode:
        if st.button("Use Speech-to-Text"):
            st.session_state.recording_mode = True

    if st.session_state.recording_mode is True:
        audio = mic_recorder(
            start_prompt="Start recording",
            stop_prompt="Stop recording",
            just_once=True,             
            use_container_width=False,  
            format="webm",               
            key="mic_recorder",
            )
        
        if audio is not None:
            audio_bytes = audio["bytes"]
            client = OpenAI(api_key=st.secrets["API_KEY"])
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = "recording.webm" 
            with st.spinner("Transcribing your recording with Whisper..."):
                transcript_obj = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                )
                transcript = transcript_obj.text

            st.session_state.ai_transcription = transcript
            st.session_state.recording_mode = False
            st.rerun()
    

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Use Manual Input", width="stretch"):
            st.session_state.page = "datainput_month"
            st.rerun()
    with col2:
        if "ai_missing_confirmed" not in st.session_state:
            st.session_state.ai_missing_confirmed = False
        if "ai_submit_pressed" not in st.session_state:
            st.session_state.ai_submit_pressed = False

        if st.button("Submit", width="stretch"): 
            st.session_state.ai_submit_pressed = True
            st.rerun()

        if st.session_state.ai_submit_pressed and not st.session_state.ai_missing_confirmed:
            data = parse_data(user_input)
            missing = [cat for cat in ALL_CATEGORIES if data.get(cat, 0) == 0]

            if len(missing) >= 4:
                st.warning(
                    "You may have missing categories:\n\n"
                    "Missing: **" + ", ".join(missing) + "**\n\n"
                    "Do you want to continue anyway?"
                )

                if st.button("Yes, this is everything", key="confirm_yes"):
                    st.session_state.ai_missing_confirmed = True
                    st.rerun()

                
                st.stop()

            else:
                st.session_state.ai_missing_confirmed = True
                st.rerun()


        if st.session_state.ai_missing_confirmed:
            with st.spinner("Processing your input..."):
                time.sleep(1)
                st.session_state.ai_transcription = " "
                st.success("Data parsed successfully!")
                st.session_state.ai_submit_pressed = False
                st.session_state.ai_missing_confirmed = False
                st.session_state.page = "datainput_summary"
                st.rerun()

            



def parse_data(user_text):
    client = OpenAI(api_key=st.secrets["API_KEY"])  
    
    system_prompt = """
    You are an expense extraction model. The user will send a paragraph describing things they spent money on. You must read the paragraph and extract the total spent for each of the following categories:

    1. Housing
    2. Transportation
    3. Groceries
    4. Utilities
    5. Clothing
    6. Healthcare
    7. Personal Care
    8. Debt Payments
    9. Miscellaneous

    Rules:
    - Extract monetary values ONLY from the user's paragraph.
    - If the user mentions multiple expenses in the same category, SUM them.
    - If the user does NOT mention a category, set its value to 0.
    - All values must be numbers only (no symbols, commas, or strings).
    - Output MUST BE valid JSON with these exact keys:

    {
      "Housing": 0,
      "Transportation": 0,
      "Groceries": 0,
      "Utilities": 0,
      "Clothing": 0,
      "Healthcare": 0,
      "PersonalCare": 0,
      "DebtPayments": 0,
      "Miscellaneous": 0
    }

    - NEVER output anything except this JSON object.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",   
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ],
        temperature=0
    )

    raw_output = response.choices[0].message.content
    data = json.loads(raw_output)


    st.session_state.Housing = data["Housing"]
    st.session_state.Transportation = data["Transportation"]
    st.session_state.Groceries = data["Groceries"]
    st.session_state.Utilities = data["Utilities"]
    st.session_state.Clothing = data["Clothing"]
    st.session_state.Healthcare = data["Healthcare"]
    st.session_state.PersonalCare = data["PersonalCare"]
    st.session_state.DebtPayments = data["DebtPayments"]
    st.session_state.Miscellaneous = data["Miscellaneous"]

    return data