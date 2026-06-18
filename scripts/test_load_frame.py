from click_segment_core.load import load_scene_camera, load_scene_rgbd, depth_to_pointcloud
import open3d as o3d
import numpy as np
scene_path = "/home/vishnucharan/Projects/point_cloud_segmentation/click_segment_ws/data/ycbv/test/000048"
frame_id = 1087


cam_K, cam_R_w2c, cam_t_w2c, depth_scale = load_scene_camera(scene_path, frame_id)
rgb, depth = load_scene_rgbd(scene_path, depth_scale, frame_id)

print("rgb shape/dtype:", rgb.shape, rgb.dtype)
print("depth shape/dtype:", depth.shape, depth.dtype)
print("depth min/max:", depth.min(), depth.max())

pcd = depth_to_pointcloud(depth, cam_K, rgb=rgb)
print("number of points:", len(pcd.points))
print("pcd has colors:", pcd.has_colors())
if pcd.has_colors():
    colors_arr = np.asarray(pcd.colors)
    print("colors min/max:", colors_arr.min(), colors_arr.max())
    print("sample colors:", colors_arr[:5])

o3d.visualization.draw_geometries([pcd])