import streamlit as st
st.set_page_config(
    page_title="Diabetes Risk Prediction",
    page_icon="💊",
    layout="centered",
)

import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents_src.crew import diabetes_prediction_crew
from agents_src.tools.diabetes_prediction_tool import predict_diabetes_core

st.title("⚕️Diabetes Risk Prediction")

st.write("Enter patient data to predict diabetes risk.")

with st.form("patient_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=1)
        glucose = st.number_input("Glucose", min_value=0, max_value=300, value=100)
        blood_pressure = st.number_input("Blood Pressure", min_value=0, max_value=200, value=70)
    with col2:
        skin_thickness = st.number_input("Skin Thickness", min_value=0, max_value=99, value=20)
        insulin = st.number_input("Insulin", min_value=0, max_value=900, value=85)
        bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=22.5)
    with col3:
        diabetes_pedigree = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=2.5, value=0.2)
        age = st.number_input("Age", min_value=0, max_value=120, value=25)
    submitted = st.form_submit_button("Predict")

if submitted:
    patient_data = {
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": blood_pressure,
        "SkinThickness": skin_thickness,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigreeFunction": diabetes_pedigree,
        "Age": age
    }
    prediction = predict_diabetes_core(patient_data)
    result = diabetes_prediction_crew.kickoff(
        inputs={
            "patient_data": json.dumps(patient_data),
            "prediction_result": json.dumps(prediction),
        }
    )
    diabetes_pred_dict = result.to_dict()
    diabetes_pred = diabetes_pred_dict.get("diabetes_risk_prediction", {})

    colA, colB = st.columns(2)
    with colA:
        st.subheader("Result")
        st.metric(label="Diabetes Risk", value=diabetes_pred.get('result', 'N/A'))
    with colB:
        st.subheader("Probability Diabetic")
        st.metric(label="Probability", value=diabetes_pred.get('probability_diabetic', 'N/A'))

    st.subheader("Summary")
    st.success(diabetes_pred.get('test_result_natural_language', 'N/A'))

    st.subheader("Explanation")
    if diabetes_pred_dict.get("explanation", []):
        st.table({"Explanation": diabetes_pred_dict.get("explanation", [])})
    else:
        st.write("No explanation available.")

    st.subheader("Actionable Health Advice")
    if diabetes_pred_dict.get("actionable_health_advice", []):
        st.table({"Advice": diabetes_pred_dict.get("actionable_health_advice", [])})
    else:
        st.write("No advice available.")

    with st.expander("Raw Tool Output"):
        st.json(diabetes_pred_dict.get("tool_output", {}))








# import streamlit as st
# import sys
# import os
# import json

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from database.mongo import get_db 
# from agents_src.crew import diabetes_prediction_crew
# from agents_src.tools.diabetes_prediction_tool import predict_diabetes_core

# st.set_page_config(
#     page_title="Diabetes Risk Prediction",
#     page_icon="💊",
#     layout="centered",
# )

# db = get_db()
# users_col = db["patients"]  # collection for auth

# # ---------- SESSION STATE ----------
# if "auth_page" not in st.session_state:
#     st.session_state.auth_page = "choice"  # "choice" | "signin" | "signup"
# if "user" not in st.session_state:
#     st.session_state.user = None          # store logged-in patient_id

# # ---------- PAGE CHOICE ----------
# if st.session_state.user is None:
#     # Not logged in -> show auth flow
#     if st.session_state.auth_page == "choice":
#         st.title("Diabetes Risk Prediction")

#         col_left, col_mid, col_right = st.columns([1, 2, 1])
#         with col_mid:
#             b1, b2 = st.columns(2)
#             with b1:
#                 if st.button("Sign in", use_container_width=True):
#                     st.session_state.auth_page = "signin"
#                     st.rerun()
#             with b2:
#                 if st.button("Sign up", use_container_width=True):
#                     st.session_state.auth_page = "signup"
#                     st.rerun()

#     elif st.session_state.auth_page == "signin":
#         st.title("Sign in")

#         with st.form("signin_form"):
#             patient_id = st.text_input("Patient ID")
#             password = st.text_input("Password", type="password")
#             submitted = st.form_submit_button("Sign in")

#         if submitted:
#             user = users_col.find_one(
#                 {"patient_id": patient_id, "password": password}
#             )
#             if user:
#                 st.session_state.user = patient_id
#                 st.success(f"Signed in as {patient_id}")
#                 st.session_state.auth_page = "choice"
#                 st.rerun()
#             else:
#                 st.error("Invalid Patient ID or Password")

#     elif st.session_state.auth_page == "signup":
#         st.title("Sign up")

#         with st.form("signup_form"):
#             patient_id = st.text_input("Patient ID")
#             password = st.text_input("Password", type="password")
#             confirm_password = st.text_input("Confirm Password", type="password")
#             submitted = st.form_submit_button("Create account")

#         if submitted:
#             if password != confirm_password:
#                 st.error("Passwords do not match")
#             else:
#                 # check if user exists
#                 existing = users_col.find_one({"patient_id": patient_id})
#                 if existing:
#                     st.error("Patient ID already exists")
#                 else:
#                     users_col.insert_one(
#                         {"patient_id": patient_id, "password": password}
#                     )
#                     st.success("Sign up successful. Please sign in.")
#                     st.session_state.auth_page = "signin"
#                     st.rerun()

# # ---------- MAIN APP (ONLY WHEN LOGGED IN) ----------
# if st.session_state.user is not None:
#     st.title("⚕️Diabetes Risk Prediction")
#     st.write(f"Logged in as **{st.session_state.user}**")

#     with st.form("patient_form"):
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=1)
#             glucose = st.number_input("Glucose", min_value=0, max_value=300, value=100)
#             blood_pressure = st.number_input("Blood Pressure", min_value=0, max_value=200, value=70)
#         with col2:
#             skin_thickness = st.number_input("Skin Thickness", min_value=0, max_value=99, value=20)
#             insulin = st.number_input("Insulin", min_value=0, max_value=900, value=85)
#             bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=22.5)
#         with col3:
#             diabetes_pedigree = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=2.5, value=0.2)
#             age = st.number_input("Age", min_value=0, max_value=120, value=25)
#         submitted = st.form_submit_button("Predict")

#     if submitted:
#         patient_data = {
#             "Pregnancies": pregnancies,
#             "Glucose": glucose,
#             "BloodPressure": blood_pressure,
#             "SkinThickness": skin_thickness,
#             "Insulin": insulin,
#             "BMI": bmi,
#             "DiabetesPedigreeFunction": diabetes_pedigree,
#             "Age": age
#         }
#         prediction = predict_diabetes_core(patient_data)
#         result = diabetes_prediction_crew.kickoff(
#             inputs={
#                 "patient_data": json.dumps(patient_data),
#                 "prediction_result": json.dumps(prediction),
#             }
#         )
#         diabetes_pred_dict = result.to_dict()
#         diabetes_pred = diabetes_pred_dict.get("diabetes_risk_prediction", {})

#         colA, colB = st.columns(2)
#         with colA:
#             st.subheader("Result")
#             st.metric(label="Diabetes Risk", value=diabetes_pred.get('result', 'N/A'))
#         with colB:
#             st.subheader("Probability Diabetic")
#             st.metric(label="Probability", value=diabetes_pred.get('probability_diabetic', 'N/A'))

#         st.subheader("Summary")
#         st.success(diabetes_pred.get('test_result_natural_language', 'N/A'))

#         st.subheader("Explanation")
#         if diabetes_pred_dict.get("explanation", []):
#             st.table({"Explanation": diabetes_pred_dict.get("explanation", [])})
#         else:
#             st.write("No explanation available.")

#         st.subheader("Actionable Health Advice")
#         if diabetes_pred_dict.get("actionable_health_advice", []):
#             st.table({"Advice": diabetes_pred_dict.get("actionable_health_advice", [])})
#         else:
#             st.write("No advice available.")