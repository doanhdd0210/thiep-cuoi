/**
 * Nhận lời chúc từ thiệp cưới và lưu vào Google Sheet.
 * Cách cài: xem RSVP-SETUP.md, mục "Lưu lời chúc vào Google Sheet".
 *
 * - Mỗi lời chúc là 1 dòng ở trang tính "Lời chúc": Thời gian | Tên | Lời chúc | Bản | Hiện
 * - Muốn ẩn 1 lời chúc khỏi thiệp: bỏ tick ô "Hiện" ở dòng đó.
 */
var SHEET_NAME = 'Lời chúc';

function sheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(['Thời gian', 'Tên', 'Lời chúc', 'Bản', 'Hiện']);
    sh.setFrozenRows(1);
    sh.setColumnWidths(1, 1, 150); sh.setColumnWidths(2, 1, 160); sh.setColumnWidths(3, 1, 460);
    sh.getRange('E2:E').insertCheckboxes();
  }
  return sh;
}

// chặn công thức ("=...", "+...") khi ghi vào ô
function safe_(t) { t = String(t || ''); return /^[=+\-@]/.test(t) ? "'" + t : t; }

function doPost(e) {
  try {
    var d = JSON.parse(e.postData.contents);
    var name = String(d.name || '').trim().slice(0, 60);
    var msg = String(d.message || '').trim().slice(0, 500);
    if (!name || !msg) return ContentService.createTextOutput('skip');
    var sh = sheet_();
    sh.appendRow([new Date(), safe_(name), safe_(msg), safe_(d.side), true]);
    sh.getRange(sh.getLastRow(), 5).insertCheckboxes().check();
    return ContentService.createTextOutput('ok');
  } catch (err) {
    return ContentService.createTextOutput('error');
  }
}

// Trang thiệp gọi hàm này để hiện "Lời chúc từ mọi người" (60 lời mới nhất, bỏ dòng đã bỏ tick "Hiện")
function doGet() {
  var rows = sheet_().getDataRange().getValues().slice(1);
  var out = rows.filter(function (r) { return r[2] && r[4] !== false; })
    .slice(-60).reverse()
    .map(function (r) { return { name: String(r[1]), message: String(r[2]), at: r[0] }; });
  return ContentService.createTextOutput(JSON.stringify(out)).setMimeType(ContentService.MimeType.JSON);
}
