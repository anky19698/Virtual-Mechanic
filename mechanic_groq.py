import streamlit as st
from langchain_groq import ChatGroq
import os


def get_model(selected_model_name):
    groq_api_key = st.secrets['groq_api_key']
    os.environ['GROQ_API_KEY'] = groq_api_key

    model_name = selected_model_name

    model = ChatGroq(
        model=model_name
    )
    return model 

def get_examples():
    few_shot_examples = [
    {
        "symptom": "Engine is making a knocking noise",
        "action": "The knocking noise could indicate a problem with the engine bearings or low oil levels. First, check the oil level. If the oil is low, top it up with the correct grade. If the noise persists after adding oil, take the car to a mechanic for further inspection."
    },
    {
        "symptom": "Car is pulling to one side while driving",
        "action": "This could be due to uneven tire pressure, misaligned wheels, or brake issues. Start by checking the tire pressure on all four tires and ensure they are at the recommended levels. If the problem continues, have your wheel alignment checked by a professional. If alignment is correct and the issue persists, inspect the brakes."
    },
    {
        "symptom": "Brakes are squeaking loudly",
        "action": "Squeaky brakes could be due to worn-out brake pads or moisture on the brake rotors. First, inspect the brake pads to see if they need replacing. If the pads are fine, drive the car for a short distance to see if the noise goes away as moisture evaporates. If the noise continues, take the car to a mechanic to have the brakes inspected."
    },
    {
        "symptom": "Car won't start, and there's a clicking noise when you turn the key",
        "action": "This could be a result of a dead battery or a faulty starter motor. First, check the battery terminals for corrosion and ensure they are tight. Try jump-starting the car. If the car starts, have the battery and alternator tested to ensure they are functioning properly. If the car doesn't start after jump-starting, the starter motor might need replacing."
    },
    {
        "symptom": "Excessive smoke coming from the exhaust",
        "action": "Excessive smoke could indicate burning oil, a clogged air filter, or engine overheating. Start by checking the oil level and top up if necessary. Then, inspect the air filter and replace it if it's dirty. Finally, check the coolant level and ensure the radiator fan is working properly. If the smoke continues after these checks, take the car to a mechanic for a more thorough inspection."
    }
]

    return few_shot_examples

def get_llm_models():
    models = {
        'Llama 3.1 70B': 'llama-3.1-70b-versatile',
        'Mixtral 8x7B': 'mixtral-8x7b-32768',
        'Llama 3.1 8B': 'llama-3.1-8b-instant',
        'Meta Llama 3 70B': 'llama3-70b-8192',
        'Gemma 7B': 'gemma-7b-it',
        'Gemma 2 9B': 'gemma2-9b-it'
    }
    return models


def generate_response(query, model, chat_history):
    # Chat History
    try:
        recent_history = chat_history[-5:]
        history_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in recent_history])
    except:
        history_text = ""

    prompt = f"""
    You are a Virtual Mechanic Assitant. 
    Your Task is to Answer the Mechanical Queries of User. 
    User will tell context and symptoms based on that Suggest Actions to User based on their Query.
    Always Use Polite Tone and Be As Helpful as You can. Give Concise Answer.

    Here are Some Few Shot Examples to Structure the Response:
    {get_examples()}

    symptom: {query}

    action: """

    # Groq Syntax
    # system_prompt = f"""
    #     You are a Virtual Mechanic Assitant. 
    #     Your Task is to Answer the Mechanical Queries of User. 
    #     User will tell context and symptoms based on that Suggest Actions to User based on their Query.
    #     Always Use Polite Tone and Be As Helpful as You can. Give Consise Answer.

    #     Here are Some Few Shot Examples to Structure the Response:
    #     {get_examples()}
    # """
    
    # messages = [
    #     ('system', system_prompt),
    #     ('symptom', query),
    # ]

    response = model.invoke(prompt)

    return response.content


def main():
    

    # Streamlit App
    st.title(":hammer_and_wrench: Virtual Mechanic Assistant:male-mechanic: ")

    # Model Selection
    selected_model = st.sidebar.selectbox("Select LLM Model", options=list(get_llm_models().keys()), index=0)

    # Get Model
    models_dict = get_llm_models()
    model = get_model(selected_model_name=models_dict[selected_model])

    print("Current Model:", selected_model)

    # Initialize chat history in session state if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Display chat history
    for i, message in enumerate(st.session_state.chat_history):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input at the bottom
    user_question = st.chat_input("Ask a Question about Unusual Car Symptoms:")

    if user_question:
        # Add user question to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_question})

        # Display user question
        with st.chat_message("user", avatar="🙋‍♂️"):
            st.markdown(user_question)

        # Generate and display AI response
        with st.chat_message("assistant", avatar="👨‍🔧"):
            with st.spinner("Virtual Mechanic is Thinking..."):

                try:
                    response = generate_response(query=user_question, model=model, chat_history=st.session_state.chat_history)
                    st.write(response)

                    # Add assistant response to chat history
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                except:
                    st.error("Can't Find Any Solution, Please Consult a Real Mechanic")



if __name__ == '__main__':
    main()
