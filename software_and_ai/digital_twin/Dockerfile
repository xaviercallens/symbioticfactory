FROM ubuntu:22.04

LABEL maintainer="Symbiotic Factory <github.com/xaviercallens/symbioticfactory>"
LABEL description="Digital Twin simulation environment for the WEFC Biorefinery"

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 python3.11-venv python3-pip \
    git curl wget build-essential gfortran \
    libopenblas-dev liblapack-dev \
    libhdf5-dev libmpich-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python3.11 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python simulation dependencies
WORKDIR /app
COPY software_and_ai/digital_twin/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the digital twin code
COPY software_and_ai/digital_twin/ /app/digital_twin/

WORKDIR /app/digital_twin

# Default: run the full digital twin
CMD ["python", "run_digital_twin.py", "--mode", "full"]
