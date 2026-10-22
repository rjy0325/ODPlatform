#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  : paths.py
# @Author    : ODPlatform Team
# @Project   : ODPlatform
# @Function  : 集中定义项目路径常量

from pathlib import Path
from typing import List, Tuple

# ============================================================
# Workspace 根目录定位
# ============================================================
WORKSPACE_MARKER: str = ".odp-workspace"

def _find_workspace_root(start: Path, markers: Tuple[str, ...] = (WORKSPACE_MARKER,)) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent

    for parent in [current, *current.parents]:
        for marker in markers:
            if (parent / marker).exists():
                return parent

    raise FileNotFoundError(f"找不到 workspace marker 文件 ({markers})。请确认仓库根存在 {WORKSPACE_MARKER} 文件。")

ROOT_DIR: Path = _find_workspace_root(Path(__file__))

# ============================================================
# 端根目录 APP_DIR
# ============================================================
APP_DIR: Path = ROOT_DIR / "apps" / "platform"

# ============================================================
# 共享资产
# ============================================================
DATA_DIR: Path = ROOT_DIR / "data"
MODELS_DIR: Path = ROOT_DIR / "models"
RUNS_DIR: Path = ROOT_DIR / "runs"

PRETRAINED_MODELS_DIR: Path = MODELS_DIR / "pretrained"
TRAINED_MODELS_DIR: Path = MODELS_DIR / "trained"

RAW_DATA_DIR: Path = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"

# ============================================================
# 端私有资产
# ============================================================
CONFIGS_DIR: Path = APP_DIR / "configs"
LOGGING_DIR: Path = APP_DIR / "logging"
UNIT_TEST_DIR: Path = APP_DIR / "tests"

# ============================================================
# 顶层共享目录
# ============================================================
DOCS_DIR: Path = ROOT_DIR / "docs"
SCRIPTS_DIR: Path = ROOT_DIR / "scripts"

# ============================================================
# 【新增】工具元数据目录 (audit trail / 工具自身日志)
# ============================================================
# 业务工具(train/val/inference)的日志 -> LOGGING_DIR, 会被 reset 清理
# 元工具(reset/doctor/upgrade)的日志 -> META_LOGGING_DIR, 是对清理动作本身的审计追踪
META_DIR: Path = ROOT_DIR / ".odp-meta"
META_LOGGING_DIR: Path = META_DIR / "logs"

# ============================================================
# 要初始化的目录列表
# ============================================================
def get_dirs_to_initialize() -> List[Path]:
    return [
        # 共享资产
        DATA_DIR, RUNS_DIR, MODELS_DIR, PRETRAINED_MODELS_DIR, TRAINED_MODELS_DIR,
        RAW_DATA_DIR, PROCESSED_DATA_DIR,
        # 端私有资产
        CONFIGS_DIR, LOGGING_DIR, UNIT_TEST_DIR,
        # 工程基础设施
        SCRIPTS_DIR, DOCS_DIR,
        # 【新增】元工具数据（reset 等元工具的审计日志位置）
        META_LOGGING_DIR,
    ]

# ============================================================
# reset 专用清理清单
# ============================================================
def get_dirs_to_reset() -> List[Path]:
    # 注意：META_LOGGING_DIR 绝对不在这里！不能自己清理自己！
    return [
        PROCESSED_DATA_DIR,
        RUNS_DIR,
        TRAINED_MODELS_DIR,
        LOGGING_DIR,
    ]

# ============================================================
# 【新增】绝对保护目录
# ============================================================
PROTECTED_DIRS: Tuple[Path, ...] = (
    ROOT_DIR,
    ROOT_DIR / "apps",
    ROOT_DIR / "packages",
    APP_DIR,
    APP_DIR / "src",
    SCRIPTS_DIR,
    DOCS_DIR,
    UNIT_TEST_DIR,
    CONFIGS_DIR,
    ROOT_DIR / ".git",
    ROOT_DIR / ".odp-workspace",
    # 【新增】工具元数据根与日志目录，审计追踪不可被破坏
    META_DIR,
    META_LOGGING_DIR,
)

def is_protected(path: Path) -> bool:
    path = path.resolve(strict=False)
    for protected in PROTECTED_DIRS:
        protected_resolved = protected.resolve(strict=False)
        if path == protected_resolved:
            return True
        if protected_resolved.is_relative_to(path):
            return True
    return False

# ============================================================
# 测试入口
# ============================================================
if __name__ == "__main__":
    print(f"ROOT_DIR (workspace) = {ROOT_DIR}")
    print(f"META_DIR (tool data) = {META_DIR}")
    print(f"\n要初始化的目录共 {len(get_dirs_to_initialize())} 个:")
    for d in get_dirs_to_initialize():
        print(f"  - {d.relative_to(ROOT_DIR)}")