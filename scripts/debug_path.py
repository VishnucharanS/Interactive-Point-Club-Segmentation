from pathlib import Path
import json

base_test_dir = Path("/home/vishnucharan/Projects/point_cloud_segmentation/click_segment_ws/data/ycbv/test")
print(f"1. Checking Base Path: {base_test_dir} -> Exists? {base_test_dir.exists()}")

scene_folders = sorted([f for f in base_test_dir.iterdir() if f.is_dir() and f.name.isdigit()])
print(f"2. Found {len(scene_folders)} numeric scene directories.")

if len(scene_folders) > 0:
    sample_scene = scene_folders[0]
    rgb_dir = sample_scene / "rgb"
    print(f"3. First Scene: {sample_scene.name} -> rgb/ exists? {rgb_dir.exists()}")
    
    if rgb_dir.exists():
        frame_files = sorted([f.stem for f in rgb_dir.glob("*.png")])
        print(f"4. Found {len(frame_files)} frames inside rgb/ folder.")
        
    gt_json = sample_scene / "scene_gt.json"
    print(f"5. scene_gt.json exists? {gt_json.exists()}")
    if gt_json.exists():
        with open(gt_json, "r") as f:
            gt_data = json.load(f)
        print(f"6. Total keys inside scene_gt.json: {len(gt_data)}")
        print(f"7. Sample frame key types: {list(gt_data.keys())[:3]}")
