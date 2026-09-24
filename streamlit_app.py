import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from searchAlgos import (
    hospital_graph,
    locations,
    gbfs,
    a_star
)

# Streamlit GUI
#*******************#

st.set_page_config(page_title="Hospital Robot Pathfinder", layout="centered")

st.title("🏥 Emergency Supply Robot – Search Visualizer")
st.write(
    "Pick a start location, a goal location, and a search algorithm. "
    "The app runs GBFS or A* on the hospital graph and highlights the path found."
)

# define the nodes and their coordinates
nodes = list(hospital_graph.keys())

# create a selectbox for the user to choose the start and goal nodes
start = st.selectbox(
    "Select Initial Node",
    nodes,
    index=nodes.index("Pharmacy")
)

goal = st.selectbox(
    "Select Goal Node",
    nodes,
    index=nodes.index("Emergency_Ward")
)

# create a selectbox for the user to choose the search algorithm
algorithm = st.selectbox(
    "Select Search Algorithm",
    ["GBFS", "A*"]
)

if st.button("Run Search"):

    if algorithm == "GBFS":
        path, cost, expansion_order = gbfs(start, goal)
    else:
        path, cost, expansion_order = a_star(start, goal)

    if path is None:

        st.error(f"No path found from {start} to {goal}.")

    else:

        # Display result
        st.subheader("Search Result")

        st.write(f"**Algorithm:** {algorithm}")
        st.write(f"**Solution Path:** {' → '.join(path)}")
        st.write(f"**Total Path Cost:** {cost:.2f}")
        st.write(f"**Expansion Order:** {' → '.join(expansion_order)}")

        # Visualize NetworkX graph
        G = nx.DiGraph()

        for node, neighbors in hospital_graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)

        pos = locations
        path_edges = list(zip(path, path[1:]))

        fig, ax = plt.subplots(figsize=(10, 6))

        nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=1500, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold", ax=ax)

        nx.draw_networkx_edges(
            G, pos, edgelist=G.edges(), edge_color="gray",
            arrows=True, connectionstyle="arc3,rad=0.08", ax=ax
        )
        nx.draw_networkx_edges(
            G, pos, edgelist=path_edges, edge_color="red", width=3,
            arrows=True, connectionstyle="arc3,rad=0.08", ax=ax
        )

        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, ax=ax)

        ax.set_title(f"{algorithm} Solution Path")
        ax.axis("off")

        st.pyplot(fig)