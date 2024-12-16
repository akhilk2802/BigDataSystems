## Model Evaluation tool using streamlit

This part of the project is a Model Evaluation Tool built using Streamlit, integrating Hugging Face’s BERT-based model (deepset/bert-base-cased-squad2) for question-answering tasks. The system evaluates model responses against test cases from the GAIA dataset, compares predictions with the expected answers, and collects user feedback.


### The application provides:

1. Model Evaluation: Uses Hugging Face’s BERT model to generate answers
2. Test Case Management: Extracts test questions and context from the dataset.
3. Evaluation Metrics: Compares model responses using Exact Match and BLEU Score.
4. Feedback Recording: Records user corrections and feedback in a CSV file
5. Evaluation Report: Displays all evaluation results in a tabular format.


### libraries used: 
- Streamlit - Web Framework for UI
- Transformers - Hugging Face Model Integration
- Torch - Deep Learning Library
- Pandas - Data Manipulation and Storage
- Evaluate - Model Metrics (BLEU Score)
- Huggingface Hub - Authentication and API Management
- Python-dotenv - Environment Variable Management

### Installation and Setup:

1. Clone repository:
   ```bash
   git clone https://github.com/akhilk2802/BigDataSystems.git
   cd assignment1
   ```
2. Create a Virtual Environment
   ```bash
    python3 -m venv venv
    source venv/bin/activate  # macOS/Linux
    venv\Scripts\activate     # Windows
   ```
3. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```

### Running the application:
```bash
streamlit run app.py
```