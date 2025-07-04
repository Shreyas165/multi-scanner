FROM python:3.10

WORKDIR /app

# Copy all source files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install flask gunicorn transformers==4.30.2 huggingface_hub==0.23.0
RUN pip install llm-guard
# Install latest llm-guard with PromptInjection scanner
RUN pip install git+https://github.com/protectai/llm-guard.git@main

EXPOSE 5003

# Start server
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5003", "--timeout", "120", "scanner3:app"]
