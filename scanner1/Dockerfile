FROM python:3.10

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code into container
COPY . .

# Optional: Preload models during build (requires HF_TOKEN as build ARG)
# Note: ENV vars like HF_TOKEN are not available at build time unless passed as ARGs.
# We remove this step to avoid model load failures during build.
# The model will instead be downloaded at runtime by Hugging Face cache.

EXPOSE 5001

# Start app using gunicorn
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5001", "--timeout", "120", "scanner1:app"]
