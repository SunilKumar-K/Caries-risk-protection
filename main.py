import streamlit as st

def main():
    st.title("Caries Risk Assessment")

    questions = [
        ("Is your kid using Fluoride Items?",["Yes", "No"]),
        ("Does your kid have Sugary Foods or Drinks?",["Primarily at mealtimes", "Frequent or prolonged between meal exposures/day", "Bottle or sippy cup with anything other than water at bedtime"]),
        ("Is your kid eligible for Government Programs?", ["No", "Yes"]),
        ("Does Mother, Caregiver, and/or other Siblings have Experience of Caries?", ["No carious lesions in last 24 months", "Carious lesions in last 7-23 months", "Carious lesions in last 6 months"]),
        ("Does your kid follow Dental Home?", ["Yes", "No"]),
        ("Does your kid have Special Health Care Needs?", ["No", "Yes"]),
        ("Does your kid have Visual Evident Restorations/Cavitated Carious Lesions?", ["No new carious lesions or restorations in last 24 months", "Carious lesions or restorations in last 24 months"]),
        ("Does your Kid have Non-cavitated (incipient) Carious Lesions?", ["No new lesions in last 24 months", "New lesions in last 24 months"]),
        ("Does your kid have Visible Plaque?", ["NO", "Yes"]),
        ("Does your kid use Dental/Orthodontic Appliances?", ["NO", "Yes"])
    ]

    question_index = st.session_state.get("question_index", 0)
    answers = st.session_state.get("answers", [])

    if question_index < len(questions):
        question, options = questions[question_index]

        st.subheader(f"Question {question_index + 1}:")
        st.write(question)

        selected_option = st.selectbox("Select an option:", options, key=f"question_{question_index}")

        if st.button("Next"):
            answers.append(selected_option)
            question_index += 1

        st.session_state.question_index = question_index
        st.session_state.answers = answers

    if question_index > 0:
        if st.button("Back"):
            question_index -= 1
            st.session_state.question_index = question_index

    if question_index >= len(questions):
        st.session_state.question_index = 0
        display_result(answers)

def display_result(answers):
    st.write("Thank you for answering the questions!")

    feedback = {
        "Yes": "low risk", "No": "moderate risk",
        "Primarily at mealtimes": "low risk", "Frequent or prolonged between meal exposures/day": "moderate risk",
        "Bottle or sippy cup with anything other than water at bedtime": "high risk",
        "No": "low risk", "Yes": "high risk",
        "No carious lesions in last 24 months": "low risk", "Carious lesions in last 7-23 months": "moderate risk",
        "Carious lesions in last 6 months": "high risk",
        "Yes": "low risk", "No": "moderate risk",
        "No": "low risk", "Yes": "moderate risk",
        "No new carious lesions or restorations in last 24 months": "low risk",
        "Carious lesions or restorations in last 24 months": "high risk",
        "No new lesions in last 24 months": "low risk", "New lesions in last 24 months": "high risk",
        "NO": "low risk", "Yes": "moderate risk",
        "NO": "low risk", "Yes": "moderate risk"
    }

    risk_levels = {
        "low risk": 0,
        "moderate risk": 0,
        "high risk": 0
    }

    for ans in answers:
        if ans in feedback:
            risk_levels[feedback[ans]] += 1

    most_common_risk = max(risk_levels, key=risk_levels.get)
    st.subheader("Risk Assessment Result")
    st.write(f"Based on your answers, you have a {most_common_risk}.")

    if most_common_risk == "high risk":
        st.write("You are advised to consult a doctor for further guidance.")
    else:
        if most_common_risk == "low risk":
            st.write("You are at low risk. Continue maintaining good oral health.")
        else:
            st.write("You are at moderate risk. Consider taking extra precautions for oral health.")

if __name__ == "__main__":
    main()
