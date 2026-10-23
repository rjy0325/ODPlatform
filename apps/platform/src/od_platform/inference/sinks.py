#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  : sinks.py
# @Project   : ODPlatform
# @Function  : 推理结果输出适配器 (OutputSink 抽象 + LocalFileSink + NullSink)
"""推理结果输出适配器..."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from pathlib import Path

import numpy as np
from PIL import Image

# from od_platform.frame_source import SourceType  # 等写 frame_source 时再解开
from enum import Enum
class SourceType(Enum):
    VIDEO = "video"
    CAMERA = "camera"
    IMAGE = "image"

logger = logging.getLogger(__name__)


class OutputSink(ABC):
    """推理结果输出适配器."""
    @abstractmethod
    def open(self, output_dir: Path, source_type: SourceType) -> None:
        pass

    @abstractmethod
    def write(self, frame, annotated: np.ndarray) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class LocalFileSink(OutputSink):
    """本地文件 sink — 视频源写 mp4, 图片源写 jpg."""
    def __init__(self) -> None:
        self.output_dir: Path | None = None
        self._is_stream: bool = False
        self._video = None
        self._count: int = 0

    def open(self, output_dir: Path, source_type: SourceType) -> None:
        self.output_dir = output_dir
        self._is_stream = source_type in (SourceType.VIDEO, SourceType.CAMERA)

    def write(self, frame, annotated) -> None:
        import cv2
        try:
            if self._is_stream:
                if self._video is None:
                    h, w = annotated.shape[:2]
                    fps = float(frame.info.fps) if getattr(frame.info, "fps", None) else 30.0
                    out = self.output_dir / "output.mp4"
                    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                    self._video = cv2.VideoWriter(str(out), fourcc, fps, (w, h))
                self._video.write(annotated)
            else:
                fname = frame.info.filename or f"frame_{frame.info.frame_index:06d}"
                # 加上参数 [cv2.IMWRITE_JPEG_QUALITY, 95] 显式告诉 OpenCV 用 JPEG 格式写
                                # 替换掉 cv2.imwrite，改用 PIL 保存
                save_path = str(self.output_dir / f"{Path(fname).stem}.jpg")
                img_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                Image.fromarray(img_rgb).save(save_path, format="JPEG", quality=95)
            self._count += 1
        except Exception as e:
            logger.warning(f"LocalFileSink.write 失败, 跳过: {e}")

    def close(self) -> None:
        if self._video is not None:
            try:
                self._video.release()
            except Exception as e:
                logger.warning(f"LocalFileSink.close release 失败 (已吞): {e}")
            finally:
                self._video = None


class NullSink(OutputSink):
    """什么也不写."""
    def open(self, output_dir: Path, source_type: SourceType) -> None:
        pass

    def write(self, frame, annotated) -> None:
        pass

    def close(self) -> None:
        pass