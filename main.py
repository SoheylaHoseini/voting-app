import streamlit as st
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

worksheet_name = "Sheet2"

if 'data' not in st.session_state:
    st.session_state.data = conn.read(worksheet=worksheet_name)
    st.session_state.names = st.session_state.data['Name'].tolist()
    st.session_state.votes = st.session_state.data['Votes'].fillna(0).astype(int).tolist()

st.title("رای‌گیری")

selected_name = st.selectbox("به یک اسم رای بدهید:", st.session_state.names)

if st.button("رای بده"):
    index = st.session_state.names.index(selected_name)
    st.session_state.votes[index] += 1

    st.session_state.data.at[index, 'Votes'] = st.session_state.votes[index]

    conn.update(data=st.session_state.data, worksheet=worksheet_name)
    st.success(f"رای شما به {selected_name} ثبت شد!")

st.subheader("نتایج رای‌گیری")
st.write("نام", "رای")
for name, vote in zip(st.session_state.names, st.session_state.votes):
    st.write(name, vote)
