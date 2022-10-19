from distutils.command.build_scripts import first_line_re
import streamlit as st
from record import start_record, stop_record
from analyse import analyse
from test import get_person_name, start_auth, stop_auth

recording = False

st.write("# Multi-factor Authentication System")
start_auth()

# Record typing style
st.write("## Record typing style")
username = st.text_input("Username")
username_err = st.empty()
if st.button("Start recording"):
    if username.strip() == "":
        username_err.error("Please enter a username")
    else:
        start_record()
        stop_auth()
        recording = True
st.text_area(
    "Please type the following text: *The quick brown fox jumps over the lazy dog.*",
    height=100,
    disabled=(not recording),
)
# print(username)


if st.button("Stop recording"):
    stop_record(username)
    recording = False
    analyse()
    start_auth()

# Authenticate using typing style
st.write("## Authenticate using typing style")
auth_text = st.text_area("Please type here", disabled=recording)
# if auth_text != "":
col1, col2 = st.columns([1, 5])
b1 = None
b2 = None
with col1:
    b1 = st.empty()

with col2:
    b2 = st.empty()

if b1.button("Authenticate"):
    new_user = get_person_name()
    if new_user != "":
        st.write(f"User: **{new_user}**")
    else:
        st.write(f"User: **Unknown**")

if b2.button("Reset Authentication"):
    stop_auth()
    start_auth()
    new_user = "Unknown"
