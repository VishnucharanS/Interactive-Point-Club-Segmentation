import json
import cv2
import numpy as np
import open3d as o3d

def load_scene_camera(scene_path, frame_id):
    with open(f"{scene_path}/scene_camera.json", "r") as f:
        camera_data = json.load(f)
    frame_data = camera_data[str(frame_id)]
    cam_K = np.reshape(frame_data["cam_K"], (3, 3))
    cam_R_w2c = np.reshape(frame_data["cam_R_w2c"], (3, 3))
    cam_t_w2c = np.array(frame_data["cam_t_w2c"])
    depth_scale = frame_data["depth_scale"]
    return cam_K, cam_R_w2c, cam_t_w2c, depth_scale

def load_scene_rgbd(scene_path, depth_scale, frame_id):
    rgb = cv2.imread(f"{scene_path}/rgb/{frame_id:06d}.png", cv2.IMREAD_COLOR)
    rgb =cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    depth = cv2.imread(f"{scene_path}/depth/{frame_id:06d}.png", cv2.IMREAD_UNCHANGED)*depth_scale/ 1000.0 
    depth = depth.astype(np.float32)
    return rgb, depth

def depth_to_pointcloud(depth, cam_K, rgb=None):
    cam_K_o3d = o3d.camera.PinholeCameraIntrinsic()
    cam_K_o3d.set_intrinsics(depth.shape[1], depth.shape[0], cam_K[0, 0], cam_K[1, 1], cam_K[0, 2], cam_K[1, 2])

    if rgb is not None:
        rgb_o3d = o3d.geometry.Image(np.ascontiguousarray(rgb))
        depth_o3d = o3d.geometry.Image(depth)
        rgbd_o3d = o3d.geometry.RGBDImage.create_from_color_and_depth(
            rgb_o3d, depth_o3d, depth_scale=1.0, depth_trunc=5.0, convert_rgb_to_intensity=False
        )
        pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_o3d, cam_K_o3d)
    else:
        depth_o3d = o3d.geometry.Image(depth)
        pcd = o3d.geometry.PointCloud.create_from_depth_image(depth_o3d, cam_K_o3d)

    return pcd