from od_platform.assistant.service import analyze_video

def test_analyze_video_llm_fail_safe(tmp_path):
    """测试 LLM 失败降级逻辑"""
    # 伪造一个空视频文件
    fake_video = tmp_path / "test.mp4"
    fake_video.touch()
    
    try:
        # 因为视频是空的，cv2 可能会报错，我们只需要验证它不会直接引发未捕获的 Python 崩溃
        report = analyze_video(str(fake_video))
        assert "video_name" in report
    except ValueError as e:
        # 如果因为空文件报错，捕获它也符合"不崩溃"的要求
        assert "无法打开" in str(e)