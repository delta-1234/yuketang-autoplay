from DrissionPage import ChromiumPage
import time

def get_sections(page):
    """获取所有小节元素"""
    sections = []
    # 获取所有章节
    chapters = page.eles('.leaf-title text-ellipsis')
    for chapter in chapters:
        if '视频' in chapter.text:
            sections.append(chapter)
    return sections

def wait_until_finished(tab, timeout=7200):
    """等待完成度=100%"""
    start_time = time.time()
    while True:
        ele = tab.ele('xpath=//span[contains(text(), "完成度")]')
        if ele:
            text = ele.text.strip()
            # print("当前进度：", text)
            if "100%" in text:
                print("视频已完成！")
                break
        # 超时保护
        if time.time() - start_time > timeout:
            print("等待超时，强制退出")
            break
        time.sleep(10)  # 每 10 秒检查一次

def open_section_and_play(sec, page):
    """点击小节进入新页面并播放"""
    try:
        # 点击小节，会新开一个 tab
        sec.click()
        time.sleep(2)

        # 获取新开的标签页
        new_tab = page.latest_tab

        # 点击播放按钮
        play_btn = new_tab.ele('.play-status-box')
        if play_btn:
            play_btn.click()
            print("播放中...")

        wait_until_finished(new_tab)

        # 播放完后关闭该标签页
        new_tab.close()
    except:
        pass

def auto_course(url):
    """自动刷课流程"""
    page = ChromiumPage()
    page.get(url)
    sections = get_sections(page)
    print(f"共找到 {len(sections)} 个小节")

    for idx, sec in enumerate(sections, 1):
        print(f"\n进入第 {idx} 节课...")
        open_section_and_play(sec, page)

if __name__ == "__main__":
    urls = "https://buaa.yuketang.cn/pro/lms/CTmmnGpxVGJ/28502700/studycontent" #新时代
    auto_course(urls)


