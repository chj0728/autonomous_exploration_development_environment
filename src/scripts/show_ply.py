# @Time2021/9/915:00
# QAuthorCHJ
# @Site读取pLy文件并显示
# @File show_ply.py

import open3d as o3d
import numpy as np

if __name__ == "__main__":
    print("Load a ply point cloud,print it,and render it")

    # pcd = o3d.io.read_point_cloud("pointcloud.ply")
    pcd_paths = o3d.io.read_point_cloud("../local_planner/paths/paths.ply")
    pcd_pathList = o3d.io.read_point_cloud("../local_planner/paths/pathList.ply")
    pcd_startPaths = o3d.io.read_point_cloud("../local_planner/paths/startPaths.ply")


    # print(pcd)
    # print(np.asarray(pcd.points))

    # using PyCharm
    # 方式1
    # vis = o3d.visualization.Visualizer()
    # vis.create_window()
    # vis.add_geometry(pcd)
    # vis.poll_events()
    # vis.update_renderer()
    # vis.run()

    # using PyCharm
    # 方式2
    o3d.visualization.draw_geometries([pcd_paths, pcd_pathList, pcd_startPaths])
