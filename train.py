import argparse
import os
from ultralytics import YOLO

def train_yolov11(
    data_yaml,
    model="yolov11n.pt",
    img_size=1280,
    epochs=100,
    project="bepro",
    run_name="exp1",
    wandb_enabled=True
):
    # Ensure W&B is logged in if enabled
    if wandb_enabled:
        try:
            import wandb
            wandb.login()
        except Exception as e:
            print("W&B login failed:", e)

    # Load YOLOv11 model and train
    model = YOLO(model)
    model.train(
        data=data_yaml,
        imgsz=img_size,
        epochs=epochs,
        project=project,
        batch=-1
        name=run_name
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="Path to data.yaml")
    parser.add_argument("--model", type=str, default="yolov11n.pt", help="YOLOv11 model to use")
    parser.add_argument("--imgsz", type=int, default=1280, help="Input image size")
    parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs")
    parser.add_argument("--project", type=str, default="bepro", help="W&B project name")
    parser.add_argument("--name", type=str, default="exp1", help="W&B run name")
    parser.add_argument("--wandb", action="store_true", help="Enable W&B logging")

    args = parser.parse_args()

    train_yolov11(
        data_yaml=args.data,
        model=args.model,
        img_size=args.imgsz,
        epochs=args.epochs,
        project=args.project,
        run_name=args.name,
        wandb_enabled=args.wandb
    )
