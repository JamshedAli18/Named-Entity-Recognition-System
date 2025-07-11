import streamlit as st
import spacy
from spacy import displacy
import pandas as pd
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from collections import Counter

# Load spaCy models
@st.cache_resource
def load_model(model_name):
    return spacy.load(model_name)

# Initialize the app
st.set_page_config(page_title="Named Entity Recognition System", layout="wide")
st.title("Named Entity Recognition System")

# Sidebar for model selection and controls
st.sidebar.title("Controls")
model_name = st.sidebar.selectbox(
    "Select spaCy Model",
    ("en_core_web_sm", "en_core_web_md", "en_core_web_lg")
)

# Try loading the model, with error handling
try:
    nlp = load_model(model_name)
    st.sidebar.success(f"Model '{model_name}' loaded successfully!")
except:
    st.sidebar.error(f"Error: Model '{model_name}' not found. Please install it with 'python -m spacy download {model_name}'")
    st.stop()

# Explanation of NER
st.markdown("""
## What is Named Entity Recognition?
Named Entity Recognition (NER) is a natural language processing technique that identifies and classifies named entities in text into predefined categories such as:
- Persons
- Organizations
- Locations
- Dates
- Quantities
- Monetary values
- And more...
""")

# Entity color mapping for visualization
entity_colors = {
    "PERSON": "#7aecec",
    "ORG": "#feca74",
    "GPE": "#ff9561",
    "LOC": "#ff8197", 
    "DATE": "#bfe1d9",
    "TIME": "#bfe1d9",
    "MONEY": "#e4e7d2",
    "PERCENT": "#e4e7d2",
    "WORK_OF_ART": "#f0d0ff",
    "FAC": "#aab7d4", 
    "PRODUCT": "#bfeeb7",
    "EVENT": "#f89e96",
    "LAW": "#ddd1ff",
    "LANGUAGE": "#ff8461",
    "QUANTITY": "#e4e7d2",
}

# Input text area
st.header("Enter Text for NER Analysis")
text_input = st.text_area("Paste your text here:", height=150, 
                          value="Apple Inc. is planning to open a new office in New York City next January. CEO Tim Cook announced this during his visit to Boston last week.")

# Process button
if st.button("Analyze Text"):
    if not text_input.strip():
        st.error("Please enter some text to analyze.")
    else:
        doc = nlp(text_input)
        
        # Display results in tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Highlighted Text", "Entity List", "Entity Count", "Entity Visualization"])
        
        with tab1:
            st.subheader("Entities Highlighted in Text")
            # Use spaCy's displaCy for visualization
            html = displacy.render(doc, style="ent", options={"colors": entity_colors})
            st.markdown(html, unsafe_allow_html=True)
        
        with tab2:
            st.subheader("Extracted Entities")
            if len(doc.ents) > 0:
                entities_data = [(ent.text, ent.label_) for ent in doc.ents]
                df = pd.DataFrame(entities_data, columns=["Entity", "Type"])
                st.dataframe(df, use_container_width=True)
                
                # Download button for entity list
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="entities.csv">Download Entity List as CSV</a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                st.info("No entities were detected in the text.")
        
        with tab3:
            st.subheader("Entity Count by Type")
            if len(doc.ents) > 0:
                entity_counts = Counter([ent.label_ for ent in doc.ents])
                
                # Create a bar chart
                fig, ax = plt.subplots(figsize=(10, 6))
                entity_types = list(entity_counts.keys())
                counts = list(entity_counts.values())
                
                # Create colors list for bars
                colors = [entity_colors.get(entity, "#cccccc") for entity in entity_types]
                
                bars = ax.bar(entity_types, counts, color=colors)
                ax.set_ylabel('Count')
                ax.set_title('Entity Counts by Type')
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                
                # Add count labels on top of bars
                for bar in bars:
                    height = bar.get_height()
                    ax.annotate(f'{height}',
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 3),
                                textcoords="offset points",
                                ha='center', va='bottom')
                
                st.pyplot(fig)
            else:
                st.info("No entities were detected in the text.")
        
        with tab4:
            st.subheader("Entity Network Visualization")
            if len(doc.ents) > 0:
                # Simple network visualization using matplotlib
                st.markdown("Entity relationship visualization shows how entities appear in the document:")
                
                # Just displaying an entity cloud for simplicity
                # In a more advanced implementation, you could use networkx for relationship graphs
                entities = [ent.text for ent in doc.ents]
                entity_types = [ent.label_ for ent in doc.ents]
                
                # Create a scatter plot with entity types as colors
                fig, ax = plt.subplots(figsize=(10, 6))
                
                # Convert entity types to numerical values for scatter plot
                unique_types = list(set(entity_types))
                type_to_num = {ent_type: i for i, ent_type in enumerate(unique_types)}
                y_values = [type_to_num[ent_type] for ent_type in entity_types]
                
                # Create a scatter plot
                colors = [entity_colors.get(ent_type, "#cccccc") for ent_type in entity_types]
                scatter = ax.scatter(range(len(entities)), y_values, c=colors, s=100)
                
                # Add labels
                for i, entity in enumerate(entities):
                    ax.annotate(entity, (i, y_values[i]), 
                                xytext=(0, 5), textcoords='offset points',
                                ha='center', fontsize=9)
                
                # Create legend
                legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                            label=ent_type, 
                                            markerfacecolor=entity_colors.get(ent_type, "#cccccc"), 
                                            markersize=8)
                                for ent_type in unique_types]
                
                ax.legend(handles=legend_elements, title="Entity Types")
                ax.set_yticks([])
                ax.set_xticks([])
                ax.set_title("Entity Visualization")
                plt.tight_layout()
                
                st.pyplot(fig)
            else:
                st.info("No entities were detected in the text.")

# Add an explanation section for entity types
with st.expander("Entity Types Explanation"):
    st.markdown("""
    | Entity Type | Description | Example |
    |-------------|-------------|---------|
    | PERSON | People, including fictional | Tim Cook, Harry Potter |
    | ORG | Companies, agencies, institutions | Apple Inc., United Nations |
    | GPE | Countries, cities, states | New York City, France |
    | LOC | Non-GPE locations, mountain ranges, bodies of water | Alps, Pacific Ocean |
    | DATE | Absolute or relative dates or periods | January, last week |
    | TIME | Times smaller than a day | 3pm, midnight |
    | MONEY | Monetary values, including unit | $200, 10 euros |
    | PERCENT | Percentage | 15%, one-tenth |
    | WORK_OF_ART | Titles of books, songs, etc. | "The Great Gatsby" |
    | FAC | Buildings, airports, highways, bridges | Golden Gate Bridge |
    | PRODUCT | Objects, vehicles, foods, etc. (not services) | iPhone, Boeing 747 |
    | EVENT | Named hurricanes, battles, wars, sports events | World War II, Olympics |
    | LAW | Named documents made into laws | Constitution, GDPR |
    | LANGUAGE | Any named language | English, Spanish |
    | QUANTITY | Measurements, as of weight or distance | 10km, 20 pounds |
    """)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using spaCy and Streamlit")