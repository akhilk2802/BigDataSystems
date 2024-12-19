## GAIA ETL Pipeline - Data Processing and Model Evaluation

### Project Overview

This project focuses on building a robust ETL (Extract, Transform, Load) pipeline using AWS services like RDS, S3, and PostgreSQL, integrated with Hugging Face’s GAIA dataset. The application processes metadata, files, and annotations, stores them securely in AWS infrastructure, and facilitates interactions via a Streamlit-powered web interface.


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

ETL Pipeline Flow

1. Extract
	•	Data is extracted from Hugging Face’s GAIA dataset using the Hugging Face Hub API.

2. Transform
	•	Annotator Metadata and file information are cleaned and transformed using pandas.
	•	Data is converted to SQL and uploaded to AWS RDS.

3. Load
	•	Metadata is stored in PostgreSQL on AWS RDS.
	•	Files are uploaded to AWS S3.
	•	File paths and metadata URLs are updated in PostgreSQL.

### Installation and Setup:

1. Clone repository:
   ```bash
   git clone https://github.com/akhilk2802/BigDataSystems.git
   cd gaia-openai-validations
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
4. Create .env file
   ```bash
   HF_TOKEN=
   OPEN_AI_TOKEN=
   AWS_PROFILE=
   AWS_RDS_HOST=
   AWS_RDS_USERNAME=
   AWS_RDS_PASSWORD=
   AWS_RDS_DB_PORT=
   AWS_RDS_DATABASE=
   AWS_S3_BUCKET=
   ```

### Running the application:
```bash
python components/data_storage.py
streamlit run app.py
```