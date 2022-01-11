from abc import ABC, abstractstaticmethod
from typing import Dict, Union

from selenium.webdriver.common.by import By

class BaseItem(ABC):
    '''Базовый класс предмета, который мы ищем'''

    container_tag: str # Это тег контейнер на странице, котороый содержит искомые элементы
    item_tag: str # Это тег самого искомого элемента на странице

    @abstractstaticmethod
    def __init__(*args, **kwargs) -> Union[str, Dict[str, str], None]:
        '''Функция для обработки тега html в то, что нужно получить от данного элемента'''

class PostItem(BaseItem):
    '''Класс поста'''

    container_tag = 'wall_posts'
    item_tag = 'post_signed'

    def __init__(self, post, communities_url: str = '', *args, **kwargs) -> str:
        '''Парсит сообщество и находит в нем ссылку на себя'''
        self.url  = f"{communities_url}?w={post.get_attribute('id').replace('post', 'wall')}"

    def __repr__(self) -> str:

        return f'<Post: url={self.url}>'

class CommunityItem(BaseItem):
    '''Класс сообщества'''
    container_tag = 'search_communities_results'
    item_tag = 'groups_row'

    def __init__(self, community, *args, **kwargs) -> str:
        '''Пассит пост из сообщества и находит в нем ссылку на себя'''

        self.url = community.find_element(By.CLASS_NAME, 'title').find_element(By.TAG_NAME, 'a').get_attribute('href')

    def __repr__(self) -> str:

        return f'<Community: url={self.url}>'

class CommentItem(BaseItem):
    '''Класс комантария'''
    container_tag = 'wl_replies_block_wrap'
    item_tag = 'reply'

    def __init__(self, comment, *args, **kwargs):
        '''Парсит коментарий. На вход принимает элемент с классам reply
        '''

        post_id = comment.get_attribute('id')
        reply_post_id = 'post' + comment.get_attribute('onclick').split("'")[1]
        time = comment.find_element(By.CLASS_NAME, 'rel_date').text

        #Иногда коментарии могут быть удалеными, и тогда этих параметров не будет
        try:
            author = comment.find_element(By.CLASS_NAME, 'author').get_attribute('href')
        except:
            author = None
        try:
            text = comment.find_element(By.CLASS_NAME, 'reply_text').text
        except:
            text = None
        
        self.post_id = post_id
        self.reply_post_id = reply_post_id
        self.author = author
        self.text = text
        self.time = time
    
    def __repr__(self) -> str:
        return f'<Comment: post_id={self.post_id}, reply_id={self.reply_post_id}, author={self.author}, text={self.text}, time={self.time}>'
    