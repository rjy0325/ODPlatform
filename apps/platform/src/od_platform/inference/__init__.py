# apps/platform/src/od_platform/inference/__init__.py
"""推理子系统 (D8)."""
from .pipeline_config import load_pipeline_config, PipelineConfig
from .overlay import FPSCounter, Metrics, draw_hud, draw_pause
from .sinks import OutputSink, LocalFileSink, NullSink
from .hooks import InferHooks, FrameEvent, ProgressEvent
from .cancel import CancelToken, InferenceCancelled

__all__ = [
    # pipeline_config
    "load_pipeline_config", "PipelineConfig",
    # overlay
    "FPSCounter", "Metrics", "draw_hud", "draw_pause",
    # sinks
    "OutputSink", "LocalFileSink", "NullSink",
    # hooks
    "InferHooks", "FrameEvent", "ProgressEvent",
    # cancel
    "CancelToken", "InferenceCancelled",
]