## Phân tích giá vàng – hướng dẫn chạy dự án

Tài liệu này giúp chuẩn bị môi trường, cài thư viện, kích hoạt virtualenv và chạy ứng dụng.

### Yêu cầu
- Python 3.9+ đã cài trong hệ thống
- PowerShell (Windows)
- Quyền truy cập internet để tải thư viện

### Thiết lập nhanh
1) (Tùy chọn) Clone repo: `git clone https://github.com/ductuongne/PhanTichGiaVang ` rồi `cd PhanTichGiaVang`
2) Tạo môi trường ảo: `python -m venv .venv`
3) Kích hoạt venv: `.\.venv\Scripts\Activate.ps1`
4) Cập nhật `pip`: `python -m pip install --upgrade pip`
5) Cài thư viện: `pip install -r requirements.txt`
6) Chạy ứng dụng Streamlit: `streamlit run app.py`
	- Streamlit sẽ mở trình duyệt; nếu không, xem URL hiển thị trong terminal.
7) Thoát môi trường ảo khi xong: `deactivate`

### Cấu trúc thư mục (rút gọn)
- `app.py`: Điểm vào ứng dụng Streamlit.
- `requirements.txt`: Danh sách thư viện cần thiết.
- `data/`: Lưu dữ liệu đầu vào/mẫu (đang rỗng, có `.gitkeep`).
- `pages/`: Trang phụ cho Streamlit (đa trang).
- `utils/`: Hàm tiện ích, tiền xử lý, cấu hình chung.
- `venv/` hoặc `.venv/`: Môi trường ảo (không cần commit).
- `.gitignore`: Bỏ qua file/thư mục không cần version control.

Ví dụ cây thư mục:

```
PhanTichGiaVang/
├─ app.py #điểm endpoint của chương trình
├─ README.md
├─ requirements.txt #danh sách thư viện cần cài
├─ data/ #dữ liệu đầu vào 
│ 
├─ pages/ #phân trang
│  
├─ utils/ #các file xử lý logic
│  
├─ venv/
└─ .gitignore
```

### Ghi chú phát triển
- Giữ dữ liệu nặng trong `data/` và tránh commit file lớn.
- Tạo trang mới cho Streamlit bằng cách thêm file Python vào `pages/`.
- Đặt hàm tái sử dụng vào `utils/` để dễ quản lý.
