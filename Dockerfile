FROM python:3.8

# Set working directory
WORKDIR /pyapp

# Install dependencies
COPY ./src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY ./src .

# Expose app port (optional but recommended)
EXPOSE 5000

# Run the app
CMD ["python", "runserver.py"]
