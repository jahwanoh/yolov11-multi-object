import os
import pandas as pd
from glob import glob
import cv2
from tqdm import tqdm
import argparse

def convert_csv_to_yolo(csv_path, img_dir, label_dir):
    sample_images = glob(os.path.join(img_dir, "*.jpg"))
    if not sample_images:
        return

    sample = cv2.imread(sample_images[0])
    if sample is None:
        return
    img_height, img_width = sample.shape[:2]

    df = pd.read_csv(csv_path)

    for frame, group in df.groupby("frameNumber"):
        label_path = os.path.join(label_dir, f"{int(frame)}.txt")
        lines = []
        for _, row in group.iterrows():
            x_center = (row["vx"] + row["vw"] / 2) / img_width
            y_center = (row["vy"] + row["vh"] / 2) / img_height
            w = row["vw"] / img_width
            h = row["vh"] / img_height
            class_id = int(row["objectId"])
            lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")
        with open(label_path, "w") as f:
            f.write("\n".join(lines))

def main(base_dir):
    dataset_dirs = sorted(glob(os.path.join(base_dir, "*-*")))
    for dataset_dir in tqdm(dataset_dirs, desc="Converting to YOLO format"):
        csv_path = os.path.join(dataset_dir, "annotation.csv")
        img_dir = os.path.join(dataset_dir, "raw_images")
        label_dir = os.path.join(dataset_dir, "labels")

        if not os.path.exists(csv_path) or not os.path.exists(img_dir):
            continue

        os.makedirs(label_dir, exist_ok=True)
        convert_csv_to_yolo(csv_path, img_dir, label_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, required=True, help="Base directory of dataset")
    args = parser.parse_args()
    main(args.dir)
