// コードブロックのコピーボタンで、【タブ】をタブ文字（\t）に置き換えてコピーする。
// Material のコピーボタンは clipboard.js 経由で execCommand("copy") を使うため、
// copy イベントでクリップボードの中身を差し替える。
document.addEventListener("copy", function (e) {
  // clipboard.js は一時的な textarea を選択してコピーする（Firefox は getSelection() が空になる）
  var text = String(document.getSelection()) || (e.target && e.target.value) || "";
  if (text.indexOf("【タブ】") < 0 || !e.clipboardData) return;
  e.clipboardData.setData("text/plain", text.split("【タブ】").join("\t"));
  e.preventDefault();
});
