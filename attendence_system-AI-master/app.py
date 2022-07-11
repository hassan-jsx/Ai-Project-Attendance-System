import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from PIL import Image
import os
# import attendence.py as att
#adding a button

@st.cache
def load_image(image_file):
    img = Image.open(image_file)
    return img

with st.sidebar:
    selected = option_menu(
       menu_title="",#required
       options=["Upload Images","Open Camera","Open CSV"],#required
    )

if selected=="Open Camera":
    # execfile('att.py')
    os.system("python attendence.py")
    # print("Upload Images    and Open CSV files")
elif selected=='Open CSV':
    df = pd.read_csv("Attendance.csv") 
    st.title("Attendance File")
    st.write(df)
elif selected=='Upload Images':
    #upload multiple files to images f 
    image_file = st.file_uploader("uload an image",type=['png', 'jpg', 'jpeg'])
    if image_file is not None:
        fileDetails = {"FileNamw":image_file.name,"fileType":image_file.type}
        st.write(fileDetails)
        st.write(type(image_file))
        img=load_image(image_file)
        st.image(img,width=250)
        #saving file
        with open(os.path.join('images',image_file.name), 'wb') as f:
            f.write(image_file.getbuffer())
        
        st.success("file saved")

    