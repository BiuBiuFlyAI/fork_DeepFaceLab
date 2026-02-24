#!/bin/env python


import json
import os
from typing import List, Dict, Any

import torch


def _bytes_to_strs(b: int) -> Dict[str, str]:
    """把字节数转换为 B/KB/MB/GB 字符串（保留三位小数）"""
    return {
        "memory_limit_B": f"{int(b)}",
        "memory_limit_KB": f"{int(b) / 1024:.3f}",
        "memory_limit_MB": f"{int(b) / 1024 ** 2:.3f}",
        "memory_limit_GB": f"{int(b) / 1024 ** 3:.3f}",
    }


def get_device_list() -> List[Dict[str, Any]]:
    devices: List[Dict[str, Any]] = []

    # CPU 条目（始终存在）
    cpu_info: Dict[str, Any] = {
        "name": "cpu",
        "device_type": "CPU",
        "index": None,
        # CPU 总内存在这里未探测（跨平台差异），如需可以使用 psutil 获取
        "memory_limit_B": "N/A",
        "memory_limit_KB": "N/A",
        "memory_limit_MB": "N/A",
        "memory_limit_GB": "N/A",
        "num_logical_cpus": os.cpu_count(),
    }
    devices.append(cpu_info)

    # 检查 MPS（Apple Silicon）
    # 在 torch 1.13.1 上如果构建并支持 MPS，则可以通过 torch.backends.mps.is_available() 得知
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        mps_info: Dict[str, Any] = {
            "name": "mps",
            "device_type": "MPS",
            "index": None,
            # PyTorch 对 MPS 没有像 CUDA 那样公开 total memory 属性
            "memory_limit_B": "N/A",
            "memory_limit_KB": "N/A",
            "memory_limit_MB": "N/A",
            "memory_limit_GB": "N/A",
            "is_available": True,
        }
        devices.append(mps_info)

    # CUDA（GPU）
    if torch.cuda.is_available():
        try:
            count = torch.cuda.device_count()
        except Exception:
            count = 0

        for i in range(count):
            try:
                props = torch.cuda.get_device_properties(i)
            except Exception:
                # 万一取属性失败，仍然插入基本信息
                gpu_info = {
                    "name": f"cuda:{i}",
                    "device_type": "GPU",
                    "index": i,
                    "memory_limit_B": "N/A",
                    "memory_limit_KB": "N/A",
                    "memory_limit_MB": "N/A",
                    "memory_limit_GB": "N/A",
                    "is_available": True,
                }
                devices.append(gpu_info)
                continue

            total_mem = int(getattr(props, "total_memory", 0))
            mem_strs = _bytes_to_strs(total_mem)

            gpu_info: Dict[str, Any] = {
                "name": getattr(props, "name", f"cuda:{i}"),
                "device_type": "GPU",
                "index": i,
                "device_str": f"cuda:{i}",
                "is_available": True,
                # 显存信息（以总显存为准）
                "memory_limit_B": mem_strs["memory_limit_B"],
                "memory_limit_KB": mem_strs["memory_limit_KB"],
                "memory_limit_MB": mem_strs["memory_limit_MB"],
                "memory_limit_GB": mem_strs["memory_limit_GB"],
                # 额外可用属性（如果存在）
                "major": getattr(props, "major", None),
                "minor": getattr(props, "minor", None),
                "capability": f"{getattr(props, 'major', '?')}.{getattr(props, 'minor', '?')}",
                "multi_processor_count": getattr(props, "multi_processor_count", None),
                "total_memory_bytes": total_mem,
            }
            devices.append(gpu_info)

    # 在字典中添加运行时/版本信息（可选）
    runtime_info = {
        "torch_version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_version": getattr(torch.version, "cuda", None),
    }
    # 把 runtime_info 作为首个元素（或单独返回）
    # 这里选择放在列表开头作为第一条记录（如果你不想，可以注释掉）
    devices.insert(0, {"runtime_info": runtime_info})

    return devices


if __name__ == "__main__":
    device_list = get_device_list()
    print(json.dumps(device_list, indent=4, ensure_ascii=False))
