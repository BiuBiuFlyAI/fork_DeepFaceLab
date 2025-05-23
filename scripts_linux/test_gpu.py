#!/bin/env python



import json

from tensorflow.python.client import device_lib

def get_device_list():
    """
    获取本地设备信息，并将其转换为包含字典的列表，每个字典表示一个设备的关键信息。

    Returns:
        List[Dict[str, str]]: 设备信息列表，每个设备由一个字典表示，包含相关属性。
    """
    devices = device_lib.list_local_devices()
    device_list = []

    for device in devices:
        device_info = {
            'name': device.name,
            'device_type': device.device_type,
            'memory_limit_B': f"{int(device.memory_limit)}",
            'memory_limit_KB': f"{int(device.memory_limit) / 1024:.3f}",
            'memory_limit_MB': f"{int(device.memory_limit) / 1024 ** 2:.3f}",
            'memory_limit_GB': f"{int(device.memory_limit) / 1024 ** 3:.3f}",
            'incarnation': str(device.incarnation)
        }

        # 处理本地性信息
        locality = device.locality
        if locality:
            device_info['locality_bus_id'] = str(locality.bus_id) if locality.bus_id else "N/A"
            # 如果需要，可以进一步处理其他本地性信息

        # 对于GPU，添加额外的信息
        if device.device_type == "GPU":
            device_info['physical_device_desc'] = device.physical_device_desc

        device_list.append(device_info)

    return device_list

if __name__ == "__main__":
    device_list = get_device_list()
    
    for device in device_list:
        print(
            json.dumps(device, indent=4, ensure_ascii=False),
            end="\n\n",
        )
