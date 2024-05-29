import streamlit as st
from streamlit_option_menu import option_menu

from langchain_community.chat_message_histories import StreamlitChatMessageHistory

from llm import ( 
    chain
)


from helpers.streamlit import (
    add_history_model,
    format_messages_to_db
)

if "chat_list" not in st.session_state:
    st.session_state.chat_list = []
    
if "messages_list" not in st.session_state:
    st.session_state.messages_list = []

if "disabled" not in st.session_state:
    st.session_state.disabled = True

if "chat_key" not in st.session_state:
    st.session_state.chat_key = ""


@st.experimental_dialog(title="Nome do Chat", width="small")
def define_chat_name():
    st.write("Qual sera o nome do novo chat?")
    chat_name = st.text_input("")
    if chat_name: 
        st.session_state.chat_list.append(chat_name)
        st.rerun()
    
# if not st.session_state.chat_list:
#     history = get_messages_db()
    
#     print(history)

#     for chats in history:
        
#         print(chats.chat_name)
        
#         st.session_state.chat_list.append(chats.chat_name)
#         messages_list = chats.chat_messages["messages"]
        
#         print(messages_list)
        
#         add_history_model(
#             messages_list=messages_list,
#             chat_history=StreamlitChatMessageHistory,
#             key=st.session_state.chat_list[-1]
#         )

msgs = StreamlitChatMessageHistory(key=st.session_state.chat_key)

with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        if add_button := st.button("Criar novo chat"):
            define_chat_name()
            
    with col2:
        if delete_button := st.button("Deletar chat"):            
            if st.session_state.chat_key:        
                msgs.clear()
                chat_name = st.session_state.chat_key    
                st.session_state.chat_list.remove(chat_name)
                st.session_state.chat_key = None
                # delete_in_db(chat_name)
    
    
    def get_chat_name():
        chat_name = st.session_state["text_input"]
        st.session_state.chat_list.append(chat_name)
        st.session_state["text_input"] = ""

    
    def get_chat_selection(key):
        st.session_state.chat_key = st.session_state[key]
    
    if st.session_state.chat_list:
        st.session_state.chat_key = st.session_state.chat_list[0]
        selected = option_menu(
            "Histórico", 
            st.session_state.chat_list,
            on_change=get_chat_selection, 
            key="chats",
            styles={
                "container": {"background-color": "rgb(38, 39, 48)"},        
                "icon": {"visibility": "hidden", "font-size": "0px"},
                "nav-item": {"padding": "5px 0 5px"},
            }
        )
        

if st.session_state.chat_key:
    for msg in msgs.messages:
        st.chat_message(msg.type).write(msg.content)

    if prompt := st.chat_input():        
        st.chat_message("human").markdown(prompt)
        
        config = {"configurable": {"session_id": "any"}}
        model_response = chain.invoke({"question": prompt, "history": msgs.messages}, config)
        
        st.chat_message("ai").markdown(model_response.content)
        
        msgs.add_user_message(prompt)
        msgs.add_ai_message(model_response.content)

        # update_in_db(st.session_state.chat_key, {"messages": format_messages_to_db(msgs)})