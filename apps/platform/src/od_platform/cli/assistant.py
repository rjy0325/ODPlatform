# apps/platform/src/od_platform/cli/assistant.py
import argparse
from ..assistant.service import analyze_video
from ..assistant.report import save_report

def main():
    parser = argparse.ArgumentParser(description="机场X光安检智能助手")
    parser.add_argument("--video", type=str, required=True, help="安检视频文件路径")
    args = parser.parse_args()
    
    print(f"🚀 开始处理安检视频: {args.video}")
    try:
        report_data = analyze_video(args.video)
        run_id = save_report(report_data)
        print(f"✅ 分析完成！报告已保存至: runs/assistant/{run_id}/")
    except Exception as e:
        print(f"❌ 运行失败: {e}")

if __name__ == "__main__":
    main()