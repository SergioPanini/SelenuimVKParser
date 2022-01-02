import argparse
from driver import BrowserManager

parser = argparse.ArgumentParser()
parser.add_argument('--no-window', default=False, dest='no_window', help='Запускать selenuim в терминале.')
parser.add_argument('--web-driver-path', default=None, dest="web_driver_path", help='Путь к веб драйверу')
args = parser.parse_args()

print(
    '''
$$$$$$$\                     $$\           $$\        $$$$$$\                      $$\           $$\               
$$  __$$\                    \__|          \__|      $$  __$$\                     \__|          $$ |              
$$ |  $$ |$$$$$$\  $$$$$$$\  $$\ $$$$$$$\  $$\       $$ /  \__| $$$$$$$\  $$$$$$\  $$\  $$$$$$\$$$$$$\    $$$$$$$\ 
$$$$$$$  |\____$$\ $$  __$$\ $$ |$$  __$$\ $$ |      \$$$$$$\  $$  _____|$$  __$$\ $$ |$$  __$$\_$$  _|  $$  _____|
$$  ____/ $$$$$$$ |$$ |  $$ |$$ |$$ |  $$ |$$ |       \____$$\ $$ /      $$ |  \__|$$ |$$ /  $$ |$$ |    \$$$$$$\  
$$ |     $$  __$$ |$$ |  $$ |$$ |$$ |  $$ |$$ |      $$\   $$ |$$ |      $$ |      $$ |$$ |  $$ |$$ |$$\  \____$$\ 
$$ |     \$$$$$$$ |$$ |  $$ |$$ |$$ |  $$ |$$ |      \$$$$$$  |\$$$$$$$\ $$ |      $$ |$$$$$$$  |\$$$$  |$$$$$$$  |
\__|      \_______|\__|  \__|\__|\__|  \__|\__|       \______/  \_______|\__|      \__|$$  ____/  \____/ \_______/ 
                                                                                       $$ |                        
                                                                                       $$ |                        
                                                                                       \__|                        
    '''
)

if args.no_window:
    from pyvirtualdisplay import Display
    display = Display(visible=0, size=(800, 600))
    display.start()

bm = BrowserManager()
comm = bm.get_communities("На приеме у Шевцова", limit=30)
print('comm', comm)
posts_urls = bm.get_posts(comm[0], limit = 30)
print('posts_urls', posts_urls)
print('comment: ', bm.get_comments(posts_urls[0]))

#print(bm.get_comments('https://vk.com/itpedia_youtube?w=wall-88245281_8026263'))
