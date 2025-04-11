import os
import pytz
import requests
from bs4 import BeautifulSoup
import json

def get_douban_hot_movies():
    """
    从豆瓣获取当前热映电影信息
    """
    url = "https://movie.douban.com/cinema/nowplaying/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 豆瓣热映电影信息通常在一个id为"nowplaying"的div中
        nowplaying_div = soup.find('div', id='nowplaying')
        if not nowplaying_div:
            return []
            
        movies = []
        for li in nowplaying_div.find_all('li', class_='list-item'):
            movie = {}
            movie['id'] = li.get('id', '').strip()
            movie['title'] = li.get('data-title', '').strip()
            movie['score'] = li.get('data-score', '').strip()
            movie['duration'] = li.get('data-duration', '').strip()
            movie['region'] = li.get('data-region', '').strip()
            movie['director'] = li.get('data-director', '').strip()
            movie['actors'] = li.get('data-actors', '').strip()
            movie['poster'] = li.find('img').get('src') if li.find('img') else ''
            
            # 获取星级评分（如果有）
            star_rating = li.find('span', class_='subject-rate')
            if star_rating:
                movie['star_rating'] = star_rating.get_text().strip()
            else:
                movie['star_rating'] = '暂无评分'
                
            movies.append(movie)
            
        return movies
        
    except Exception as e:
        print(f"获取豆瓣热映电影失败: {e}")
        return []

def generate_star_rating(score):
    """生成星级评分"""
    try:
        score = float(score)
        full_stars = int(score // 2)
        half_star = 1 if score % 2 >= 1 else 0
        empty_stars = 5 - full_stars - half_star
        return '⭐' * full_stars + '½' * half_star + '☆' * empty_stars
    except:
        return ''

def generate_html(movies):
    """
    生成展示热映电影的HTML页面
    """
    html_template = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="referrer" content="no-referrer">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
       	<meta name="description" content="It&#39;s just a note, not a guide." />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
	<meta name="baidu-site-verification" content="codeva-LhXgKgQNnq" />
	<meta name="keywords" content="linux onecloud armbian docker 学习笔记 个人博客">
	<title>豆瓣热映电影 | The blog of qs</title>
	<link rel="shortcut icon" href="https://qs100371.vip/favicon.ico">

	<link rel="stylesheet" href="https://qs100371.vip/styles/main.css">
	<script defer src="https://cloud.umami.is/script.js" data-website-id="6e0a4c7e-ee80-4e33-aca1-db6b188445b7"></script>
	<script src="/media/scripts/Valine.min.js" ></script>
        <style>
            body {{
                font-family: 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            h1 {{
                text-align: center;
                color: #007722;
                margin-bottom: 30px;
            }}
            a {{
                color: #007722;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .movie-container {{
                display: flex;
                flex-wrap: wrap;
                justify-content: space-around;
                gap: 20px;
            }}
            .movie-card {{
                width: 220px;
                background: white;
                border-radius: 5px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s;
            }}
            .movie-card:hover {{
                transform: translateY(-5px);
            }}
            .movie-poster {{
                width: 100%;
                height: 300px;
                object-fit: cover;
            }}
            .movie-info {{
                padding: 15px;
            }}
            .movie-title {{
                font-weight: bold;
                font-size: 16px;
                margin-bottom: 5px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            .movie-meta {{
                font-size: 13px;
                color: #666;
                margin-bottom: 3px;
            }}
            .movie-rating {{
                color: #e09015;
                font-weight: bold;
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                color: #999;
                font-size: 14px;
            }}
            @media (max-width: 768px) {{
                .movie-card {{
                    width: 45%;
                }}
            }}
            @media (max-width: 480px) {{
                .movie-card {{
                    width: 100%;
                }}
            }}
        </style>
    </head>
    <body class="is-preload">
    <!-- Wrapper -->
			<div id="wrapper">
      <!-- Header -->
<header id="header">
  <div class="inner">
    <!-- Logo -->
    <a href="https://qs100371.vip" class="logo">
      <span class="symbol"
        ><img
          src="https://qs100371.vip/images/avatar.png"
          alt=""
        />
      </span>
      <div class="site-title"> The blog of qs </div>
    </a>

    <!-- Nav -->
    <nav>
      <ul>
        <li><a href="#menu">Menu</a></li>
      </ul>
    </nav>
  </div>
</header>

<!-- Menu -->
<nav id="menu">
  <ul>
    
    
      <li><a href="/" class="menu">
        首页
      </a></li>
      
    
    
      <li><a href="/archives" class="menu">
        归档
      </a></li>
      
    
    
      <li><a href="/tags" class="menu">
        标签
      </a></li>
      
    
    
      <li><a href="https://t.qs100371.vip" class="menu" target="_blank">
        笔记
      </a></li>
    
    
    
      <li><a href="https://m.qs100371.vip/u/guest" class="menu" target="_blank">
        日常
      </a></li>
    
    
    
      <li><a href="https://w.qs100371.vip" class="menu">
        文字版
      </a></li>
      
    
    <li>
    <form id="gridea-search-form" action="https://qs100371.vip/search/">
      <input name="q" placeholder="搜索文章" />
    </form></li>
  </ul>
</nav>
<div id="main">
						<div class="inner">
             <h2 class="tags-title">
                🎬 豆瓣热映电影
              </h2>
              <div class="tags-container">
               
        <div class="movie-container">
            {movies_html}
        </div>
        <div class="footer">
            数据来源: 豆瓣电影 | 更新时间: {update_time}
        </div>  
                  
                
              </div>
    
            </div>
					</div>

        <!-- Footer -->
<footer id="footer">
  <div class="inner">
    
    <ul class="copyright">
     
      ©2025   <a href="mailto:admin@qs100371.vip">qs100371.vip</a>
      
    </ul>
  </div>
</footer>
			</div>

		<!-- Scripts -->
			<script src="https://qs100371.vip/media/scripts/jquery.min.js"></script>
			<script src="https://qs100371.vip/media/scripts/browser.min.js"></script>
			<script src="https://qs100371.vip/media/scripts/breakpoints.min.js"></script>
			<script src="https://qs100371.vip/media/scripts/util.js"></script>
			<script src="https://qs100371.vip/media/scripts/main.js"></script>

      </div>
    </div>
  </body>
</html>
    """
    
    from datetime import datetime
    
    update_time = get_beijing_time()
    movies_html = ""
    for movie in movies:
        movie_html = f"""
        <div class="movie-card">
            <img class="movie-poster" src="{movie.get('poster', '')}" alt="{movie.get('title', '')}">
            <div class="movie-info">
                 <div class="movie-title">
                    <a href="https://movie.douban.com/subject/{movie.get('id', '')}/" target="_blank">
                        {movie.get('title', '')}
                    </a>
                </div>
                <div class="movie-meta">导演: {movie.get('director', '未知')}</div>
                <div class="movie-meta">主演: {movie.get('actors', '未知')}</div>
                <div class="movie-meta">地区: {movie.get('region', '未知')}</div>
                <div class="movie-meta">片长: {movie.get('duration', '未知')}</div>
                <div class="movie-rating">评分: {movie.get('score', movie.get('star_rating', '暂无评分'))}
                    {generate_star_rating(movie.get('score', 0))}
                </div>
            </div>
        </div>
        """
        movies_html += movie_html
    
    full_html = html_template.format(movies_html=movies_html, update_time=update_time)
    return full_html




from datetime import datetime

def save_html(html_content, filename="docs/index.html"):
    os.makedirs("docs", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

def get_beijing_time():
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')



if __name__ == "__main__":
    print("正在获取豆瓣热映电影信息...")
    movies = get_douban_hot_movies()
    
    if movies:
        print(f"获取到 {len(movies)} 部热映电影")
        html_content = generate_html(movies)
        save_html(html_content)
    else:
        print("未能获取热映电影信息")
