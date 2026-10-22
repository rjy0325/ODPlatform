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
# 工具元数据目录
# ============================================================
META_DIR: Path = ROOT_DIR / ".odp-meta"
META_LOGGING_DIR: Path = META_DIR / "logs"


# ============================================================
# 【新增】数据集相关路径 (D3 增量)
# ============================================================
# 数据集 yaml 的家 (Ultralytics 约定)
DATASET_CONFIGS_DIR: Path = CONFIGS_DIR / "datasets"

def raw_dataset_root(name: str) -> Path:
    return RAW_DATA_DIR / name

def dataset_processed_dir(name: str) -> Path:
    return PROCESSED_DATA_DIR / name

def dataset_yaml_path(name: str) -> Path:
    return DATASET_CONFIGS_DIR / f"{name}.yaml"


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
        # 元工具数据
        META_LOGGING_DIR,
        # 【新增】数据集配置目录
        DATASET_CONFIGS_DIR,
    ]

# ============================================================
# reset 专用清理清单
# ============================================================
def get_dirs_to_reset() -> List[Path]:
    return [
        PROCESSED_DATA_DIR,
        RUNS_DIR,
        TRAINED_MODELS_DIR,
        LOGGING_DIR,
    ]

# ============================================================
# 绝对保护目录
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
    print(f"DATASET_CONFIGS_DIR  = {DATASET_CONFIGS_DIR}")
    print(f"\n要初始化的目录共 {len(get_dirs_to_initialize())} 个:")
    for d in get_dirs_to_initialize():
        print(f"  - {d.relative_to(ROOT_DIR)}")