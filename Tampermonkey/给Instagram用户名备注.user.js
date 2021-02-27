// ==UserScript==
// @name         给Instagram用户名备注
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  备注用户名
// @author       hugepower
// @match        https://www.instagram.com/*
// @grant        none
// ==/UserScript==

(function () {
    'use strict';
    window.onload = function () {
        setInterval(showRemarkName, 2000);

        function showRemarkName() {

            var userList = {
                "chenchiyiu":"陳自瑤yoyo",
                "anchor_carolyn":"新聞主播 陳海茵",
                "nameibaby":"中泰混血兒",
                "xiexin1127":"主持人",
                "lingyu10311031":"三立新聞台主播張齡予",
                "vivnews":"寰宇新聞主播",
                "yanhibi0221": "大槻ひびき、大槻响",
                "mabel_goo": "亚航空姐",
                "taewaew_natapohn": "娜塔玻·提米露克、道妹",
                "tranggphamm2402": "越南河内",
                "epoint2016": "相沢みなみ、相泽南",
                "lingyu10311031": "台湾张龄予主播",
                "clio1008": "卡塔尔航空空姐、尖如",
                "elizabetholsenofficial": "伊丽莎白·奥尔森、绯红女巫",
                "vivian19941008": "台湾网络红人谢薇安",
                "salen_wu": "长荣空姐Salen",
                "alephant_0427": "台湾女主播林妤臻",
                "kana_momonogi": "桃乃木かな、桃乃木香奈",
                "kana_momonogi": "小島みなみ、小岛南",
                "ai_uehara_ex": "上原亚衣",
                "hatsukaw_aminami": "初川みなみ、初川南",
                "yoko_mitsuya": "三津谷葉子",
                "amami_tsubasa000": "天海つばさ、天海翼",
                "yua_mikami": "三上悠亜",
                "aikayamagishi": "山岸逢花"
            };

            var items = document.querySelectorAll('a[class="sqdOP yWX7d     _8A5w5   ZIAjV "]');
            items.forEach(function (item) {
                if (userList[item.innerText]) {
                    item.innerText = item.innerText + "(" + userList[item.innerText] + ")";
                }
            });
        }
    }
})();