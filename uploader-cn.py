import streamlit as st

css = '''
<style>
[data-testid="stFileUploaderDropzone"] div div::before {content:"将文件拖放到此处"}
[data-testid="stFileUploaderDropzone"] div div span {display:none;}
[data-testid="stFileUploaderDropzone"] div div::after {color:rgba(49, 51, 63, 0.6); font-size: .8em; content:"每个文件限制 200MB • XLSX"}
[data-testid="stFileUploaderDropzone"] div div small{display:none;}
[data-testid="stFileUploaderDropzone"] [data-testid="baseButton-secondary"] { font-size: 0px;}
[data-testid="stFileUploaderDropzone"] [data-testid="baseButton-secondary"]::after {content: "浏览文件";  font-size: 17px;}
</style>
'''

st.markdown(css, unsafe_allow_html=True)

uploaded_file = st.file_uploader("上传 Excel 文件", type="xlsx")

