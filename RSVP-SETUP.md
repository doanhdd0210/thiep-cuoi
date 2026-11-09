# Thiệp cưới Đức Doanh & Huyền Trang

Trang tĩnh thuần HTML/CSS/JS, không cần build. Deploy cả thư mục `thiep-cuoi/` (bỏ qua `_old-cinelove/` nếu muốn nhẹ).

## Cá nhân hoá link cho từng khách
- `https://<domain>/?to=Anh Nam & gia đình` → hiện tên khách ở trang bìa + dòng "Trân trọng kính mời" (không có `?to=` thì hiện "Bạn & người thương").
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
`CONFIG.events` (đang có Lễ ăn hỏi 28/11 07:15, Lễ vu quy 29/11 13:45, Lễ thành hôn 29/11 15:15; icon: party, rings, clock, glass, dish) và `CONFIG.dressCode` (mã màu, đang trống = ẩn) ở đầu phần `<script>` của `index.html`.

## Phiên bản cũ
`_old-cinelove/` chứa thiệp CineLove cũ, bản nâu đỏ theo mẫu in (`index-maroon-card.html`) và bản xanh olive (`index-green-lami.html`). Muốn chạy thì copy ra thư mục gốc đổi tên `index.html`.

## Ảnh xem trước khi share Zalo/Facebook
Đổi `og:image` trong `<head>` thành link tuyệt đối `https://<domain>/img/og.jpg`.
