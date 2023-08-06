import numpy as np
from pyproj import CRS, Transformer


def get_zenith_angle(sat_lon, sat_lat, sat_alt, obs_lon, obs_lat, obs_alt=None):
    """
    计算卫星与地面观测点之间的夹角
    :参数 sat_lon: 卫星经度（单位：度）
    :参数 sat_lat: 卫星纬度（单位：度）
    :参数 sat_alt: 卫星高度（单位：千米）
    :参数 obs_lon: 观测点经度（单位：度）
    :参数 obs_lat: 观测点纬度（单位：度）
    :参数 obs_alt: 观测点高度（单位：米），可选，默认为0
    :return: 卫星与地面观测点之间的夹角（单位：度）
    """

    # 预处理
    obs_shape = obs_lat.shape
    obs_lat = obs_lat.flatten()
    obs_lon = obs_lon.flatten()
    obs_alt = obs_alt.flatten() if obs_alt is not None else np.zeros_like(obs_lat)
    sat_alt = sat_alt * 1000  # 卫星高度:km转换为米

    # 创建坐标转换器（从WGS84经纬度坐标转换到地心惯性坐标系）
    crs_lla = CRS("EPSG:4326")  # WGS84经纬度坐标系统
    crs_ecef = CRS("EPSG:4978")  # 地心惯性坐标系
    transformer = Transformer.from_crs(crs_lla, crs_ecef, always_xy=True)

    # 将卫星位置、地面观测点位置从WGS84经纬度和高度转换为地心惯性坐标系下的坐标
    sat_ecef = transformer.transform(sat_lon, sat_lat, sat_alt)
    obs_ecef = transformer.transform(obs_lon, obs_lat, obs_alt)

    # 计算卫星与地面观测点之间的向量
    obs_vec = np.array(obs_ecef)
    obs_sat_vec = np.array(sat_ecef)[:, np.newaxis] - obs_vec
    obs_sat_dist = np.linalg.norm(obs_sat_vec, axis=0)
    obs_dist = np.linalg.norm(obs_vec, axis=0)

    # 计算卫星与地面观测点之间的夹角（单位：度）
    theta = np.rad2deg(
        np.arccos(np.sum(obs_vec*obs_sat_vec, axis=0) / obs_sat_dist / obs_dist))

    return theta.reshape(obs_shape)


def mercator_in_wps(rlat, rlon, tlat, delta, e_we, e_sn):
    '''
    用于计算namelist.wps中的参数计算经纬度范围
    rlat: 中心纬度
    rlon: 中心纬度
    tlat: 真实经纬度true_lat
    delta: 网格间距dx,dy你设置成不一样的，也会是一样的
    e_we: 东西方向格点数
    e_sn: 南北方向格点数
    '''
    # 创建自定义麦卡托投影的定义字符串
    mercator_proj = f"+proj=merc +lon_0=100 +lat_ts={tlat} +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs"

    # 创建转换器实例
    tf1 = Transformer.from_crs("EPSG:4326", mercator_proj)
    tf2 = Transformer.from_crs(mercator_proj, "EPSG:4326")

    # 将经纬度坐标转换为自定义麦卡托投影坐标
    rx, ry = tf1.transform(rlat, rlon)

    north, west = tf2.transform(rx - delta*e_we / 2, ry + delta*e_sn / 2)
    south, east = tf2.transform(rx + delta*e_we / 2, ry - delta*e_sn / 2)

    return north, west, south, east
