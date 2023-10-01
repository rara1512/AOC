# Import Modeules
import streamlit as st
import base64
from pathlib import Path
from PIL import Image
import pandas as pd
import plotly.express as px

# Set path for images and data
Image_path = Path(__file__).parent.absolute() / "Images"
Data_path = Path(__file__).parent.absolute() / "Data"

# Sidebar and its contents
BackGround = Image.open(Image_path / "Logo.PNG")
st.sidebar. image(BackGround)
st.sidebar.title("About")
st.sidebar.write("Web App For [Atoms of Confusion]""(https://atomsofconfusion.com/).")

# Setting web-app title
st.title("Atoms of Confusion")

# Reading data
atoms_data = pd.read_csv(Data_path / "atom-context_2018-10-12_parent-type.csv")
atom_counts = pd.read_csv(Data_path / "atom_counts.csv")

# Pie chart for atom distribution
atom_dist = px.pie(atom_counts, names = "atom", values = "count", title = "Atoms and its distribution")
st.plotly_chart(atom_dist, use_container_width=True)

# Filter Widget for the data
with st.expander("Apply filters"):
    atom_list = list(atoms_data["atom"].unique())
    # file_list = ['linux', 'FreeBSD' , 'Gecko', 'WebKit', 'GCC', 'Clang', 'MongoDB', 'MySQL', 'Subversion', 'Git', 'Emacs', 'Vim', 'Nginx']
    atom_selected = st.selectbox("Select a type of atom?", atom_list)
    selected_atom_df = atoms_data[atoms_data['atom']==atom_selected]
    st.write("[Detailed Atom Description]""(https://atomsofconfusion.com/data.html#literal-encoding)")

# Filtered Charts
node_type_rows = st.slider('How many node-types would you like to see?', 0, len(selected_atom_df["node-type"].value_counts()), 1)
selected_atom_df = selected_atom_df["node-type"].value_counts().to_frame().reset_index().rename(columns = {'index':'node-type'}).head(node_type_rows)
node_type_chart = px.bar(selected_atom_df, x='node-type', y='count', title=f"node-type and its count for {atom_selected}")
st.plotly_chart(node_type_chart, use_container_width=True)

parent_type_rows = st.slider('How many parent-types would you like to see?', 0, len(selected_atom_df["parent-type"].value_counts()), 1)
parent_type_chart = px.bar(selected_atom_df["parent-type"].value_counts().to_frame().reset_index().rename(columns = {'index':'parent-type'}).head(parent_type_rows), x='parent-type', y='count', title=f"parent-type and its count for {atom_selected}")
st.plotly_chart(parent_type_chart, use_container_width=True)