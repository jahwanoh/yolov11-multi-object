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

        # Create a symlink from raw_images to images if it doesn't exist
        images_symlink = os.path.join(dataset_dir, "images")
        if not os.path.exists(images_symlink):
            try:
                os.symlink(img_dir, images_symlink)
            except FileExistsError:
                pass

    # Draw bounding boxes on one sample image for each dataset directory using YOLO annotation and save to file
    for sample_dataset in dataset_dirs:
        sample_img_dir = os.path.join(sample_dataset, "raw_images")
        sample_label_dir = os.path.join(sample_dataset, "labels")
        sample_images = sorted(glob(os.path.join(sample_img_dir, "*.jpg")))
        if sample_images:
            sample_img_path = sample_images[0]
            sample_img = cv2.imread(sample_img_path)
            if sample_img is not None:
                img_height, img_width = sample_img.shape[:2]
                # Find corresponding label file
                sample_img_name = os.path.splitext(os.path.basename(sample_img_path))[0]
                label_path = os.path.join(sample_label_dir, f"{sample_img_name}.txt")
                if os.path.exists(label_path):
                    with open(label_path, "r") as f:
                        for line in f:
                            parts = line.strip().split()
                            if len(parts) == 5:
                                class_id, x_center, y_center, w, h = map(float, parts)
                                # Convert YOLO format to pixel coordinates
                                x_center *= img_width
                                y_center *= img_height
                                w *= img_width
                                h *= img_height
                                x1 = int(x_center - w / 2)
                                y1 = int(y_center - h / 2)
                                x2 = int(x_center + w / 2)
                                y2 = int(y_center + h / 2)
                                cv2.rectangle(sample_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    # Save the image with bounding boxes
                    out_path = os.path.join(sample_dataset, "sample_with_boxes.jpg")
                    cv2.imwrite(out_path, sample_img)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, required=True, help="Base directory of dataset")
    args = parser.parse_args()
    main(args.dir)
