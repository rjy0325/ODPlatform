# apps/platform/src/od_platform/assistant/service.py
import os
import cv2
import logging
from collections import Counter
from openai import OpenAI
from .prompt import build_prompt
from .types import AssistantReport, Statistics, HighRiskEvent

logger = logging.getLogger(__name__)

def analyze_video(video_path: str) -> AssistantReport:
    logger.info(f"开始分析安检视频: {video_path}")
    
    # 1. 抽帧 (限制采样率：每 1 秒 1 帧)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"无法打开视频文件: {video_path}")
        
    fps = cap.get(cv2.CAP_PROP_FPS)
    skip_frames = int(fps) if fps > 0 else 30 
    
    counter = Counter()
    high_risk_events = [] 
    frame_id = 0
    analyzed_frames = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_id % skip_frames == 0:
            analyzed_frames += 1
            current_sec = frame_id // skip_frames
            
            # 模拟 YOLO 推理（后续需替换为真实模型输出）
            if current_sec % 5 == 0: 
                counter["lighter"] += 1
                high_risk_events.append({
                    "time_sec": current_sec,
                    "object": "打火机",
                    "confidence": 0.92
                })
        frame_id += 1
    cap.release()

    stats_data = {
        "analyzed_frames": analyzed_frames,
        "object_counts": dict(counter),
        "high_risk_events": high_risk_events
    }

    # 2. 调用大模型 (带 fail-safe 降级)
    llm_text = ""
    try:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("环境变量中未配置 DEEPSEEK_API_KEY")

        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )

        # 调用外部模块构建 Prompt
        prompt = build_prompt(stats_data)
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个严谨的安检分析助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        llm_text = response.choices[0].message.content

    except Exception as e:
        logger.error(f"LLM 调用失败，触发降级逻辑: {e}")
        llm_text = "⚠️ 智能解读服务暂时不可用，请查看下方原始统计数据。"

    # 3. 严格按照 Pydantic 模型返回数据
    return AssistantReport(
        video_name=os.path.basename(video_path),
        statistics=Statistics(
            analyzed_frames=stats_data["analyzed_frames"],
            object_counts=stats_data["object_counts"],
            high_risk_events=[HighRiskEvent(**event) for event in stats_data["high_risk_events"]]
        ),
        llm_interpretation=llm_text
    )