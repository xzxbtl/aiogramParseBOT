from bs4 import BeautifulSoup as Bs
import httpx
from aiogrambot.base.TakeInfoBase import TakeInfo
from aiogrambot.logs import logger


class Parse:
    """Парсит названия, просмотры, ссылки, описания"""

    def __init__(self, link: str, count: int, user_id: int):
        self.link = link
        self.count = count
        self.user_id = user_id

    async def response_database(self):
        request = httpx.get(f"{self.link}")
        try:
            if request.status_code == 200:
                soup = Bs(request.text, "html.parser")
                titles = soup.select(".wdp-card-description-module__title")
                reviews = soup.select(".wdp-card-description-meta-info-module__metaInfoViewsCountNumber")
                links = soup.find_all("a", class_="wdp-link-module__link wdp-card-poster-module__posterWrapper")
                authors = soup.find_all("a",
                                        class_="wdp-link-module__link wdp-card-description-module__author "
                                               "wdp-card-description-module__url")

                for title, review, link, author in list(zip(titles, reviews, links, authors))[:self.count]:
                    request_desc = httpx.get("https://rutube.ru" + link.get("href"))
                    soup_desc = Bs(request_desc.text, "html.parser")
                    if request_desc is not None:
                        desc_element = soup_desc.select_one(".freyja_pen-videopage-description__description_x8Lqk")
                        if desc_element is not None:
                            desc_text = desc_element.get_text(strip=True)[:100] + "..."
                        else:
                            desc_text = "Не найдено"
                    else:
                        desc_text = "Ошибка в теге"
                    await TakeInfo.insert_video_parse_info(self.user_id, title.text, review.text,
                                                           "https://rutube.ru" + link.get("href"),
                                                           desc_text, author.text)
            elif request.status_code == 301:
                new_url = request.headers['Location']
                await logger.info(f"Адрес не совпадает с имеющимся на запросе, возможный адрес - {new_url}")

        except Exception as err:
            await logger.info(f"Ошибка при получении ссылки {err}")
