import streamlit as st
from src.core.learn_info import run

st.title("DEMO")

# Session state to store data
session_state = st.session_state

# Input text
mssv = st.text_input("MSSV")
password = st.text_input("Password", type="password")
data = None

# Button
if st.button("Submit"):
    with st.spinner('Đang lấy dữ liệu...'):
        session_state['data'] = run(mssv, password)
        st.success('Lấy dữ liệu thành công!')

data = session_state.get('data', None)

if data is None:
    st.stop()
    
student_info = data['student_info']
score_by_semester = data['score_by_semester']
credits_info = data['credits_info']
        
st.write(f'Họ và tên: {student_info["name"]}')
st.write(f'MSSV: {student_info["mssv"]}')

st.write(f'Số tín chỉ tích lũy: {credits_info["so_tc_tich_luy"]}')
st.write(f'Số tín chỉ đạt: {credits_info["so_tc_dat"]}')
st.write(f'Điểm trung bình tích lũy: {credits_info["diem_tb_tich_luy"]}')

# Show score by semester
st.write('---', unsafe_allow_html=True)
list_semester = list(data['score_by_semester'].keys())
st.subheader('Điểm học phần')
semester = st.selectbox('Mã học kỳ', list_semester)

# Show score
choosen_semester_data = data['score_by_semester'][semester]
st.write(f'Mã học kỳ: {semester} (Học kì {semester[-1]} năm học 20{semester[:2]} - 20{str(int(semester[:2])+1)})')

# Search ma_hp
list_ma_hp_in_semester = list([x['ma_hp'] for x in choosen_semester_data])

ma_hp = st.selectbox('Mã học phần', list_ma_hp_in_semester)

# Show score
for hp in choosen_semester_data:
    if hp['ma_hp'] == ma_hp:
        st.write(f'Tên học phần: {hp["ten_hp"]}')
        st.write(f'Số tín chỉ: {hp["so_tc"]}')
        st.write(f'Điểm hệ 10: {hp["diem_he_10"]}')
        st.write(f'Điểm chữ: {hp["diem_chu"]}')
        break
