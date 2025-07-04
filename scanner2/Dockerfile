FROM python:3.10

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git git-lfs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_trf

# Download NLTK tokenizer data
RUN python -c "import nltk; nltk.download('punkt')"

# Copy application code
COPY . .

# Expose port for container
EXPOSE 5002

# Run the app using gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5002", "scanner2:app"]
