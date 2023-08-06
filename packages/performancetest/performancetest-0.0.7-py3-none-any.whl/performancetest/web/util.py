import concurrent.futures
import os
import traceback
from builtins import *

import numpy as np

from performancetest.core.global_data import logger


class DataCollect(object):

    def __init__(self, file_dir_path=None):
        """
        任务所在文件夹, 设置了这个文件夹其他的不需要再传file_path
        """
        self.file_dir_path = file_dir_path
        self.is_need_relative_time = False

    def __read_csv_file(self, file_path=None, skip_rows=1, usecols=None):
        """
        读取cpu，memory，fps，gpu，温度等csv文件的值
        """
        if not usecols:
            csv_data = np.genfromtxt(file_path, skip_header=skip_rows, delimiter=",", dtype=float, filling_values=0)
        else:
            csv_data = np.genfromtxt(file_path, skip_header=skip_rows, delimiter=",", dtype=float, filling_values=0,
                                     usecols=usecols)
        return csv_data

    def __read_cpu(self, file_path=None):
        if not file_path:
            file_path = os.path.join(self.file_dir_path, "cpu.csv")
        return self.__read_csv_file(file_path=file_path)

    def __read_memory(self, file_path=None):
        if not file_path:
            file_path = os.path.join(self.file_dir_path, "memory.csv")
        return self.__read_csv_file(file_path=file_path)

    def __read_gpu(self, file_path=None):
        if not file_path:
            file_path = os.path.join(self.file_dir_path, "gpu.csv")
        return self.__read_csv_file(file_path=file_path)

    def __read_device_temperature(self, file_path=None):
        if not file_path:
            file_path = os.path.join(self.file_dir_path, "devicebattery.csv")
        return self.__read_csv_file(file_path=file_path, usecols=(0, 1))

    def __read_device_battery_level(self, file_path=None):
        if not file_path:
            file_path = os.path.join(self.file_dir_path, "devicebattery.csv")
        return self.__read_csv_file(file_path=file_path, usecols=(0, 2))

    def __read_fps(self, file_path=None):
        if not file_path:
            file_path = os.path.join(self.file_dir_path, "fps.csv")
        return self.__read_csv_file(file_path=file_path)

    # 监控类型对应的读取方法
    __monitortype_func = {"cpu": __read_cpu, "memory": __read_memory, "fps": __read_fps,
                          "gpu": __read_gpu, "devicebatterytemperature": __read_device_temperature,
                          "devicebatterylevel": __read_device_battery_level}

    # 读数据的方法使用：DataCollect.read_data(1, "cpu", "memory", "fps")
    @classmethod
    def read_data(cls, file_dir_path: int, /, *args, **kwargs):
        """
        param: "cpu", "memory"
        return:
        {
            public_imgs：[{"16xxxxxx": "pic_path"}, {"16xxxxxx": "pic_path1"}]
            public_start_time：16xxxxxx: int,
            public_end_time：16xxxxxx: int,
            cpu: {
                 time：[16xxxxxx, 16xxxxxx]  //cpu,memory,fps 开始真实时间戳相同
                 value: [100, 101]
                 relative_time: [00:00, 00:10]
            },
            memory: {
                  time：[16xxxxxx, 16xxxxxx]  //cpu,memory,fps 开始真实时间戳相同
                 value: [100, 101]

            }
        }
        """
        return cls.item_result(file_dir_path, monitortypes=args,
                               is_need_relative_time=kwargs.get("is_need_relative_time", True))

    # 读所有类型的数据的方法使用：DataCollect.read_data(1, "cpu", "memory", "fps")
    @classmethod
    def read_data_all(cls, file_dir_path):
        return cls.read_data(file_dir_path, *cls.__monitortype_func.keys())

    @classmethod
    def item_result(cls, file_dir_path: int, monitortypes: tuple, **kwargs):
        data_collect = DataCollect(file_dir_path=file_dir_path)
        result_dict: dict = {}  # 存储每种监控类型的结果
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 执行所有读取
            wait_task: list = []
            for monitor_name in monitortypes:
                future = executor.submit(cls.__monitortype_func.get(monitor_name), data_collect)
                result_dict[monitor_name] = future
                wait_task.append(future)
            # wait task end
            done, not_done = concurrent.futures.wait(wait_task, return_when=concurrent.futures.ALL_COMPLETED)
            for key, value_future in list(result_dict.items()):
                try:
                    value_future_res = value_future.result()
                    if len(value_future_res.shape) < 2:
                        raise Exception("数组低于2维度")
                    if value_future_res.size <= 0:
                        raise Exception("数据结果为空")
                    result_dict[key] = value_future_res
                    # 如果是fps 会去掉第一个和 最后一个点
                    if key == "fps":
                        result_dict[key] = result_dict[key][1: -1] if len(
                            result_dict[key]) > 3 else result_dict[key]
                except Exception as e:
                    logger.error(e)
                    result_dict.pop(key, None)

            # 处理公共开始时间, 结束时间
            # logger.info("item{0}".format(result_dict))
            if result_dict:
                public_start_time, public_end_time = cls.get_public_time(result_dict)
                # 获取所有结果
                for (monitor_name, future_result) in result_dict.items():
                    result_dict[monitor_name] = cls.time_value_result(monitor_name, future_result,
                                                                      public_start_time, public_end_time,
                                                                      is_need_relative_time=kwargs.get(
                                                                          "is_need_relative_time", False))
                result_dict["public_start_time"] = public_start_time
                result_dict["public_end_time"] = public_end_time
                img_path_dir = os.path.join(file_dir_path, "picture_log")
                if os.path.exists(img_path_dir):
                    task_dir, task_name_int = os.path.split(file_dir_path)
                    _, host = os.path.split(task_dir)
                    result_dict["public_imgs"] = cls.get_public_imgs(img_path_dir, public_start_time,
                                                                     public_end_time, task_name_int, host)
        return result_dict

    @staticmethod
    def get_public_imgs(img_path_dir: str, public_start_time: int, public_end_time: int, task_name_int: str, host: str):
        all_imgs = os.listdir(img_path_dir)
        img_time_dict = {i: "" for i in range(public_start_time, public_end_time + 1)}
        for img in all_imgs:
            try:
                img_time_dict[int(int(
                    img.replace(".jpg", "")) * 0.001)] = "/static/{0}/{1}/picture_log/{2}".format(host, task_name_int,
                                                                                                  img)
            except Exception as e:
                logger.error(e)
                traceback.print_exc()
                continue
        res_list = []
        for key, v in img_time_dict.items():
            try:
                res_list.append({"time": key, "picture_path": v,
                                 "relative_time": DataCollect.seconds_to_time(int(key) - public_start_time)})
            except Exception as e:
                logger.error(e)
        res_list.sort(key=lambda x: int(x.get("time")))
        return res_list

    @staticmethod
    def get_public_time(result_dict: dict):
        time_collect: list[list] = [list(map(lambda x: int(x), future_result[:, 0])) for monitor_name, future_result in
                                    result_dict.items()]  # 所有的时间[[], []]
        public_start_time, public_end_time = DataCollect.find_common_elements(time_collect)
        return public_start_time, public_end_time

    @staticmethod
    def find_common_elements(lists):

        min_time = None
        max_time = None
        for item_list in lists:
            if not min_time:
                min_time = item_list[0]
            if not max_time:
                max_time = item_list[-1]
            max_time = max(max_time, max(item_list))
            min_time = min(min_time, min(item_list))
        return min_time, max_time

    # 获取不同类型的数据，掐头去尾保证所有的数据起点终点一致
    @staticmethod
    def time_value_result(monitor_name, csv_data, start_time, end_time, **kwargs):
        real_time: list = csv_data[:, 0].tolist()
        value: list = np.round(csv_data[:, 1], 2).tolist()
        value_max = max(value)
        value_min = min(value)
        value_avg = sum(value) / len(value) if value and len(value) else 0
        real_time_int: list = list(map(lambda x: int(x), real_time))
        head_lack_second = real_time_int[0] - start_time
        end_lack_second = end_time - real_time_int[-1]
        head_time = [real_time_int[0] + i for i in range(head_lack_second)]
        end_time = [real_time_int[-1] + i for i in range(end_lack_second)]
        head_time_value = ["-" for i in range(head_lack_second)]
        end_time_value = ["-" for i in range(end_lack_second)]
        res_dict = {"time": head_time + real_time + end_time, "value": head_time_value + value + end_time_value,
                    "max": value_max, "min": value_min, "avg": value_avg}
        if kwargs.get("is_need_relative_time", False):
            res_dict["relative_time"] = [DataCollect.seconds_to_time(item - start_time) for item in
                                         head_time + real_time_int + end_time]
        if monitor_name == "fps":
            try:
                res_dict["full_number"] = max(csv_data[:, 3])  # 满帧
                source_jank_number = csv_data[:, 4].tolist()
                source_big_jank_number = csv_data[:, 5].tolist()
                res_dict["jank_number_sum"] = sum(source_jank_number)
                res_dict["big_jank_number_sum"] = sum(source_big_jank_number)
                res_dict["all_jank_rate"] = (sum(source_jank_number) + sum(source_big_jank_number)) / len(
                    res_dict["time"]) * 100
                res_dict["jank_number"] = head_time_value + source_jank_number + end_time_value  # 卡顿
                res_dict["big_jank_number"] = head_time_value + source_big_jank_number + end_time_value  # 强卡顿
                res_dict["ftimege100"] = head_time_value + csv_data[:, 6].tolist() + end_time_value  # 增量耗时
            except Exception as e:
                res_dict["full_number"] = 0
                res_dict["jank_number"] = []
                res_dict["big_jank_number"] = []
                res_dict["ftimege100"] = []
                res_dict["jank_number_sum"] = 0
                res_dict["big_jank_number_sum"] = 0
                res_dict["all_jank_rate"] = 0
                logger.error(e)
            # fps值需要去掉开头一个和最后一个
            # res_dict["time"] = res_dict["time"][1: -2] if res_dict.get("time") else []
            # res_dict["value"] = res_dict["value"][1: -2] if res_dict.get("value") else []
        return res_dict

    @staticmethod
    def seconds_to_time(time_data_collect):
        minutes = str(time_data_collect // 60).zfill(2)
        seconds = str(time_data_collect % 60).zfill(2)
        return f"{minutes}:{seconds}"
