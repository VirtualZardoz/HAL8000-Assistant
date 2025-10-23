FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    wget \
    libgl1-mesa-glx \
    libglib2.0-0 \
    imagemagick \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip3 install --upgrade pip

# Install ComfyUI
WORKDIR /app
RUN git clone https://github.com/comfyanonymous/ComfyUI.git
WORKDIR /app/ComfyUI
RUN pip3 install --no-cache-dir -r requirements.txt

# Install additional dependencies
RUN pip3 install --no-cache-dir \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 \
    pillow \
    requests

# Create directories for mounted volumes
RUN mkdir -p /models/checkpoints /models/vae /models/clip /output

# Create symlinks from ComfyUI's expected model paths to our mounted volumes
RUN rm -rf /app/ComfyUI/models && ln -s /models /app/ComfyUI/models

# Copy entrypoint script
COPY entrypoint.py /app/entrypoint.py
RUN chmod +x /app/entrypoint.py

# Set working directory
WORKDIR /app

# Environment variables
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python3", "/app/entrypoint.py"]
