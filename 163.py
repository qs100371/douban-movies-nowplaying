import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime

def crawl_163_news():
    # 请求网易新闻首页
    url = "https://news.163.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        # 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有符合条件的div
        news_divs = soup.find_all('div', class_='hidden', attrs={'ne-if': '{{__i == 0}}'})
        
        news_list = []
        
        for div in news_divs:
            # 在div中查找新闻标题和链接
            links = div.find_all('a')
            for link in links:
                title = link.get_text(strip=True)
                href = link.get('href')
                if title and href:
                    news_list.append({'title': title, 'url': href})
        
        return news_list
        
    except Exception as e:
        print(f"爬取过程中出现错误: {e}")
        return []

def generate_html(news_list):
    # 获取当前时间
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 生成HTML文件
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>网易新闻抓取结果</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #d00;
                text-align: center;
                border-bottom: 1px solid #eee;
                padding-bottom: 10px;
            }
            .news-item {
                padding: 10px 0;
                border-bottom: 1px dashed #eee;
            }
            .news-item a {
                color: #333;
                text-decoration: none;
            }
            .news-item a:hover {
                color: #d00;
                text-decoration: underline;
            }
            .footer {
                margin-top: 20px;
                padding-top: 10px;
                border-top: 1px solid #eee;
                text-align: center;
                color: #666;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>网易新闻</h1>
    """
    
    for news in news_list:
        html_content += f"""
            <div class="news-item">
                <a href="{news['url']}" target="_blank">{news['title']}</a>
            </div>
        """
    
    html_content += f"""
            <div class="footer">
                新闻来源：网易 | 抓取时间：{current_time}| 共 {len(news_list)} 条
            </div>
        </div>
    </body>
    </html>
    """
    
    # 保存HTML文件
    os.makedirs('docs', exist_ok=True)
    with open('docs/163_news.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML文件已生成: 163_news.html (抓取时间: {current_time}，共 {len(news_list)} 条)")

if __name__ == "__main__":
    news = crawl_163_news()
    if news:
        generate_html(news)
    else:
        print("没有获取到新闻数据")