from typing import List, Optional, Dict
import time
import datetime

from webdriver_manager.firefox import GeckoDriverManager
from base import BaseItem, CommentItem, CommunityItem, PostItem


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class BrowserManager():
    '''Класс браузера'''
    
    def __init__(self) -> None:
        self.broswer = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    

    def get_communities(self, search_text: str, limit: int = None) -> Optional[List[str]]:
        '''Находит ссылки на сообщества связаные по ключевому слову search_text'''

        #Загружаем страницу
        url = f'https://vk.com/search?c[q]={search_text}&c[section]=communities&c[type]=4'
        self.broswer.get(url)
        time.sleep(5)
        
        #Пробуем найти контейнер наших элементов - сообществ
        try:
            search_auto_rows_item = self.broswer.find_element_by_class_name("search_communities_results")
        except NoSuchElementException:
            return None

        self._load_all_items(search_auto_rows_item, (By.CLASS_NAME, "groups_row"), limit=limit)
        
        #Собираем ссылки на сообщества
        urls = []
        for item in search_auto_rows_item.find_elements(By.CLASS_NAME, "groups_row"):
            urls.append(self._prepere_community_to_url(item))
        
        return urls
    
    def _load_all_items(self, item_container, args_find: dict, limit: int = None):
        '''Листает страницу, пока все элементы которые мы ищем не загрузятся
            input:
                item_container - элемент верстки, который содержит загружаемые элементы, контейнер для них.
                args_find - аргументы, по которым искать элементы в контейнере.
        '''

        group_rows_count = len(item_container.find_elements(*args_find))
        
        while True:
            # Листаем, пока кол-во сообществ не перестанет расти
            self.broswer.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            group_rows_count_new = len(item_container.find_elements(*args_find))
            print(f"Load items: {group_rows_count_new}")
            if group_rows_count_new == group_rows_count:
                break
            if limit and group_rows_count_new > limit:
                break

            group_rows_count = group_rows_count_new
    
    def get_posts(self, url_communiti: str, limit: int = None) -> List[str]:
        '''Загружаем посты сообщества'''

        self.broswer.get(url_communiti)
        try:
            posts_container = self.broswer.find_element_by_id('page_wall_posts')
        except NoSuchElementException:
            return None
        
        self._load_all_items(posts_container, (By.CLASS_NAME, 'post_signed'), limit)

        posts = posts_container.find_elements(By.CLASS_NAME, 'post_signed')

        posts_url = []
        for post in posts:
            posts_url.append(self._prepere_post_to_url(post))
        
        return posts_url
    
    def get_comments(self, post_url: str) -> Optional[Dict[str, str]]:
        '''Находит коментарии к посту
            input: post_url - ссылка на пост
            output: Словарь с информацией о комантариях:
            {   'id post': {
                           'author url':'Ссылка на автора',
                           'reply_post_id': 'ссылка на пост на который был дан ответ',
                           'text' : 'Текст сообщения'
                        },
                'post-88245281_8026409': {
                           'author': 'https://vk.com/arabov1990',
                           'reply_post_id': 'post-88245281_8026263',
                           'text': 'Я помню что это было!'
                        },
                'post-88245281_8026415': {
                           'author': 'https://vk.com/gidroksimetil_hinoksilin_dioksid',
                           'reply_post_id': 'post-88245281_8026263',
                           'text': 'вк к лайкам обратно вернулись'
                        }
            }
        '''

        self.broswer.get(post_url)
        time.sleep(3)
        try:
            posts_countainer = self.broswer.find_element_by_class_name('wl_replies_block_wrap')
        except NoSuchElementException:
            return None

        if not posts_countainer:
            return None

        self._load_all_items(posts_countainer, (By.CLASS_NAME, 'reply'))

        replys = {i.get_attribute('id'): self.parse_comment(i) 
                         for i in posts_countainer.find_elements(By.CLASS_NAME, 'reply')
        }

        return replys
    
    @staticmethod
    def parse_comment(comment) -> Dict[str, str]:
        '''Парсит коментарий
            На вход принимает элемент с классам reply
        '''
        print('reply: ', comment.get_attribute('onclick').split("'")[1])
        return {
                'reply_post_id':'post' + comment.get_attribute('onclick').split("'")[1],
                'author': comment.find_element(By.CLASS_NAME, 'author').get_attribute('href'),
                'text' : comment.find_element(By.CLASS_NAME, 'reply_text').text
            }
    
    @staticmethod
    def _prepere_community_to_url(item):
        '''Парсит сообщество и находит в нем ссылку на себя'''
        item.find_element(By.CLASS_NAME, 'title').find_element(By.TAG_NAME, 'a').get_attribute('href')

    @staticmethod
    def _prepere_post_to_url(post, url_communiti: str) -> str:
        '''Пассит пост из сообщества и находит в нем ссылку на себя'''
        return f"{url_communiti}?w={post.get_attribute('id').replace('post', 'wall')}"


class CustomBrowserManager:
    '''Класс браузера'''

    def __init__(self) -> None:
        self.broswer = webdriver.Firefox()

    def load_items(self, item_container, args_find: dict, limit: int = None):
        '''Генератор для получаения элементов с загрузкой их по Ajax'''

        items = item_container.find_elements(*args_find)
        group_rows_count = len(items)
        group_rows_count_new = None
        N = -1
        while True:

            N += 1

            if limit and N >= limit:
                break
            #Если номер элемента для отдачи больше, чем сейчас загружено, то загружаем еще элементы
            if N >= group_rows_count:
                self.broswer.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)

                #Проверяем что мы загрузили новые элементы, иначе элементы закончились и мы заканчиваем работу
                new_items = item_container.find_elements(*args_find)
                group_rows_count_new = len(new_items)
                if group_rows_count_new == group_rows_count:
                    break
            
                group_rows_count = group_rows_count_new
                items = new_items
                yield new_items[N]

            else:
                yield items[N]

    def _generator(self, item: BaseItem, url: str, limit: int = None):
        '''Базовая логика генератора для получаения элемента'''

        #Создаем новую вкладку, запоминаем и переключается на ее 
        self.broswer.execute_script(f"window.open('', '{url}');")
        generator_handler = self.broswer.window_handles[-1]
        self.broswer.switch_to.window(generator_handler)

        #Загружаем страницу
        self.broswer.get(url)
        time.sleep(5)

        #Находим контейнер постов
        try:
            posts_container = self.broswer.find_element_by_class_name(item.container_tag)
        except NoSuchElementException:
            return None
        

        #Создаем генератор для получения обьектов, в нашем случаем постов
        post_generator = self.load_items(posts_container, (By.CLASS_NAME, item.item_tag), limit)
        while True:

            try:
                self.broswer.switch_to.window(generator_handler)
                new_item = next(post_generator)
            except StopIteration:
                break

            yield item.prepeare(new_item, url)
        
        self.broswer.close()
    
    def communities(self, search_tetx: str, limit: int = None) -> str:
        '''Генератор, который возвращяет ссылки на сообщества'''

        url = f'https://vk.com/search?c[q]={search_tetx}&c[section]=communities&c[type]=4'
        return self._generator(CommunityItem, url, limit)
    
    def posts(self, community_url: str, limit: int = None) -> str:
        '''Генератор, который возвращяет ссылки на посты из сообщества'''

        return self._generator(PostItem, community_url, limit)
    
    def comments(self, post_url: str, limit: int = None):
        '''Генератор, который возвращяет коментарии как словари'''

        return self._generator(CommentItem, post_url, limit)
