import numpy as np
from pyproj import CRS, Transformer
import re


def get_zenith_angle(sat_lon, sat_lat, sat_alt, obs_lon, obs_lat, obs_alt=None):
    """
    计算卫星与地面观测点之间的天顶角（本地入射角）
    :参数 sat_lon: 卫星经度（单位：度）
    :参数 sat_lat: 卫星纬度（单位：度）
    :参数 sat_alt: 卫星高度（单位：千米）
    :参数 obs_lon: 观测点经度（单位：度）
    :参数 obs_lat: 观测点纬度（单位：度）
    :参数 obs_alt: 观测点高度（单位：米），可选，默认为0
    :return: 卫星与地面观测点之间的天顶角（单位：度）
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


class ShellScriptVariable:
    '''
    用于读取和修改 shell 脚本中的变量值
    '''

    def __init__(self, script_path, **kwargs):
        self.script_path = script_path
        with open(script_path, 'r', **kwargs) as f:
            self.content = f.read()

    # 读取变量值
    def get(self, variable_name):
        pattern = rf"({variable_name}\s*=\s*)([^\s\n][^\n]*)"
        match = re.search(pattern, self.content)
        if match:
            return match.group(2)
        else:
            raise ValueError(f"变量 {variable_name} 不存在")

    # 修改变量值
    def update(self, variable_name, new_value, count=1):
        pattern = rf"({variable_name}\s*=\s*)([^\s\n][^\n]*)"
        # 确认是否存在变量，不存在会抛出异常
        self.get(variable_name)
        new_str = f"{variable_name}={new_value}"
        self.content = re.sub(pattern, new_str, self.content, count=count)

    # 保存脚本

    def save(self, save_path=None):
        if not save_path:
            save_path = self.script_path
        with open(save_path, 'w') as f:
            f.write(self.content)

    # 显示脚本的内容

    def show(self):
        print(f'-------{self.script_path}----------')
        print(self.content)
        print('------------------------------------')

    # 类方法，修改脚本的变量值并保存
    @classmethod
    def modify(cls, script_path, variable_name, new_value, save_path=None, count=1, **kwargs):
        ssv = cls(script_path, **kwargs)
        ssv.update(variable_name, new_value, count=count)
        ssv.save(save_path)
