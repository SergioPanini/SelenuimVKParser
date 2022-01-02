from abc import ABC, abstractstaticmethod
from typing import Dict, Union

from selenium.webdriver.common.by import By

class BaseItem(ABC):
    '''Базовый класс предмета, который мы ищем'''

    container_tag: str # Это тег контейнер на странице, котороый содержит эти элементы
    item_tag: str # Это тег самого элемента на странице

    @abstractstaticmethod
    def prepeare(*args, **kwargs) -> Union[str, Dict[str, str], None]:
        '''Функция для обработки тега html в то, что нужно получить от данного элемента'''

class PostItem(BaseItem):
    '''Класс поста'''

    container_tag = 'wall_posts'
    item_tag = 'post_signed'

    @staticmethod
    def prepeare(post, communities_url: str = '', *args, **kwargs) -> str:
        '''Парсит сообщество и находит в нем ссылку на себя'''
        return f"{communities_url}?w={post.get_attribute('id').replace('post', 'wall')}"


class CommunityItem(BaseItem):
    '''Класс сообщества'''
    container_tag = 'search_communities_results'
    item_tag = 'groups_row'

    @staticmethod
    def prepeare(community, *args, **kwargs) -> str:
        '''Пассит пост из сообщества и находит в нем ссылку на себя'''

        return community.find_element(By.CLASS_NAME, 'title').find_element(By.TAG_NAME, 'a').get_attribute('href')


class CommentItem(BaseItem):
    '''Класс комантария'''
    container_tag = 'wl_replies_block_wrap'
    item_tag = 'reply'

    @staticmethod
    def prepeare(comment, *args, **kwargs) -> Dict[str, str]:
        '''Парсит коментарий
            На вход принимает элемент с классам reply
        '''
        return {
                'reply_post_id':'post' + comment.get_attribute('onclick').split("'")[1],
                'author': comment.find_element(By.CLASS_NAME, 'author').get_attribute('href'),
                'text' : comment.find_element(By.CLASS_NAME, 'reply_text').text
            }
    