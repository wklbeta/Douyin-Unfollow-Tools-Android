import xml.etree.ElementTree as ET
import subprocess
import time
import os

# 定义要查找的节点标签和属性值
node_tag = "node"
followed_btn_class = "android.widget.Button"
uiautomator_file_name = "window_dump.xml"
unfollow_btn_content_desc = "已关注，按钮"
list_container_class = "androidx.recyclerview.widget.RecyclerView"


def click_by_text(xml_path, text):
    # 解析XML文件te
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 遍历XML树，查找符合条件的节点
    for elem in root.iter(node_tag):
        if text in elem.attrib.get("text", ""):
            text_center = bounds_str_to_center(elem.attrib.get("bounds", ""))
            subprocess.run(
                f"adb shell input tap {text_center[0]} {text_center[1]}".split()
            )
            return True

    return False


def find_node_bounds(xml_path):
    # 解析XML文件te
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 遍历XML树，查找符合条件的节点
    btn_bounds_center_list = []
    list_container_bounds = []
    for elem in root.iter(node_tag):
        node = elem.find("node")
        if (
            node is not None
            and node.attrib["text"] == "已关注"
            and node.attrib["class"] == followed_btn_class
        ) or (
            unfollow_btn_content_desc in elem.attrib.get("content-desc", "")
            and elem.attrib["text"] == "取消关注"
        ):
            bounds = elem.attrib.get("bounds", "")
            btn_bounds_center_list.append(bounds_str_to_center(bounds))
        if list_container_class in elem.attrib.get("class", ""):
            list_container_bounds = get_bounds(elem.attrib.get("bounds", ""))

    return btn_bounds_center_list, list_container_bounds


def find_node_with_text(xml_path, text):
    # 解析XML文件te
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 遍历XML树，查找符合条件的节点
    for elem in root.iter(node_tag):
        if elem.attrib["text"] == text:
            return bounds_str_to_center(elem.attrib.get("bounds", ""))
    return []


def bounds_str_to_center(bound):
    left, top, right, bottom = get_bounds(bound)
    center = [(left + right) // 2, (top + bottom) // 2]
    return center


def get_bounds(bound):
    [left_top, right_bottom] = bound.split("][")
    left_top = left_top[1:]
    [left, top] = [str(edge) for edge in left_top.split(",")]
    right_bottom = right_bottom[:-1]
    [right, bottom] = [str(edge) for edge in right_bottom.split(",")]
    return int(left), int(top), int(right), int(bottom)


def exit_with_postprocess():
    subprocess.run("adb shell settings put global animator_duration_scale 1".split())
    if os.path.exists(uiautomator_file_name):
        os.remove(uiautomator_file_name)
    exit(1)


def back_reenter(back_times, reenter_text):
    for i in range(back_times):
        subprocess.run("adb shell input keyevent 4".split())
        time.sleep(1)
    print("再次读取UI布局中…")
    result = subprocess.run(
        "adb shell uiautomator dump --compressed".split(), capture_output=True
    )
    if "ERROR" in str(result.stderr):
        print("错误：拿不到UI布局，退出")
        exit_with_postprocess()
    else:
        subprocess.run("adb pull /sdcard/window_dump.xml .".split())
        clicked = click_by_text(uiautomator_file_name, reenter_text)
        if clicked:
            print("等待0.5s")
            time.sleep(0.5)
            return True
        else:
            print(f"错误：个人页找不到“{reenter_text}”入口，退出")
            exit_with_postprocess()


if __name__ == "__main__":
    try_stop_anim = False
    try_back_reenter_profile = False
    try_back_reenter_recently_less_interact = False

    while True:
        print("读取UI布局中…")

        result = subprocess.run(
            "adb shell uiautomator dump --compressed".split(), capture_output=True
        )

        if "ERROR" in str(result.stderr):
            if not try_stop_anim:
                try_stop_anim = True
                print("错误：读取UI布局错误，停止动画后重试")
                subprocess.run(
                    "adb shell settings put global animator_duration_scale 0".split()
                )
                continue
            else:
                print("错误：尝试了停止动画和返回重试，还是获取不到UI布局，退出")
                exit_with_postprocess()
        try_stop_anim = False

        subprocess.run("adb pull /sdcard/window_dump.xml .".split())
        unfollow_btn_centers, list_container_bounds = find_node_bounds(
            uiautomator_file_name
        )

        if len(unfollow_btn_centers) == 0:
            if len(find_node_with_text(uiautomator_file_name, "暂时没有更多了")) != 0:
                if not try_back_reenter_recently_less_interact:
                    try_back_reenter_recently_less_interact = True
                    if back_reenter(1, "近期互动最少的人"):
                        continue
                else:
                    exit_with_postprocess()
            if not try_back_reenter_profile:
                try_back_reenter_profile = True
                print("错误：没有找到“已关注/取消关注”按钮(1)")
                if back_reenter(2, "关注"):
                    continue
            else:
                print("错误：没有找到“已关注/取消关注”按钮(2)")
                exit_with_postprocess()
        try_back_reenter_profile = False
        try_back_reenter_recently_less_interact = False

        if len(list_container_bounds) == 0:
            print("错误：没有找到关注列表的容器")
            exit_with_postprocess()

        print("已关注按钮中心点列表: " + str(unfollow_btn_centers))
        print("关注列表容器边界: " + str(list_container_bounds))
        for center in unfollow_btn_centers:
            subprocess.run(
                "adb shell input tap {} {}".format(center[0], center[1]).split()
            )
        list_container_h_center = (
            list_container_bounds[0] + list_container_bounds[2]
        ) // 2
        list_container_top = list_container_bounds[1]
        list_container_bottom = list_container_bounds[3]
        print("list_container_h_center: " + str(list_container_h_center))
        print("list_container_y_start: " + str(list_container_bottom - 300))
        print(
            "list_container_y_end: "
            + str(
                list_container_top + (list_container_bottom - list_container_top) * 0.63
            )
        )
        print("划动翻页")
        subprocess.run(
            "adb shell input swipe {0} {1} {2} {3} 550".format(
                list_container_h_center,
                list_container_bottom - list_container_h_center,
                list_container_h_center,
                list_container_top,
            ).split(" ")
        )
        # print("停止飞滚")
        # subprocess.run(
        #     "adb shell input tap {} {}".format(
        #         list_container_h_center, list_container_top + 100
        #     ).split()
        # )
        print(
            "================================================================================"
        )
