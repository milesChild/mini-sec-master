FROM python:3.11-slim
WORKDIR /code
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY app ./app
COPY .env .env
CMD ["streamlit", "run", "app/frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
