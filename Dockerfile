FROM python:3.10.14-slim-bullseye

# Some packages
RUN apt update && \
    apt install -y \
    python3-dev \
    gcc \
    libc-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY . /pragmatics
RUN pip3 install --no-cache-dir -r /pragmatics/requirements.txt

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Set the working directory
WORKDIR /pragmatics

# Copy the dummy api keys
RUN cp ./config/api-keys.yaml.example ./config/api-keys.yaml
# Pull the latest templates
RUN python3 pragmatics.py --download-templates

# Run
ENTRYPOINT ["python3", "pragmatics.py"]
