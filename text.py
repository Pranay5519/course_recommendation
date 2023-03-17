import pandas as pd
import pickle
import streamlit as st
import numpy as np
import sklearn


image = 'https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/https://coursera.s3.amazonaws.com/media/coursera-rebrand-logo-square.png'
df = pd.read_csv(r"C:\Users\HP\Downloads\course_rec_data_2.csv")
del df['Unnamed: 0']
knn_model = pickle.load(open(r"C:\Users\HP\Downloads\knn_model_coursera.pkl",'rb'))
vectorizer= pickle.load(open(r"C:\Users\HP\Downloads\vetorizer.pkl",'rb'))
def recommend_courses(course_name,num_recommendations=6):
    indices = df[(df['Course Name'] == course_name)].index

    if len(indices) == 0:
        return 'No course found!'
    idx = indices[0]

    query_vector = vectorizer[idx]

    distances, indices = knn_model.kneighbors(query_vector, n_neighbors=num_recommendations+1) # get the indices of the recommended courses
    indices = indices.squeeze()[1:]


    return df.iloc[indices][['Course Name','Course Description', 'University', 'Difficulty Level', 'Course Rating', 'Course URL','Skills']]


st.title("Coursera Course Recommendation")

course_name  = st.selectbox('Select Course',df['Course Name'].unique())
if st.button("Recommend"):


    data = recommend_courses(course_name)
    data = data.reset_index(drop=True)

    nu_rows = 2
    nu_col = 3
    x = 0
    for i in range(nu_rows):
        cols = st.columns(nu_col)
        for j in range(nu_col):
            cols[j].image(image, width=140)
            cols[j].subheader(data['Course Name'][x])
            cols[j].markdown(data['University'][x])
            cols[j].write(data['Difficulty Level'][x])
            cols[j].caption(data['Course URL'][x])
            cols[j].write(f"Rating: {data['Course Rating'][x]}")
            cols[j].write(data['Skills'][x])
            x += 1