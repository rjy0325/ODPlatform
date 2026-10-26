# apps/platform/src/od_platform/assistant/report.py
import os
import json
import time
from .types import AssistantReport

def save_report(report_data: AssistantReport) -> str:
    """保存报告并返回 run_id"""
    run_id = time.strftime("%Y%m%d_%H%M%S") + "_" + report_data.video_name.split('.')[0]
    save_dir = os.path.join("runs", "assistant", run_id)
    os.makedirs(save_dir, exist_ok=True)
    
    # 因为 report_data 是 Pydantic 对象，必须先转成字典才能存 JSON
    data_dict = report_data.model_dump()
    
    # 存 JSON
    with open(os.path.join(save_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=2)
        
    # 存 Markdown
    with open(os.path.join(save_dir, "report.md"), "w", encoding="utf-8") as f:
        f.write(f"# 安检视频分析报告: {report_data.video_name}\n\n")
        f.write("## 一、 AI 智能解读\n\n")
        f.write(report_data.llm_interpretation + "\n\n")
        f.write("## 二、 原始统计数据\n\n")
        f.write("```json\n")
        f.write(json.dumps(data_dict["statistics"], ensure_ascii=False, indent=2))
        f.write("\n```\n")
        
    return run_id