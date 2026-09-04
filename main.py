import streamlit as st
st.title("Welcome to my application")
# 1. กำหนดค่าเริ่มต้นใน session_state ถ้ายังไม่มี
if "" not in st.session_state:
    st.session_state.ans1_val = ""
if "ans2_val" not in st.session_state:
    st.session_state.ans2_val = ""
if "ans3_val" not in st.session_state:
    st.session_state.ans3_val = ""
if "ans4_val" not in st.session_state:
    st.session_state.ans4_val = ""


st.divider()

# 3. ช่องรับคำตอบ (ใช้ value ผูกกับตัวแปรตรงๆ เพื่อสั่งเคลียร์ได้)
product1 = st.text_input(
    "รายการ",
    value=st.session_state.ans1_val,
)
product2 = st.text_input(
    "ข้อ 2: Cats love to eat `f _ s h`. 🐟",
    value=st.session_state.ans2_val,
)
product3 = st.text_input(
    "ข้อ 3: Monkey love to eat `b a _ _ n a`. 🍌",
    value=st.session_state.ans3_val,
)
product4 = st.text_input(
    "ข้อ 4: Students must use a `p _ n`. 🖊️",
    value=st.session_state.ans4_val,
)

st.header(f"ค่า BMI ของคุณคือ: **{product4}**")
