from turtle import clear
from dotenv import load_dotenv
load_dotenv(override=True)
from tutor.builder import graph

png_data = graph.get_graph(xray=True).draw_mermaid_png()

with open("graph_diagram.png", "wb") as f:
    f.write(png_data)

print("Saved graph_diagram.png")