// ==UserScript==
// @name         天涯小助手
// @namespace    http://tampermonkey.net/
// @version      0.3.3
// @description  天涯帖子，默认只看楼主，展开所有评论，导出帖子等。
// @author       hugepower
// @include      ^http://bbs.tianya.cn/post-*.shtml$
// @include      http://bbs.tianya.cn/list-spirit-*
// @include      tianya.cn/*
// @grant        GM_xmlhttpRequest
// @grant        GM_download
// @updateURL    https://github.com/hugepower/UserScript/upload/master/UserScript/TianyaBBS.user.js
// ==/UserScript==

(function () {
    'use strict';


    function myFunction(registrationDate, userBirthday, userLocation, careerCategory, userCareer, userPost) {
        var div1;
        div1 = document.createElement('Div');
        div1.id = 'user-info';
        //div1.className = "atl-item";
        div1.style = "background-color: rgba(216, 80, 48, 0.3)!important;padding: 14px;border-left: 6px solid #ccc!important;border-color: rgba(216, 80, 48, 0.3)!important;margin-bottom:10px;margin-top:10px;color:firebrick;font-size:14px;border: 2px solid #8AC007;border-radius: 25px;";
        var list = document.getElementById("bd");
        list.insertBefore(div1, document.getElementsByClassName('atl-main')[0]);

        if (registrationDate != "") {
            var li_registrationDate;
            li_registrationDate = document.createElement('li');
            li_registrationDate.innerHTML = "注册日期：" + registrationDate;
            document.getElementById("user-info").appendChild(li_registrationDate);
        }

        if (userBirthday != "") {

            var li_user_bir;
            li_user_bir = document.createElement('li');
            li_user_bir.innerHTML = "出生日期：" + userBirthday;
            document.getElementById("user-info").appendChild(li_user_bir);
        }
        if (userLocation != "") {
            var li_userLocation;
            li_userLocation = document.createElement('li');
            li_userLocation.innerHTML = "用户位置：" + userLocation;
            document.getElementById("user-info").appendChild(li_userLocation);
        }
        if (careerCategory != "") {
            var li_careerCategory;
            li_careerCategory = document.createElement('li');
            li_careerCategory.innerHTML = "所属行业：" + careerCategory;
            document.getElementById("user-info").appendChild(li_careerCategory);
        }
        if (userCareer != "") {
            var li_userCareer;
            li_userCareer = document.createElement('li');
            li_userCareer.innerHTML = "所属职业：" + userCareer;
            document.getElementById("user-info").appendChild(li_userCareer);
        }
        var hr1 = document.createElement('hr');
        hr1.style = "background-color:firebrick;height:2px;border:none;";
        document.getElementById("user-info").appendChild(hr1);
    }

    function getUserTotalArticleList(userPageUrl) {
        var userId = userPageUrl.replace('http://www.tianya.cn/', '');
        var userJsonUrl = "http://www.tianya.cn/api/bbsuser?method=userinfo.ice.getUserTotalArticleList&params.pageSize=10&params.kindId=-1&params.userId=" + userId;
        GM_xmlhttpRequest({
            method: 'GET',
            url: userJsonUrl,
            headers: {
                'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3887.7 Safari/537.36',
                'contentType': 'application/json',
            },
            onload: function (responseDetails) {
                var el = JSON.parse(responseDetails.responseText);
                if (el.success == 1) {
                    for (var i = 0; i < el.data.rows.length; i++) {
                        var li1;
                        li1 = document.createElement('li');
                        li1.innerHTML = "发帖信息：" + el.data.rows[i].compose_time.replace('.0', '') + ' [' + el.data.rows[i].item_name + "]『" + el.data.rows[i].title + '』';
                        document.getElementById("user-info").appendChild(li1);

                    }
                    var hr1 = document.createElement('hr');
                    hr1.style = "background-color:lavenderblush;height:1px;border:none;";
                    document.getElementById("user-info").appendChild(hr1);
                }
                //return 0;
            }
        });
    }

    function getUserTotalReplyList(userPageUrl) {
        var userId = userPageUrl.replace('http://www.tianya.cn/', '');
        var userJsonUrl = "http://www.tianya.cn/api/bbsuser?method=userinfo.ice.getUserTotalReplyList&params.pageSize=10&params.kindId=-1&params.userId=" + userId;
        GM_xmlhttpRequest({
            method: 'GET',
            url: userJsonUrl,
            headers: {
                'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3887.7 Safari/537.36',
                'contentType': 'application/json',
            },
            onload: function (responseDetails) {
                var el = JSON.parse(responseDetails.responseText);
                if (el.success == 1) {
                    for (var i = 0; i < el.data.rows.length; i++) {
                        var li1;
                        li1 = document.createElement('li');
                        li1.innerHTML = "回帖信息：" + el.data.rows[i].reply_time.replace('.0', '') + ' [' + el.data.rows[i].item_name + "]『" + el.data.rows[i].title + '』';
                        document.getElementById("user-info").appendChild(li1);
                        if (el.data.rows[i].article_extend.hasOwnProperty("version")) {
                            var li2;
                            li2 = document.createElement('li');
                            li2.innerHTML = "设备版本：" + el.data.rows[i].reply_time.replace('.0', '') + ' ' + el.data.rows[i].article_extend.version;
                            document.getElementById("user-info").appendChild(li2);
                        }
                        if (el.data.rows[i].article_extend.hasOwnProperty("location")) {
                            var li_location;
                            li_location = document.createElement('li');
                            li_location.innerHTML = "当前位置：" + el.data.rows[i].reply_time.replace('.0', '') + ' ' + el.data.rows[i].article_extend.location;
                            document.getElementById("user-info").appendChild(li_location);
                        }
                    }
                    AddHTMLTagHr();
                }
                //return 0;
            }
        });
    }

    function AddHTMLTagHr() {
        var hr1 = document.createElement('hr');
        hr1.style = "background-color:lavenderblush;height:1px;border:none;";
        document.getElementById("user-info").appendChild(hr1);
    }

    function GetBHtml() {
        var userPageUrl = document.getElementsByClassName("atl-info")[0].getElementsByTagName('a')[0].href;
        GM_xmlhttpRequest({
            method: 'GET',
            url: userPageUrl,
            headers: {
                'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3887.7 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            },
            onload: function (responseDetails) {
                var el = document.createElement('html');
                el.innerHTML = responseDetails.responseText;
                var registrationDate = "";
                if (el.getElementsByClassName('userinfo')) {
                    for (var i = 0; i < el.getElementsByClassName('userinfo')[0].getElementsByTagName('span').length; i++) {
                        if (el.getElementsByClassName('userinfo')[0].getElementsByTagName('span')[i].innerText == "注册日期") {
                            registrationDate = el.getElementsByClassName('userinfo')[0].getElementsByTagName('span')[i].parentNode.innerText.replace('注册日期', '');
                        }
                    }
                }

                var user_bir = "";
                if (el.getElementsByClassName('user-bir').length == 1) {
                    user_bir = el.getElementsByClassName('user-bir')[0].parentNode.innerText;
                }

                var user_location = "";
                if (el.getElementsByClassName('user-location').length == 1) {
                    user_location = el.getElementsByClassName('user-location')[0].parentNode.innerText;
                }

                var career_category = "";
                if (el.getElementsByClassName('career-category').length == 1) {
                    career_category = el.getElementsByClassName('career-category')[0].parentNode.innerText.replace('行业', '').replace(/\s*/g, "");
                }

                var user_career = "";
                if (el.getElementsByClassName('user-career').length == 1) {
                    user_career = el.getElementsByClassName('user-career')[0].parentNode.innerText.replace('职业', '').replace(/\s*/g, "");
                }
                var female_offline_pngfix = "";
                if (el.getElementsByClassName('female-offline pngfix').length == 1) {
                    female_offline_pngfix = "女";
                } else {
                    female_offline_pngfix = "男";
                }
                myFunction(registrationDate, user_bir, user_location, career_category, user_career);
                getUserTotalArticleList(userPageUrl);
                getUserTotalReplyList(userPageUrl);
            }
        });
    }

    function addButton() {
        var exportButton1;
        exportButton1 = document.createElement('button');
        exportButton1.innerHTML = '导出帖子';
        exportButton1.id = "exportFile";
        exportButton1.style = "background-color: #f44336;border: none;color: white;text-align: center;text-decoration: none;display: inline-block;font-size: 14px;margin: 4px 2px;cursor: pointer;";
        setInterval(addExportButton, 200);

        function addExportButton() {
            if (document.getElementById("exportFile") === null) {
                document.getElementsByClassName("atl-info")[0].appendChild(exportButton1);
                document.querySelector('#exportFile').addEventListener('click', GetTieziInfoToTxt);
            }
        }
        var exportButton2;
        exportButton2 = document.createElement('button');
        exportButton2.innerHTML = '只看楼主';
        exportButton2.id = "VipRead";
        exportButton2.style = "background-color: #f44336;border: none;color: white;text-align: center;text-decoration: none;display: inline-block;font-size: 14px;margin: 4px 2px;cursor: pointer;";

        var exportButton3;
        exportButton3 = document.createElement('button');
        exportButton3.innerHTML = '复制名称';
        exportButton3.id = "CopyFileName";
        exportButton3.style = "background-color: #f44336;border: none;color: white;text-align: center;text-decoration: none;display: inline-block;font-size: 14px;margin: 4px 2px;cursor: pointer;";
        setInterval(addCopyFileName, 200);
        setInterval(addVipReadButton, 100);

        //添加按钮的函数
        function addVipReadButton() {
            if (document.getElementById("VipRead") === null) {
                document.getElementsByClassName("atl-info")[0].appendChild(exportButton2);
                document.querySelector('#VipRead').addEventListener('click', vipRead);
            }
        }

        //添加按钮的函数
        function addCopyFileName() {
            if (document.getElementById("CopyFileName") === null) {
                document.getElementsByClassName("atl-info")[0].appendChild(exportButton3);
                document.querySelector('#CopyFileName').addEventListener('click', CopyFileName);
            }
        }

        function CopyFileName() {
            var userNick = document.getElementsByClassName("atl-info")[0].getElementsByTagName('span')[0].innerText.replace('楼主：', '');
            var time = document.getElementsByClassName("atl-info")[0].getElementsByTagName('span')[1].innerText.replace(/时间：|-|:| /g, '');
            alert(userNick + "," + time + ",");
        }
    }
    //只看楼主
    function vipRead() {
        if (window.location.host.indexOf('bbs.tianya.cn') != -1) {
            var atlItem = document.getElementsByClassName('atl-item');
            for (var i = atlItem.length - 1; i >= 1; i--) {
                if (atlItem[i].getElementsByClassName('atl-info')[0].getElementsByTagName('span')[0].innerText.indexOf("作者：") > -1) {
                    if (atlItem[i].getElementsByClassName('item-reply-view').length > 0) {
                        // 获取每一条回复
                        var atlHeadReply = atlItem[i].getElementsByClassName('item-reply-view')[0].getElementsByTagName('li');
                        for (var j = atlHeadReply.length - 1; j >= 0; j--) {
                            // 如果评论区里的回复不是楼主回复，则删除回复
                            if (atlHeadReply[j].getElementsByTagName('a')[0].className != "ir-user ir-lz-user") {
                                atlHeadReply[j].parentNode.removeChild(atlHeadReply[j]);
                            }
                        }
                        if (atlHeadReply.length == 0) {
                            atlItem[i].parentNode.removeChild(atlItem[i]);
                        }
                    } else {
                        atlItem[i].parentNode.removeChild(atlItem[i]);
                    }
                } else {
                    if (atlItem[i].getElementsByClassName('item-reply-view').length > 0) {
                        // 获取每一条回复
                        atlHeadReply = atlItem[i].getElementsByClassName('item-reply-view')[0].getElementsByTagName('li');
                        for (j = atlHeadReply.length - 1; j >= 0; j--) {
                            //alert(atlHeadReply[j].getElementsByTagName('a')[0].className);
                            // 如果评论区里的回复不是楼主回复，则删除回复
                            if (atlHeadReply[j].getElementsByTagName('a')[0].className != "ir-user ir-lz-user") {
                                atlHeadReply[j].parentNode.removeChild(atlHeadReply[j]);
                            }
                        }
                    }
                }
            }
        }
    }

    // 根据classname删除指定内容
    function deleteDivClass() {
        var mycars = new Array("clearfix mt20 mb10",
            "action-tyf",
            "relevant-article mt10 clearfix",
            "shang-recommend",
            "atl-reply",
            "mb15 cf",
            "post-div",
            "bbs-float-menu", "ir-action", "a-link2 ir-reply"
        );
        for (var K = 0; K < mycars.length; K++) {
            var shangjin = document.getElementsByClassName(mycars[K]);
            if (shangjin) {
                for (var l = shangjin.length - 1; l >= 0; l--) {
                    shangjin[l].parentNode.removeChild(shangjin[l]);
                }
            }
        }
    }
    // 根据ID删除指定内容
    function deleteDivId() {
        var mycars = new Array("bbs_float_menu");
        for (var K = 0; K < mycars.length; K++) {
            var shangjin = document.getElementById(mycars[K]);
            try {
                if (shangjin.length > -1) {
                    for (var l = shangjin.length - 1; l >= 0; l--) {
                        shangjin[l].parentNode.removeChild(shangjin[l]);
                    }
                }
            } catch (err) {
                return
            }
        }
    }
    //删除空白行
    function DeleteBlankLines() {
        var Blanklines = document.getElementsByTagName("br");
        for (var K = Blanklines.length - 1; K >= 0; K--) {
            if (K % 2 > 1) {
                Blanklines[K].parentNode.removeChild(Blanklines[K]);
            }
        }
    }
    String.prototype.removeBlankLines = function () {
        return this.replace(/(\n[\s\t]*\r*\n)/g, '\n').replace(/^[\n\r\n\t]*|[\n\r\n\t]*$/g, '')
    }

    //展开所有评论
    function ExpandAllcomment() {
        var x = document.getElementsByClassName("a-link2 ir-showreply");
        for (var i = 0; i < x.length; i++) {
            x[i].click();
        }
    }

    function GetTieziInfo() {
        //var inValue = "用户名,发帖时间,帖子标题,帖子地址,帖子内容\n";
        var title = document.getElementsByClassName("s_title")[0].innerText;
        var url = window.location.href;
        var inValue = "【" + title + "】," + url + "\n";
        for (var i = 0; i < document.getElementsByClassName("atl-info").length; i++) {
            try {
                var regexUser = /(?<=楼主：)(.+?)(?= 时间)/;
                var matchUser = regexUser.exec(document.getElementsByClassName("atl-info")[i].innerText);
                var user = matchUser[0];
                var time = document.getElementsByClassName("atl-info")[0].getElementsByTagName('span')[1].innerText.replace('时间：').replace(' ', '').replace(':', "");
                var bbscontent = document.getElementsByClassName("bbs-content")[i].innerText;
                //inValue += user + "\n" + time + "\n" + title + "\n" + url + "" +bbscontent+"\n";
                inValue += user + "," + url + "\n" + bbscontent + "\n\n";
            } catch (err) {
                //alert(err)
            }
        }
        //saveAsCsv(inValue)
        saveAsTxt(inValue)
    }

    function GetTieziInfoToTxt() {
        var title = document.getElementsByClassName("s_title")[0].innerText;
        var regexUserNick = /(?<=楼主：)(.+?)(?= 时间)/;
        var matchUserNick = regexUserNick.exec(document.getElementsByClassName("atl-info")[0].innerText);
        var userNick = matchUserNick[0];
        var url = window.location.href;
        var inValue = "# " + title + "\n" + url + "\n";
        for (var i = 0; i < document.getElementsByClassName("atl-item").length; i++) {
            //try{
            var user = document.getElementsByClassName("atl-info")[i].innerText.replace(/只看楼主导出帖子复制名称/, '');
            var bbscontent = document.getElementsByClassName("atl-content")[i].getElementsByClassName('bbs-content')[0].innerText;
            var bbscontent_reply = "";
            if (document.getElementsByClassName("atl-content")[i].getElementsByClassName('item-reply-view').length > 0) {
                var bbscontent_reply_li = document.getElementsByClassName("atl-content")[i].getElementsByClassName('item-reply-view')[0].getElementsByTagName('li');
                for (var k = 0; k < bbscontent_reply_li.length; k++) {
                    var bbscontent_reply_username = "";
                    var bbscontent_reply_replytime = bbscontent_reply_li[k].getAttribute('_replytime')
                    var bbscontent_reply_content = bbscontent_reply_li[k].getElementsByClassName('ir-content')[0].innerText;
                    // 作者
                    if (bbscontent_reply_li[k].getElementsByTagName('a')[0].className == "ir-user") {
                        bbscontent_reply_username = bbscontent_reply_li[k].getAttribute('_username')
                        bbscontent_reply += '>`作者：' + bbscontent_reply_username + '` ' + bbscontent_reply_replytime + ' ' + bbscontent_reply_content + '\n';
                    } else if (bbscontent_reply_li[k].getElementsByTagName('a')[0].className == "ir-user ir-lz-user") {
                        bbscontent_reply_username = bbscontent_reply_li[k].getAttribute('_username')
                        bbscontent_reply += '>`楼主：' + bbscontent_reply_username + '` ' + bbscontent_reply_replytime + ' ' + bbscontent_reply_content + '\n';
                    }
                }
            }
            var regexUser = /(?<=楼主：)|(?<=作者：)(.+?)(?= 时间)/;
            var matchUser = regexUser.exec(document.getElementsByClassName("atl-info")[i].innerText);
            var alt_info_user = matchUser[0];
            //replace(/时间：|-|:| /g,'')，意思把字符串中包含【时间：】【-】【:】【 】字符的通通替换为空。-g表示全局替换，|表示条件或。
            var time = document.getElementsByClassName("atl-info")[0].getElementsByTagName('span')[1].innerText.replace(/时间：|-|:| /g, '');
            if (document.getElementsByClassName("atl-content")[i].getElementsByTagName('img')) {
                var imgList = document.getElementsByClassName("atl-content")[i].getElementsByTagName('img');
                for (var j = 0; j < imgList.length; j++) {
                    bbscontent += "\n![" + time + "](" + imgList[j].src + ")";
                }
            }
            inValue += user + "\n" + bbscontent + "\n" + bbscontent_reply + "\n\n";
            inValue += "-------\n\n";

        }
        inValue += '>' + document.getElementById('user-info').innerText;
        var filename = userNick + "," + time + "," + title;
        saveAsTxt(inValue, filename)
    }


    function saveAsTxt(inValue, filename) {
        var uri = 'data:text/csv;charset=utf-8,\ufeff' + encodeURIComponent(inValue);
        var link = document.createElement("a");
        link.href = uri;
        link.download = filename + ".md";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    //保存到 csv 中
    function saveAsCsv(inValue) {
        var uri = 'data:text/csv;charset=utf-8,\ufeff' + encodeURIComponent(inValue);
        var link = document.createElement("a");
        link.href = uri;
        link.download = "天涯帖子信息.csv";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    function registrationDate(userUrl) {
        GM_xmlhttpRequest({
            method: 'GET',
            url: userUrl,
            headers: {
                'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3887.7 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            },
            onload: function (responseDetails) {
                var el = document.createElement('html');
                el.innerHTML = responseDetails.responseText;
                var registrationDate = "";
                if (!el.getElementsByClassName('userinfo')) {
                    for (var i = 0; i < el.getElementsByClassName('userinfo')[0].getElementsByTagName('span').length; i++) {
                        if (el.getElementsByClassName('userinfo')[0].getElementsByTagName('span')[i].innerText == "注册日期") {
                            registrationDate = el.getElementsByClassName('userinfo')[0].getElementsByTagName('span')[i].parentNode.innerText.replace('注册日期', '');
                            return registrationDate;
                            break;
                        }
                    }
                }
            }
        });
    }
    window.onload = function () {
        if (document.URL.indexOf('shtml#') == -1) {
            if (document.getElementsByClassName('wd-answer').length == 0) {
                deleteDivId()
                addButton()
                ExpandAllcomment()
                deleteDivClass()
                DeleteBlankLines()
                vipRead()
                GetBHtml()
                var regexUser = /(?<=楼主：)(.+?)(?= 时间)/;
                var matchUser = regexUser.exec(document.getElementsByClassName("atl-info")[0].innerText);
                var user = matchUser[0];
                var new_title = user + ',' + document.getElementsByClassName("atl-info")[0].getElementsByTagName('span')[1].innerText.replace(/时间：|-|:| /g, '') + ',' + document.getElementsByTagName("title")[0].innerText;
                document.getElementsByTagName("title")[0].innerText = new_title;
            }
        }
    }
    //禁用原因，因频繁访问主页，被天涯限制访问。
    /*     if(document.URL.indexOf('bbs.tianya.cn/list-spirit')!=-1)
        {
            var num = document.getElementsByClassName('author').length;
            for(var i=0;i<2;i++)
            {
                var date = registrationDate(document.getElementsByClassName('author')[i].href)
                console.log(document.getElementsByClassName('author')[i].href);
                //var userId = document.getElementsByClassName('author')[i].href.replace('http://www.tianya.cn/','');
                document.getElementsByClassName('author')[i].innerText = document.getElementsByClassName('author')[i].innerText + '[' + date + ']';
            }
        } */
})();