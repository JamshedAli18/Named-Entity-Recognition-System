# Named Entity Recognition System

A web-based Named Entity Recognition (NER) system built with spaCy and Streamlit. This application allows users to input text and automatically identify named entities such as people, organizations, locations, dates, and more.

## Features

- Identify and visualize named entities in text
- Choose from multiple spaCy language models
- View entities in multiple formats (highlighted text, tables, charts)
- Download extracted entities as CSV
- Interactive visualizations of entity counts and relationships

## Installation

1. Clone this repository:
```bash
git clone https://github.com/JamshedAli18/ner-system.git
cd ner-system
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Download the spaCy language models:
```bash
# Required
python -m spacy download en_core_web_sm

# Optional larger models (better accuracy but slower)
python -m spacy download en_core_web_md
python -m spacy download en_core_web_lg
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the URL displayed in your terminal (usually http://localhost:8501)

3. Enter text in the provided text area and click "Analyze Text"

4. Explore the different tabs to see various visualizations of the named entities

## How It Works

This application uses spaCy's pre-trained models to identify named entities in text. The process involves:

1. Loading a spaCy model (small, medium, or large)
2. Processing the input text through the model
3. Extracting and categorizing named entities
4. Visualizing the results through Streamlit's interface

## Entity Types

spaCy can recognize various types of named entities, including:

- PERSON: People's names
- ORG: Organizations, companies, institutions
- GPE: Geopolitical entities (countries, cities, states)
- LOC: Non-GPE locations (mountain ranges, bodies of water)
- DATE: Dates or periods
- TIME: Times smaller than a day
- MONEY: Monetary values
- PERCENT: Percentages
- And many more

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
