// ==UserScript==
// @name         百度新闻高亮百家号的链接
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  百度新闻高亮百家号的链接
// @author       hugepower
// @include      http://news.baidu.com/*
// ==/UserScript==
(function () {
    'use strict';
    window.onload = function () {
        setInterval(baijiahao, 2000);
    }
    function baijiahao(){
        var elements = document.querySelectorAll("a");
        elements.forEach(function (element) {
            if (element.href.indexOf("baijiahao.baidu.com") >= 0) {
                // 高亮
                element.style.backgroundColor = "#FFE4B5";
                // 移除
                //element.parentNode.removeChild(element)
            }
        })
    }
})();