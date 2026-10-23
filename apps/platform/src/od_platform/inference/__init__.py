# apps/platform/src/od_platform/inference/__init__.py
"""ODPlatform 推理子系统对外面板."""
from .cancel import CancelToken, InferenceCancelled
from .hooks import FrameEvent, InferHooks, ProgressEvent
from .pipeline_config import PipelineConfig, load_pipeline_config
# ⚠️ 如果你还没有写完 service.py，这行会导致导入报错
from .service import InferResult, InferService, InferStats, infer_yolo, log_infer_stats
from .sinks import LocalFileSink, NullSink, OutputSink

__all__ = [
    "infer_yolo",
    "InferService", "InferResult", "InferStats", "log_infer_stats",
    "PipelineConfig", "load_pipeline_config",
    "OutputSink", "LocalFileSink", "NullSink",
    "InferHooks", "FrameEvent", "ProgressEvent",
    "CancelToken", "InferenceCancelled",
]