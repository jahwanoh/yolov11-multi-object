import os
import yaml
from glob import glob
import argparse

def generate_yaml(src_root):
    label_dirs = sorted(glob(os.path.join(src_root, "*-*/labels")))
    dataset_dirs = [os.path.dirname(ld) for ld in label_dirs]

    yaml_content = {
        "train": [],
        "val": [],
        "nc": 2,
        "names": ["object"]
    }

    for i, dataset_dir in enumerate(dataset_dirs):
        split = "train" if i % 5 != 0 else "val"  # ~80/20 split
        yaml_content[split].append(dataset_dir)

    yaml_path = os.path.join(src_root, "yolo_dataset.yaml")
    with open(yaml_path, "w") as f:
        yaml.dump(yaml_content, f, default_flow_style=False)

    print(f"✅ Saved dataset YAML to: {yaml_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, required=True, help="Base directory of dataset")
    args = parser.parse_args()
    generate_yaml(args.dir)
