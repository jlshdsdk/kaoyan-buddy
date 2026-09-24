/* 原创角色沈晚。同一张脸，30 套衣服按日期轮换。身材偏丰满。 */
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
  { name: "深紫高领，浅灰大衣", file: "outfit-14.png" },
  { name: "浅驼风衣，黑高领", file: "outfit-15.png" },
  { name: "奶白针织，深灰半裙", file: "outfit-16.png" },
  { name: "藏蓝衬衫，黑长裤", file: "outfit-17.png" },
  { name: "灰绿开衫，白内搭", file: "outfit-18.png" },
  { name: "米白衬衫，黑吊带", file: "outfit-19.png" },
  { name: "深棕大衣，奶油高领", file: "outfit-20.png" },
  { name: "浅蓝衬衫，藏青背心", file: "outfit-21.png" },
  { name: "白衬衫，浅灰长裙", file: "outfit-22.png" },
  { name: "暗红高领，黑长外套", file: "outfit-23.png" },
  { name: "燕麦毛衣，深橄榄裤", file: "outfit-24.png" },
  { name: "黑西装，白T恤", file: "outfit-25.png" },
  { name: "雾紫衬衫裙", file: "outfit-26.png" },
  { name: "深青针织，黑裙", file: "outfit-27.png" },
  { name: "卡其衬衫，炭灰马甲", file: "outfit-28.png" },
  { name: "银灰高领毛衣", file: "outfit-29.png" },
  { name: "墨蓝长风衣，白衬衫", file: "outfit-30.png" }
];

function outfitForDate(dateStr) {
  const parts = dateStr.split("-").map(Number);
  const days = Math.floor(Date.UTC(parts[0], parts[1] - 1, parts[2]) / 86400000);
  const index = ((days % OUTFITS.length) + OUTFITS.length) % OUTFITS.length;
  return { index, outfit: OUTFITS[index] };
}
