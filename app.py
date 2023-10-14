# Import Modeules
import streamlit as st
import base64
from pathlib import Path
from PIL import Image
import pandas as pd
import plotly.express as px
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

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
atom_file_occurrence = pd.read_csv(Data_path / "atom_file_count.csv")
pair_means = pd.read_csv(Data_path / "atom_pair_distance.csv")

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
node_type_df = selected_atom_df["node-type"].value_counts().to_frame().reset_index().rename(columns = {'index':'node-type'}).head(node_type_rows)
node_type_chart = px.bar(node_type_df, x='node-type', y='count', title=f"node-type and its count for {atom_selected}")
st.plotly_chart(node_type_chart, use_container_width=True)

parent_type_rows = st.slider('How many parent-types would you like to see?', 0, len(selected_atom_df["parent-type"].value_counts()), 1)
parent_type_df = selected_atom_df["parent-type"].value_counts().to_frame().reset_index().rename(columns = {'index':'parent-type'}).head(parent_type_rows)
parent_type_chart = px.bar(parent_type_df, x='parent-type', y='count', title=f"parent-type and its count for {atom_selected}")
st.plotly_chart(parent_type_chart, use_container_width=True)

#Network graph
selected_atom_distance_df = pair_means[pair_means["atom1"] == atom_selected]

G = nx.Graph()
for index, row in selected_atom_distance_df.iterrows():
    node1, node2, distance = row["atom1"], row["atom2"], row["distance"]
    G.add_edge(node1, node2, weight=distance)

pos = nx.spring_layout(G, seed=42)

# Filter edges with weight below a certain threshold

fig, ax = plt.subplots(figsize=(14, 8)) 
threshold = 5
filtered_edges = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] >= threshold]

# Create a legend mapping edge colors to distances
edge_colors = [d['weight'] for u, v, d in G.edges(data=True)]
cmap = plt.get_cmap('viridis')  # Choose a color map
sm = ScalarMappable(cmap=cmap, norm=Normalize(vmin=min(edge_colors), vmax=max(edge_colors)))
sm.set_array([])

# Draw nodes, filtered edges, and labels
nx.draw_networkx_nodes(G, pos, node_size=300, node_color='pink')
nx.draw_networkx_edges(G, pos, edgelist=filtered_edges, edge_color=edge_colors, width=2, edge_cmap=cmap)
nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

# Create a colorbar as the legend and specify the axis for it (the current axis)
cbar = plt.colorbar(sm, label='Average offset distance', orientation='vertical', ax=plt.gca())

plt.title(f"This network graph shows {atom_selected} atom and its closeness with other atoms")
plt.axis('off')
st.pyplot(plt)


# Dataframe Table
st.markdown("Atom and its occurences across various files")
st.dataframe(atom_file_occurrence[atom_file_occurrence["atom"]==atom_selected])