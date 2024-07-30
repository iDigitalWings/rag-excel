import pandas as pd
import requests
import streamlit as st
from openai import OpenAI

api_key = '6DDGHVK-C9Q44NT-NGMVN8H-QG3086Y'

st.set_page_config(layout="wide")
st.title("AnythingLLM RAG EXCEL")

openai_base_url = "http://localhost:3001/api/v1/openai"

col1, col2 = st.columns(2)

apikey = col1.text_input('API KEY', type='password', value=api_key)

if apikey:
    client = OpenAI(
        api_key=api_key,
        base_url=openai_base_url,
    )

    # 定义URL和头信息
    url = 'http://127.0.0.1:3001/api/v1/workspaces'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + apikey
    }
    print(apikey)

    # 发送GET请求
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        workspaces = {}
        for workspace in data['workspaces']:
            workspaces[workspace['slug']] = workspace['name']
        model = col2.selectbox("Workspaces", workspaces.keys(), format_func=lambda x: workspaces[x])
    else:
        st.error(f"Request failed with status code {response.status_code}")

uploaded_file = st.file_uploader("Upload an Excel file")

rag = st.button('RAG', use_container_width=True, type='primary',
                # disabled=not apikey or not model or not uploaded_file
                )


def chat(model_select, prompt):
    print(prompt)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model_select,
        temperature=0.7,
        stream=True,
    )
    for completion in chat_completion:
        print(completion.choices[0].delta.content)
        yield completion.choices[0].delta.content


col_grid, col_reply = st.columns([2, 1])
area_grid = col_grid.empty()
area_reply = col_reply.empty()


@st.cache_data
def get_df():
    return pd.read_excel(uploaded_file, header=0, skiprows=1)


if uploaded_file is not None:
    df = get_df()
    area_grid.data_editor(df, use_container_width=True)

name_desc = '需求描述'
name_reply = '应答'

if rag:
    print('RAGing...')
    if apikey and model and uploaded_file:
        processed = []
        for idx, row in df.iterrows():
            condition = row[name_desc]
            if condition and type(condition) == str:
                print('>>>', condition)


                def row_bg(row):
                    index = row.name
                    if index == idx:
                        return ['background-color: #ffffb8'] * len(row)
                    elif index in processed:
                        return ['background-color: #d9f7be'] * len(row)
                    else:
                        return [''] * len(row)


                area_grid.dataframe(
                    df.style.apply(
                        row_bg, subset=(processed + [idx], slice(None),),
                        axis=1
                    ),
                    use_container_width=True,
                )

                reply = ''
                for xx in chat(model, condition):
                    reply = reply + xx
                    area_reply.success(reply)
                df.loc[idx, name_reply] = reply
                processed.append(idx)

                area_grid.dataframe(use_container_width=True, data=df)

    elif not apikey:
        st.error('Please enter your API key.')
    elif not model:
        st.error('Please select a model.')
    elif not uploaded_file:
        st.error('Please upload an Excel file.')
