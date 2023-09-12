<img src="img/header.jpg" alt="Header" width="100%"/>

Please use instructions on  [project page](https://www.cmu-exploration.com).

# M200 使用 [Autonomous Exploration Development Environment and the Planning Algorithms](https://www.cmu-exploration.com)

##  1. 基于LIO_SAM的状态估计
前提情况：
+ LIO_SAM默认输出的坐标系为
map->odom->"lidar_frame"
其中map与odom的默认坐标系重合固定，可参考LIO_SAM的[imuPreintegration.cpp的92行](https://github.com/TixiaoShan/LIO-SAM/blob/0be1fbe6275fb8366d5b800af4fc8c76a885c869/src/imuPreintegration.cpp#L92)

+ 激光雷达的里程计(/lio_sam/mapping/odometry)以及点云关键帧(/lio_sam/mapping/cloud_registered)的坐标系均为odom 
可参考LIO_SAM的mapOptmization.cpp的[void publishOdometry()](https://github.com/TixiaoShan/LIO-SAM/blob/0be1fbe6275fb8366d5b800af4fc8c76a885c869/src/mapOptmization.cpp#L1633)和[void publishFrames()](https://github.com/TixiaoShan/LIO-SAM/blob/0be1fbe6275fb8366d5b800af4fc8c76a885c869/src/mapOptmization.cpp#L1704C5-L1704C25)

M200的3D激光雷达安装位置高于小车主体1.12米左右，x轴偏离0.365
~~修改如下：~~
~~+ 将imuPreintegration.cpp的~~
  ~~>static tf::Transform map_to_odom = tf::Transform(tf::createQuaternionFromRPY(0, 0, 0), tf::Vector3(0, 0, 0));~~

  ~~修改为~~

  ~~>static tf::Transform map_to_odom = tf::Transform(tf::createQuaternionFromRPY(0, 0, 0), tf::Vector3(0, 0, 1.12));~~

config文件夹下params.yaml文件部分参数修改
  > #Extrinsics: T_lb (lidar -> imu)
  extrinsicTrans: [-0.365, 0.0, 1.12]
  
  >#voxel filter paprams
  odometrySurfLeafSize: 0.2                     # default: 0.4 - outdoor, 0.2 - indoor
  mappingCornerLeafSize: 0.1                    # default: 0.2 - outdoor, 0.1 - indoor
  mappingSurfLeafSize: 0.2                      # default: 0.4 - outdoor, 0.2 - indoor

## 2. 修改 loam_interface

+ 修改launch文件的订阅话题
```xml
<param name="stateEstimationTopic" type="string" value="/lio_sam/mapping/odometry" />
<param name="registeredScanTopic" type="string" value="/lio_sam/mapping/cloud_registered" />
```
~~+ 修改[loamInterface.cpp](./src/loam_interface/src/loamInterface.cpp)~~

~~在63行添加如下~~
```cpp
odomData.pose.pose.position.z = odom->pose.pose.position.z + 1.12 ;
```
~~在99行添加如下~~
```cpp
    int laserCloudSize = laserCloud->points.size();
    for (int i = 0; i < laserCloudSize; i++) {
      laserCloud->points[i].z += 1.12;
    }
```
~~**其目的是将lio_sam基于odom坐标系的里程计和关键帧的转换到map下**~~

## 3. 其余修改

+ src/local_planner/launch/local_planner.launch
```xml
  <node pkg="tf" type="static_transform_publisher" name="vehicleTransPublisher" args="0.365 $(arg sensorOffsetY) 0 0 0 0 /sensor /vehicle 1000"/>
```

+ src/terrain_analysis/launch/terrain_analysis.launch
```xml
<param name="vehicleHeight" type="double" value="1.2" />
<param name="minRelZ" type="double" value="-1.2" />
<param name="maxRelZ" type="double" value="0.2" />
```

## 启动命令
+ 默认已启动
roslaunch m200_driver m200_driver.launch
### 分步启动
```bash
##3D激光雷达
roslaunch rslidar_sdk start.launch

##LIO_SAM
roslaunch lio_sam run.launch

##Autonomous 
roslaunch vehicle_simulator system_real_robot.launch
```
### 一键启动
```bash
roslaunch m200_navigation 3D_demo.launch
```