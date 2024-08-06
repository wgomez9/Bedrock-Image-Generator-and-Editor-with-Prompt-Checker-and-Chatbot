FROM python:3.8
# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*
    
EXPOSE 8501
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN  pip3 install --upgrade pip && pip3 install -r requirements.txt
COPY . .

# Command overriden by docker-compose
CMD streamlit run app.py