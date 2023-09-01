import streamlit as st

def main():
    st.set_page_config(page_title="CariesGuard Predictor", page_icon="🦷", layout="wide")

    title_html = """
    <style>
    .title {
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 10px;
    }
    <div class="title">
        <h1>CariesGuard: Children's Oral Health Predictor</h1>
    </div>
    </style>
    """
    st.title("CariesGuard: Children's Oral Health Predictor")
    questions = [
        ("Is your kid using Fluoride Items (through drinking water, supplements,professional applications, toothpaste) ?",["My kid uses these products", "My kid does not use these products"]),
        ("Does your kid have sugary foods or drinks (including juice, carbonated or non-carbonated soft drinks, energy drinks, medicinal syrups)?",["Primarily at mealtimes", "Frequent or prolonged between meal exposures/day", "Bottle or sippy cup with anything other than water at bedtime"]),
        ("Is your kid eligible for Government Programs?", ["No", "Yes"]),
        ("Does Mother, Caregiver, and/or other Siblings have Experience of Caries?", ["No carious lesions in last 24 months", "Carious lesions in last 7-23 months", "Carious lesions in last 6 months"]),
        ("Does your kid does follow dental home: established patient of record in a dental office ?", ["my kid follows dental home", "my kid does not follow dental home"]),
        ("Does your kid have A Special Health Care Needs (developmental, physical, medical or mental disabilities that prevent or limit performance of adequate oral health care by themselves or caregivers)?", ["No", "Yes"]),
        ("Does your kid have Visual Evident Restorations/Cavitated Carious Lesions?", ["No new carious lesions or restorations in last 24 months", "Carious lesions or restorations in last 24 months"]),
        ("Does your Kid have Non-cavitated (incipient) Carious Lesions?", ["No new lesions in last 24 months", "New lesions in last 24 months"]),
        ("Does your kid have Visible Plaque?", ["NO", "My kid has"]),
        ("Does your kid use Dental/Orthodontic Appliances?", ["NO", "My kid uses dental/orthodontic appliances"])
    ]

    question_index = st.session_state.get("question_index", 0)
    answers = st.session_state.get("answers", [])

    if question_index < len(questions):
        question, options = questions[question_index]

        st.subheader(f"Question {question_index + 1}:")
        st.write(question)

        selected_option = st.radio(
            "Select an option:",
            options=options,
            key=f"question_{question_index}"
        )

        if selected_option == "Yes" and question_index == 0:
            st.session_state.question_index = len(questions)  # Skip to the end if high risk is selected
            display_result(["high risk"])
        elif selected_option == "high risk":
            st.session_state.question_index = len(questions)  # Skip to the end if high risk is selected
            display_result(["high risk"])
        elif st.button("Next"):
            answers.append(selected_option)
            question_index += 1

        st.session_state.question_index = question_index
        st.session_state.answers = answers

    if question_index >= len(questions):
        st.session_state.question_index = 0
        display_result(answers)

def display_result(answers):
    st.write("Thank you for answering the questions!")

    feedback = {
                "My kid does not use these products": "low risk", "My kid does not use these products": "moderate risk",
        "Primarily at mealtimes": "low risk", "Frequent or prolonged between meal exposures/day": "moderate risk",
        "Bottle or sippy cup with anything other than water at bedtime": "high risk","my kid follows dental home":"low risk",
        "my kid does not follow dental home":"moderate risk",
        "No": "low risk", "Yes": "high risk","My kid has":"moderate risk",
        "No carious lesions in last 24 months": "low risk", "Carious lesions in last 7-23 months": "moderate risk",
        "Carious lesions in last 6 months": "high risk",
        "No new carious lesions or restorations in last 24 months":"low risk",
        "Carious lesions or restorations in last 24 months": "high risk","My kid uses dental/orthodontic appliances":"moderate risk",
        "No new lesions in last 24 months": "low risk", "New lesions in last 24 months": "high risk",
    }

    risk_levels = {
        "low risk": 0,
        "moderate risk": 0,
        "high risk": 0
    }

    high_risk_selected = False

    for ans in answers:
        if ans in feedback:
            risk_levels[feedback[ans]] += 1
            if feedback[ans] == "high risk":
                high_risk_selected = True

    if high_risk_selected:
        most_common_risk = "high risk"
    else:
        most_common_risk = max(risk_levels, key=risk_levels.get)

    st.subheader("CariesGuard: Children's Oral Health Predictor Assessment Result")
    st.write(f"Based on your answers, your children have a {most_common_risk}.")

    selected_feedback = most_common_risk

    if selected_feedback == "high risk":
        advice = """
        1- recall every 3 months.
        2- Radiographs every 6 months.
        3-  Drink optimally fluoridated water (alternatively, take fluoride supplements with fluoride-deficient water supplies).
        4-  Twice daiy brushing with fluoridated toothpaste.
        5- professional topical treatment every 3 months.
        6- Silver diamine fluoride on cavitated lesions.
        """

    else:
        if selected_feedback == "low risk":
            advice ="""
            1- Recall every 6-12 months.
            2- Radiographs every 12-24 months.
            3- Drink optimally fluoridated water.
            4- Twice daily brushing with fluoridated toothpaste.
            """
        else:
            advice = """
            1- recall every 6 months.
            2- Radiographs every 6-12 months.
            3- Drink optimally fluoridated water (alternatively, take fluoride supplements with fluoride-deficient water supplies).
            4- Twice daiy brushing with fluoridated toothpaste.
            5- professional topical treatment every 3 months.
            """

    st.markdown(advice)

if __name__ == "__main__":
    main()
