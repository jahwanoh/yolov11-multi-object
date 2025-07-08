FROM ultralytics/ultralytics:latest-runner

# Set working directory
WORKDIR /workspace/yolov11-multi-object

# Install additional dependencies (if needed)
RUN pip install --no-cache-dir opencv-python pandas tqdm wandb

# (Optional) Copy requirements.txt if you have one
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["/bin/bash"]
