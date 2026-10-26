# apps/platform/src/od_platform/assistant/prompt.py
import json

def build_prompt(stats_data: dict) -> str:
    """
    把结构化检测结果转成 prompt（喂 JSON，不要让模型"看图猜"）
    """
    json_str = json.dumps(stats_data, ensure_ascii=False, indent=2)
    
    prompt = f"""你是一个专业的机场安检辅助系统。
请根据以下 X 光机检测到的违禁品统计结果（JSON 格式），用严肃、专业的中文撰写一份简短的安检报告。
重点说明查获了哪些违禁品（如打火机）、出现的时段，并给出安检员的处置建议。

统计数据：
{json_str}
"""
    return prompt