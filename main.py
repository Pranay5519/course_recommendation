import pandas as pd
import pickle
import streamlit as st
import numpy as np

image = 'https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/https://coursera.s3.amazonaws.com/media/coursera-rebrand-logo-square.png'
df = pd.read_csv('data_no_dupli_index_reset.csv')
del df['Unnamed: 0']
cosine = pickle.load(open('cosine_similarity.pkl','rb'))

recommended_list = []
def recommend(title):
    print(title)
    index = df[df['Course Name'] == title].index[0]
    distances = cosine[index]
    course_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]
    for x in course_list:
        name = df['Course Name'].iloc[x[0]]
        recommended_list.append(name)

    return recommended_list
st.title("Coursera Course Recommendation")

course_name  = st.selectbox('Select Course',df['Course Name'].unique())
if st.button("Recommend"):


    course_list = recommend(course_name)
    index = []
    for x in course_list:
        index.append(np.where(df['Course Name'] == x))

    index = [tup[0][0] for tup in index]
    data  = df.loc[index]
    data = data.reset_index(drop = True)
    nu_rows = 2
    nu_col = 3
    x = 0
    for i in range(nu_rows):
        cols = st.columns(nu_col)
        for j in range(nu_col):
            cols[j].image(image,width=140)
            cols[j].subheader(data['Course Name'][x])
            cols[j].markdown(data['University'][x])
            cols[j].write(data['Difficulty Level'][x])
            cols[j].caption(data['Course URL'][x])
            cols[j].write(f"Rating: {data['Course Rating'][x]}")
            cols[j].write(data['Skills'][x])
            x += 1

