import requests
from termcolor import colored
import json
import time
import random

# Đọc cấu hình tự động nâng cấp từ file JSON
with open('config.json', 'r') as file:
    config = json.load(file)

# URL và headers cho các yêu cầu API
profile_url = "https://zavod-api.mdaowallet.com/user/profile"
claim_url = "https://zavod-api.mdaowallet.com/user/claim"
missions_url = "https://zavod-api.mdaowallet.com/missions?offset=0&status=ACTIVE"
upgrade_toolkit_url = "https://zavod-api.mdaowallet.com/user/upgradeToolkit"
upgrade_workbench_url = "https://zavod-api.mdaowallet.com/user/upgradeWorkbench"

# Màu sắc cho logo và các thông tin khác
logo_colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta', 'white']
info_colors = ['cyan', 'green', 'yellow']

def print_logo(text):
    for i, char in enumerate(text):
        color = logo_colors[i % len(logo_colors)]
        print(colored(char, color), end="")
    print()

def get_proxies():
    with open('proxies.txt', 'r') as file:
        proxies = [line.strip() for line in file.readlines()]
    return proxies

def confirm_mission(mission_id, headers, session):
    confirm_url = f"https://zavod-api.mdaowallet.com/missions/confirm/telegram/{mission_id}"
    confirm_response = session.post(confirm_url, headers=headers)
    return confirm_response.status_code == 200

def claim_mission(mission_id, headers, session):
    claim_mission_url = f"https://zavod-api.mdaowallet.com/missions/claim/{mission_id}"
    claim_response = session.post(claim_mission_url, headers=headers)
    return claim_response.status_code == 200

def upgrade_toolkit(headers, session):
    response = session.post(upgrade_toolkit_url, headers=headers)
    return response.status_code == 200

def upgrade_workbench(headers, session):
    response = session.post(upgrade_workbench_url, headers=headers)
    return response.status_code == 200

def process_account(telegram_init_data, proxy):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Origin": "https://zavod.mdaowallet.com",
        "Referer": "https://zavod.mdaowallet.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Telegram-Init-Data": telegram_init_data,
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }

    session = requests.Session()
    session.proxies = {
        "http": proxy,
        "https": proxy,
    }

    # Thực hiện yêu cầu GET để lấy thông tin người dùng
    response = session.get(profile_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print_logo("DWANDEV")
        print(colored("Đăng nhập thành công", info_colors[0]))
        print(colored(f"Tên tài khoản: {data['username']}", info_colors[1]))
        print(colored(f"ID tài khoản: {data['telegramId']}", info_colors[2]))
        print(colored(f"Token hiện có: {data['tokens']}", info_colors[0]))

        if config['auto_upgrade']:
            print(colored("Bắt đầu tự động nâng cấp...", 'blue'))
            toolkit_upgrade_cost = config.get('toolkit_upgrade_cost', 10)
            workbench_upgrade_cost = config.get('workbench_upgrade_cost', 10)
            while data['tokens'] >= min(toolkit_upgrade_cost, workbench_upgrade_cost):
                upgraded = False
                if data['tokens'] >= toolkit_upgrade_cost:
                    if upgrade_toolkit(headers, session):
                        print(colored("Nâng cấp Toolkit thành công", 'green'))
                        upgraded = True
                if data['tokens'] >= workbench_upgrade_cost:
                    if upgrade_workbench(headers, session):
                        print(colored("Nâng cấp Workbench thành công", 'green'))
                        upgraded = True
                if not upgraded:
                    break
                response = session.get(profile_url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
            print(colored("Hoàn tất quá trình nâng cấp", 'blue'))

        # Thực hiện yêu cầu POST để claim token
        claim_response = session.post(claim_url, headers=headers)

        if claim_response.status_code == 200:
            claim_data = claim_response.json()
            if claim_data.get('status') == 'success':
                print(colored(f"Claim thành công. Số token bạn hiện có là: {claim_data['tokens']}", info_colors[1]))
            else:
                print(colored("Đang thực hiện claim, chưa thể claim lúc này", info_colors[2]))
        else:
            print(colored("Claim không thành công. Vui lòng thử lại sau.", 'red'))

        # Kiểm tra trạng thái nhiệm vụ
        missions_response = session.get(missions_url, headers=headers)

        if missions_response.status_code == 200:
            missions_data = missions_response.json()
            print_logo("NHIỆM VỤ")
            for mission in missions_data['missions']:
                print(colored(f"Tên nhiệm vụ: {mission['name']['en']}", info_colors[1]))
                print(colored(f"Mô tả: {mission['description']['en']}", info_colors[2]))
                print(colored(f"Phần thưởng: {mission['prize']} tokens", info_colors[0]))
                print(colored(f"Trạng thái: {mission['status']}", info_colors[1]))
                print(colored(f"Đã claim: {'Yes' if mission['claimed'] else 'No'}", info_colors[2]))
                print(colored(f"Trạng thái hiện tại: {mission['state']}", info_colors[0]))
                print('-' * 40)

                # Tự động thực hiện nhiệm vụ nếu chưa hoàn thành
                if mission['state'] == 'STARTED' and not mission['claimed']:
                    success = confirm_mission(mission['id'], headers, session)
                    if success:
                        print(colored(f"Nhiệm vụ {mission['name']['en']} đã được thực hiện thành công.", 'green'))
                    else:
                        print(colored(f"Nhiệm vụ {mission['name']['en']} không thể thực hiện. Vui lòng thử lại sau.", 'red'))

                # Tự động claim nhiệm vụ nếu có thể
                if mission['state'] == 'READY_TO_CLAIM' and not mission['claimed']:
                    claim_success = claim_mission(mission['id'], headers, session)
                    if claim_success:
                        print(colored(f"Nhiệm vụ {mission['name']['en']} đã được claim thành công.", 'green'))
                    else:
                        print(colored(f"Nhiệm vụ {mission['name']['en']} không thể claim. Vui lòng thử lại sau.", 'red'))
        else:
            print(colored("Không thể lấy thông tin nhiệm vụ. Vui lòng thử lại sau.", 'red'))
    else:
        print_logo("DWANDEV")
        print(colored(f"Failed to get data: {response.status_code}", 'red'))

def main():
    with open('1.txt', 'r') as file:
        accounts = file.readlines()

    proxies = get_proxies()

    while True:
        for account in accounts:
            account = account.strip()
            proxy = random.choice(proxies)
            process_account(account, proxy)

        print("==============Tất cả tài khoản đã được xử lý=================")
        for i in range(30, 0, -1):
            print(f"Đang xử lý lại tất cả tài khoản trong {i} giây...", end='\r')
            time.sleep(1)
        print()

if __name__ == "__main__":
    main()
