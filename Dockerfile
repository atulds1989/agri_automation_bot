# Use an official Python runtime as a parent image
FROM python:3.11.6

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Google Chrome
# Add Google Chrome repository
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# Update apt-get and install Google Chrome
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

    # https://storage.googleapis.com/chrome-for-testing-public/136.0.7103.113/linux64/chromedriver-linux64.zip

# Install ChromeDriver
# Get the latest stable ChromeDriver version
ARG CHROME_DRIVER_VERSION="125.0.6422.78" # You might need to update this to match your Chrome version
RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/125.0.6422.78/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && rm chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver

# Copy the rest of the application code
COPY . .

# Set environment variables from .env file
# This assumes your .env file is in the root of your project
# We will use 'CMD' to load these, so they are available when the script runs.
# The CHROME_DRIVER_PATH is set directly in the config.py to a local path in the container.

# Set the CHROME_DRIVER_PATH environment variable to the path inside the container
ENV CHROME_DRIVER_PATH="/usr/local/bin/chromedriver"

# Command to run the application
# We use a shell form here to source the .env file if it contains variables that need to be loaded by the shell
# However, since you are loading them via python-dotenv in config.py, this is redundant for your current setup.
# The main.py script will load the .env variables directly.
CMD ["python", "main.py"]