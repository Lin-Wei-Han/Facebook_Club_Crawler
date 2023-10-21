import streamlit as st
from streamlit_option_menu import option_menu

st.title('Facebook 美食社團分析')

selected = option_menu(
    menu_title = None,
    options = ['Home', 'Text Cloud', 'Contact'],
    icons = ['house', 'book', 'envelope'],
    menu_icon = 'cast',
    default_index = 0,
    orientation = 'horizontal'
)

if selected == 'Home':
    st.title('Facebook 美食社團分析')
if selected == 'Text Cloud':
    st.title('Facebook')
if selected == 'Contact':
    st.title('Facebook Contact')