# Automating Text Extraction 

Automating Text Extraction and Client-Facing Application Development. This project focuses on automating workflows, implementing text extraction, and building a secure client-facing application using Airflow, Streamlit, and FastAPI.

### Project Flow 

1. Step 1: PDF Handling
   
   The system manages PDF files through two methods:
   - Open-Source Tools (PyMuPDF): Transforms PDFs into markdown format and extracts images.
   - Azure Text Extraction using AI: Processes extensive PDFs using a custom pipeline with high concurrency, adept at managing intricate document structures.

2. Step 2: Data Storage and Administration

   - S3 Buckets: Preserves original PDFs alongside processed outputs (markdown, images, JSON).
   - RDS (MySQL): Oversees metadata for PDFs and processed files, facilitating efficient querying and updates.

3. Step 3: User Interaction via Streamlit

    Users engage with the processed data through a Streamlit interface, offering capabilities to:
	- Upload new PDFs.
	- View and download extracted content.
	- Examine metadata and processed data.

4. Step 4: API Development with FastAPI
	
    FastAPI: Functions as the backend framework to establish and manage API endpoints, handling requests for PDF processing and data retrieval, ensuring seamless communication between the client interface and underlying services.
    Provides endpoints for:
	- User Authentication:
	- Login: Endpoint for user authentication and session initiation.
	- Registration: Endpoint for new user account creation, securely storing credentials in the database.
	- Retrieving extracted data and metadata.
	- Downloading PDF Files: Endpoints to facilitate the download of original PDFs.
	- Integration with the OpenAI API for advanced insights.

5. Step 5: AI Integration

	- OpenAI GPT Model: Employed to interpret natural language queries on the extracted data, offering insights based on document content.


### How the UI looks: 

![Application](./assets/image1.png)
![Select a question](./assets/image2.png)
![Answer](./assets/image3.png)
![Download](./assets/image4.png)