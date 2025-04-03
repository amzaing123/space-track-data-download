import subprocess
import os
import pandas as pd
import time


# 1. 读取 NORAD_CAT_ID
def read_norad_ids(file_path):
    try:
        df = pd.read_excel(file_path)
        id_num = df['NORAD_CAT_ID'].tolist()
        # 对id_num从大到小排序并取前80个
        id_num_sorted = sorted(id_num, reverse=True)[:300]
        return id_num_sorted
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return []


# 2. 登录 Space-Track 的函数
def login_space_track():
    login_cmd = (
        'curl -c cookies.txt -b cookies.txt '
        'https://www.space-track.org/ajaxauth/login '
        '-d "identity=your_account&password=your_password"'

    )
    try:
        result = subprocess.run(login_cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("登录成功")
            print(result.stdout)
            return True
        else:
            print("登录失败")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"登录时出错: {e}")
        return False


# 3. 使用 curl 下载数据
def fetch_and_save_tle_data(id_num_list):
    # 保存目录
    save_dir = "unknown_id2"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 初始登录
    if not login_space_track():
        return

    # 基础下载 URL 模板
    base_download_cmd = (
        'curl --cookie cookies.txt '
        'https://www.space-track.org/basicspacedata/query/class/gp_history/NORAD_CAT_ID/{}/'
        'orderby/TLE_LINE1%20ASC/EPOCH/2025-01-01--2025-03-12/format/tle '
        '> "{}"'
    )

    # 计数器和批次大小
    count = 0
    batch_size_small = 29  # 每25个延时60秒
    batch_size_large = 300  # 每300个延时300秒
    delay_short = 60  # 短延时60秒
    delay_long = 300  # 长延时300秒

    # 遍历每个 NORAD_CAT_ID 并下载
    for norad_id in id_num_list:
        # 每下载250个ID，重新登录并延时300秒
        if count > 0 and count % batch_size_large == 0:
            print(f"已下载 {count} 个ID，重新登录并延时 {delay_long} 秒...")
            if os.path.exists("cookies.txt"):
                os.remove("cookies.txt")  # 删除旧的 cookies 文件
            if not login_space_track():
                print("重新登录失败，停止处理")
                break
            time.sleep(delay_long)  # 添加300秒延时

        # 每下载25个ID（但不是250的倍数时），重新登录并延时60秒
        elif count > 0 and count % batch_size_small == 0:
            print(f"已下载 {count} 个ID，重新登录并延时 {delay_short} 秒...")
            if os.path.exists("cookies.txt"):
                os.remove("cookies.txt")  # 删除旧的 cookies 文件
            if not login_space_track():
                print("重新登录失败，停止处理")
                break
            time.sleep(delay_short)  # 添加60秒延时

        try:
            # 构造保存路径
            save_path = os.path.join(save_dir, f"{norad_id}.txt")
            # 构造下载命令
            download_cmd = base_download_cmd.format(norad_id, save_path)
            print(f"正在下载: NORAD_CAT_ID {norad_id}")
            print(f"命令: {download_cmd}")

            # 执行下载命令
            result = subprocess.run(download_cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"已保存: {save_path}")
                print(result.stdout)
            else:
                print(f"下载 {norad_id} 失败")
                print(result.stderr)

            # 计数器加1
            count += 1

        except Exception as e:
            print(f"下载 {norad_id} 时出错: {e}")
            count += 1  # 即使出错也增加计数器，避免无限循环

    # 清理 cookies 文件
    if os.path.exists("cookies.txt"):
        os.remove("cookies.txt")
        print("已清理 cookies.txt")


# 主程序
def main():
    file_path = "rocketbody3.xlsx"
    id_num_list = read_norad_ids(file_path)
    if id_num_list:
        print(f"读取到的NORAD_CAT_ID数量: {len(id_num_list)}")
        fetch_and_save_tle_data(id_num_list)
    else:
        print("未读取到任何NORAD_CAT_ID")


if __name__ == "__main__":
    main()