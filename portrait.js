/* 原创角色沈晚。同一张脸，14 套衣服按日期轮换。 */
const OUTFITS = [
  { name: "深灰高领，黑风衣", file: "outfit-01.png" },
  { name: "白衬衫，墨蓝背心裙", file: "outfit-02.png" },
  { name: "藏蓝开衫，浅灰内搭", file: "outfit-03.png" },
  { name: "黑裙，细银链", file: "outfit-04.png" },
  { name: "米白衬衫，深棕长裤", file: "outfit-05.png" },
  { name: "墨绿针织裙，短黑外套", file: "outfit-06.png" },
  { name: "浅灰卫衣，敞着的深蓝衬衫", file: "outfit-07.png" },
  { name: "黑高领，驼色开衫", file: "outfit-08.png" },
  { name: "立领白衬衣，炭灰马甲", file: "outfit-09.png" },
  { name: "酒红内搭，黑外套长裙", file: "outfit-10.png" },
  { name: "雾蓝衬衫裙，深色腰带", file: "outfit-11.png" },
  { name: "细条纹衬衫，焦糖开襟毛衣", file: "outfit-12.png" },
  { name: "全黑套装，小银耳钉", file: "outfit-13.png" },
  { name: "深紫高领，浅灰大衣", file: "outfit-14.png" }
];

function outfitForDate(dateStr) {
  const parts = dateStr.split("-").map(Number);
  const days = Math.floor(Date.UTC(parts[0], parts[1] - 1, parts[2]) / 86400000);
  const index = ((days % OUTFITS.length) + OUTFITS.length) % OUTFITS.length;
  return { index, outfit: OUTFITS[index] };
}
