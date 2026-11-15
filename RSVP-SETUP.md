# Thiệp cưới Đức Doanh & Huyền Trang

Trang tĩnh thuần HTML/CSS/JS, không cần build. Deploy cả thư mục `thiep-cuoi/` (bỏ qua `_old-cinelove/` nếu muốn nhẹ).

## Cá nhân hoá link cho từng khách
- `https://<domain>/?to=Anh Nam & gia đình` → hiện tên khách ở trang bìa + dòng "Trân trọng kính mời" (không có `?to=` thì hiện "Quý khách"; luôn thêm " & người thương" sau tên).
- Thêm `&gio=11:00&ngay=28` để đổi giờ/ngày bữa cơm thân mật (mặc định 15:00, ngày 29). Âm lịch tự tính (ngày 10–30/11).

## Nhạc nền
`music.mp3` (cạnh `index.html`) đang là nhạc cắt từ video mẫu, phát khi khách bấm mở thiệp. Muốn đổi bài thì thay file này, nhớ dùng nhạc bạn có bản quyền.

## Nhận RSVP + lời chúc vào Google Sheet
1. Tạo Google Sheet, đặt hàng 1: `Thời gian | Tên | Tham dự | Số người | Lời chúc`.
2. Extensions → Apps Script, dán:
```js
function doPost(e) {
  var d = JSON.parse(e.postData.contents);
  SpreadsheetApp.getActiveSheet().appendRow([new Date(), d.name, d.attend, d.guests, d.message]);
  return ContentService.createTextOutput('ok');
}
```
3. Deploy → New deployment → Web app → Execute as *Me*, access *Anyone* → copy URL.
4. Dán URL vào `CONFIG.rsvpEndpoint` trong `index.html`.

## Mừng cưới
Điền `bank` + `number` (và `qr` nếu có ảnh QR trong `img/`) trong `CONFIG.gifts` → nút "Mừng cưới" + popup tự hiện (đang ẩn vì chưa có số tài khoản).

## Timeline / Dresscode
`CONFIG.events` (đang có Lễ ăn hỏi 28/11 07:30, Tiệc chính 17:00, Chung vui âm nhạc 19:00–22:00, Lễ vu quy 29/11 13:30, Lễ thành hôn 29/11 15:15; icon: party, rings, clock, glass, music, dish) và `CONFIG.dressCode` (mã màu, đang trống = ẩn) ở đầu phần `<script>` của `index.html`.

## Phiên bản cũ
`_old-cinelove/` chứa thiệp CineLove cũ, bản nâu đỏ theo mẫu in (`index-maroon-card.html`) và bản xanh olive (`index-green-lami.html`). Muốn chạy thì copy ra thư mục gốc đổi tên `index.html`.

## Ảnh xem trước khi share Zalo/Facebook
Đổi `og:image` trong `<head>` thành link tuyệt đối `https://<domain>/img/og.jpg`.

## Hai bản thiệp: nhà trai / nhà gái

- Nhà trai (mặc định): `https://doanhdd0210.github.io/thiep-cuoi/?to=Tên khách`
- Nhà gái: `https://doanhdd0210.github.io/thiep-cuoi/gai/?to=Tên khách` (hoặc `...?ben=gai&to=Tên khách`)
- Nội dung từng bên (lễ chính, địa điểm, giờ, lễ nổi bật) sửa trong `CONFIG.sides`; danh sách lễ trong "Lịch trình" (gom theo ngày, cả hai bản giống nhau) sửa ở `CONFIG.events` ở `index.html`.
- Bản nhà gái đảo thứ tự "Nhà Gái" lên trước ở phần bố mẹ hai họ, đếm ngược theo giờ Lễ Vu Quy.

## Lưu lời chúc vào Google Sheet (và hiện "Lời chúc từ mọi người" trên thiệp)

1. Vào https://sheets.new, tạo Google Sheet mới, đặt tên tuỳ ý (vd "Lời chúc thiệp cưới").
2. Menu **Tiện ích mở rộng → Apps Script**. Xoá code mẫu, dán toàn bộ nội dung file `google-apps-script.gs` vào, bấm Lưu.
3. Bấm **Triển khai → Tạo bản triển khai mới** → loại **Ứng dụng web**:
   - *Thực thi bằng tư cách*: **Tôi**
   - *Người có quyền truy cập*: **Bất kỳ ai**
   Bấm Triển khai, cấp quyền khi Google hỏi (hiện cảnh báo "chưa xác minh" thì chọn Nâng cao → Tiếp tục).
4. Copy **URL ứng dụng web** (dạng `https://script.google.com/macros/s/.../exec`) rồi gửi cho Claude, hoặc dán vào `rsvpEndpoint` trong `index.html`.
5. Mỗi lời chúc sẽ thành 1 dòng ở trang tính "Lời chúc" (tự tạo). Muốn ẩn lời chúc nào khỏi thiệp: bỏ tick cột **Hiện** ở dòng đó.

## Link riêng cho từng khách nhà gái

- Link gọn: `https://doanhdd0210.github.io/thiep-cuoi/gai/<ten-khach>/` (vd `.../gai/anh-hung/`), thanh địa chỉ giữ nguyên, ảnh xem trước ghi tên khách.
- Khi đổi danh sách khách hoặc sửa `index.html`: chạy `python3 build_guests.py "/đường/dẫn/Cưới.xlsx"` rồi commit + push. Script dựng lại toàn bộ trang và cập nhật cột link trong Excel.
- Link kiểu cũ `?to=Tên` vẫn dùng được.
