'''
Парсер постов с 3dnews.ru
'''

from bs4 import BeautifulSoup
import requests


html = '''
<div class="article-entry article-infeed marker_allfeed nImp0 nIcat9 cat_9 nIaft " id="1069432" data-count="1" data-type="0" data-rtype="0" data-cat="9" data-important="0" style="display:block">
	<div class="imgPrevWrapper">
	        <a href="https://3dnews.ru/1069432/fitnesbraslet-xiaomi-mi-band-7-pro-osnashchyon-priyomnikom-gps-i-pulsoksimetrom">
	        	<div class="imgPrevAsBG" style="background: url(/assets/external/illustrations/2022/07/04/1069432/band1.jpg);">
	            	<img itemprop="image" class="imageInAllFeed" src="./Технологии и рынок IT. Новости , страница 1_files/band1.jpg" style="visibility: hidden;">
	        	</div>
	        </a>
	</div>
	<div class="cntPrevWrapper">
	        <div class="metaInfoWrapper"><span class="entry-date">04.07.2022 16:38 </span></div>
	        <a name="1069432"></a><a class="entry-header" href="https://3dnews.ru/1069432/fitnesbraslet-xiaomi-mi-band-7-pro-osnashchyon-priyomnikom-gps-i-pulsoksimetrom"><h1>Xiaomi представила Mi Band 7 Pro — фитнес-браслет с большим экраном, GPS и ценой $60 </h1></a>
	        <p>Китайская компания Xiaomi официально анонсировала трекер физической активности Mi Band 7 Pro. Устройство представляет собой нечто среднее между классическим фитнес-браслетом и смарт-часами.</p> 	
	</div>
	<script>window.yaParams.push( { "statByPubLoad": { "[1069432] Xiaomi представила Mi Band 7 Pro — фитнес-браслет с большим экраном, GPS и ценой $60": { "in-feed": 1 } } } );</script>
</div>

<div class="article-entry article-infeed marker_allfeed nImp0 nIcat9 cat_9 nIaft " id="1069431" data-count="2" data-type="2" data-rtype="0" data-cat="9" data-important="1" style="display:block">
	<div class="imgPrevWrapper">
	        <a href="https://3dnews.ru/1069431/debyutiroval-smartfon-xiaomi-12s-ultra-s-kameroy-leica-na-osnove-1dyuymovogo-sensora">
	        	<div class="imgPrevAsBG" style="background: url(/assets/external/illustrations/2022/07/04/1069431/ultra1.jpg);">
	            	<img itemprop="image" class="imageInAllFeed" src="./Технологии и рынок IT. Новости , страница 1_files/ultra1.jpg" style="visibility: hidden;">
	        	</div>
	        </a>
	</div>
	<div class="cntPrevWrapper">
	        <div class="metaInfoWrapper"><span class="entry-date">04.07.2022 16:26 </span></div>
	        <a name="1069431"></a><a class="entry-header" href="https://3dnews.ru/1069431/debyutiroval-smartfon-xiaomi-12s-ultra-s-kameroy-leica-na-osnove-1dyuymovogo-sensora"><h1>Представлен Xiaomi 12S Ultra — флагман за $900 с камерой Leica на огромном 1-дюймовом сенсоре </h1></a>
	        <p>Официально представлен флагманский смартфон Xiaomi 12S Ultra, при разработке которого особое внимание было уделено возможностям фото- и видеосъёмки. Устройство получило мощную систему камер, разработанную в сотрудничестве со специалистами Leica.</p> 	
	</div>
	<script>window.yaParams.push( { "statByPubLoad": { "[1069431] Представлен Xiaomi 12S Ultra — флагман за $900 с камерой Leica на огромном 1-дюймовом сенсоре": { "in-feed": 1 } } } );</script>
</div>
'''


def parse_posts(raw_text: str) -> dict:
    """Парсим посты с 3dnews.ru
    arg: html as str
    return -> dict[post_number]: (post_text, post_href, post_img)
    """
    try:
        data = BeautifulSoup(raw_text, features='html.parser')
        posts = data.find_all('div', class_='article-entry')
        all_posts = {}
        for post in posts:
            post_number = int(post.get('id'))
            post_text = post.find('a', class_='entry-header')
            post_href = post_text.get("href")
            if post_href[:5] != 'https':
                post_href = f'https://3dnews.ru{post_href}'
            # post_img = post.find('img', class_='imageInAllFeed').get('src')
            # post_img = f'https://3dnews.ru{post_img}'
            all_posts[post_number] = (
                post_text.text,
                post_href,
                # post_img
            )
        return all_posts

    except Exception as e:
        raise Exception(
            f'Не удалось распарсить посты: {e}')


if __name__ == "__main__":
	url = 'https://3dnews.ru/news/'
	response = requests.get(url).text
	print(parse_posts(response))

	# print(parse_posts(html))