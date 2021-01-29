from urllib.parse import urljoin

if __name__ == "__main__":

    result = list(map(lambda x, y: x + y, [1, 3, 5, 7, 9], [2, 4, 6, 8, 10]))
    print(result)
    '''Output: [3, 7, 11, 15, 19] '''

    domain = [
        "https://google.com", "https://baidu.com", "https://youtube.com",
        "https://weibo.com"
    ]
    username = ["xiaoli", "xiaohong", "xiaowang", "xiaohuang"]
    user_url = list(map(lambda x, y: urljoin(x, y), domain, username))
    print(user_url)
    '''Output: ['https://google.com/xiaoli', 'https://baidu.com/xiaohong', 'https://youtube.com/xiaowang', 'https://weibo.com/xiaohuang'] '''