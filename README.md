# MDAO-Wallet

## Hướng dẫn sử dụng

### 1. Tạo file `1.txt`
- Dán `queryid` vào mỗi dòng, mỗi dòng tương ứng với một tài khoản.

### 2. Tạo file `config.json`
- Cấu hình file `config.json` để điều chỉnh các thiết lập của script. Ví dụ:
    ```json
    {
        "auto_upgrade": true,
        "toolkit_upgrade_cost": 10,
        "workbench_upgrade_cost": 10
    }
    ```
    - `auto_upgrade`: Nếu `true` sẽ tự động nâng cấp, nếu `false` sẽ không tự động nâng cấp.
    - `toolkit_upgrade_cost`: Số token cần thiết để nâng cấp toolkit.
    - `workbench_upgrade_cost`: Số token cần thiết để nâng cấp workbench.

### 3. Cài đặt các thư viện cần thiết
- Chạy lệnh sau để cài đặt các thư viện:
    ```bash
    pip install requests termcolor
    ```

### 4. Chạy script
- Để chạy script, sử dụng lệnh sau:
    ```bash
    python mdao.py
    ```

## Chức năng của script
- Tự động claim token
- Tự động nâng cấp máy đào
- Tự động làm nhiệm vụ

## Tham gia kênh Telegram
- Để cập nhật thông tin mới nhất, tham gia kênh Telegram của chúng tôi:
  [Airdropcrytor](https://t.me/Airdropcrytor)

---

Cảm ơn bạn đã sử dụng MDAO-Wallet!
