#!/bin/bash

# Set variables for host paths
HOST_PROJECT_DIR={$REPO_PATH}
HOST_DATA_DIR="/mnt/data"
WANDB_API_KEY={$ADD_YOUR_KEY}

# Run the Docker container
sudo docker run -it --rm \
  --gpus all \
  --shm-size=16g \
  --ulimit memlock=-1 \
  --ulimit stack=67108864 \
  --privileged \
  --network host \
  --cap-add=SYS_ADMIN \
  --pid=host \
  -e NVIDIA_DRIVER_CAPABILITIES=utility,video,compute \
  -e WANDB_API_KEY=${WANDB_API_KEY} \
  -v ${HOST_PROJECT_DIR}:/workspace/yolov11-multi-object:cached \
  -v ${HOST_DATA_DIR}:/workspace/yolov11-multi-object/data \
  --user root \
  --name yolov11-multi-object \
  ultralytics/ultralytics:latest-runner /bin/bash 