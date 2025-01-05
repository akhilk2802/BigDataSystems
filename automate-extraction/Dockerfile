FROM python:3.12.6

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./fastapi /code/fastapi
COPY ./scripts /code/scripts
COPY ./streamlit /code/streamlit
COPY ./utils /code/utils

CMD ["/bin/bash", "-c", "uvicorn fastapi.app/.main:app --host 0.0.0.0 --port 8000 --reload & streamlit run streamlit/app/main --server.port 8501"]
