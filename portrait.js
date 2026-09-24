/* 原创角色沈晚。同一张脸，50 套衣服按日期轮换。胸更大，腰和腿保持细。 */
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
  { name: "墨蓝长风衣，白衬衫", file: "outfit-30.png" },
  { name: "黑色比基尼", file: "outfit-31.png" },
  { name: "白色比基尼", file: "outfit-32.png" },
  { name: "藏蓝连体泳衣", file: "outfit-33.png" },
  { name: "红色比基尼", file: "outfit-34.png" },
  { name: "黑色连体泳衣", file: "outfit-35.png" },
  { name: "碎花比基尼", file: "outfit-36.png" },
  { name: "墨绿比基尼", file: "outfit-37.png" },
  { name: "黑比基尼，白罩衫", file: "outfit-38.png" },
  { name: "条纹连体泳衣", file: "outfit-39.png" },
  { name: "雾蓝比基尼", file: "outfit-40.png" },
  { name: "黑吊带，牛仔短裤", file: "outfit-41.png" },
  { name: "黑色吊带裙", file: "outfit-42.png" },
  { name: "米色吊带，短裙", file: "outfit-43.png" },
  { name: "运动背心，黑短裤", file: "outfit-44.png" },
  { name: "奶油衬衫，黑裙", file: "outfit-45.png" },
  { name: "亚麻衬衫裙", file: "outfit-46.png" },
  { name: "黑背心，白短裤", file: "outfit-47.png" },
  { name: "灰上衣，黑打底裤", file: "outfit-48.png" },
  { name: "浅粉吊带裙", file: "outfit-49.png" },
  { name: "黑色挂脖裙", file: "outfit-50.png" }
];

function outfitForDate(dateStr) {
  if (dateStr === "2026-09-24") {
    return { index: 30, outfit: OUTFITS[30] };
  }
  const parts = dateStr.split("-").map(Number);
  const days = Math.floor(Date.UTC(parts[0], parts[1] - 1, parts[2]) / 86400000);
  const index = ((days % OUTFITS.length) + OUTFITS.length) % OUTFITS.length;
  return { index, outfit: OUTFITS[index] };
}
