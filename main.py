import argparse
from driver import BrowserManager, CustomBrowserManager

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

#bm = BrowserManager()
#comm = bm.get_communities("На приеме у Шевцова", limit=30)
#print('comm', comm)
#posts_urls = bm.get_posts(comm[0], limit = 30)
#print('posts_urls', posts_urls)
#print('comment: ', bm.get_comments(posts_urls[0]))
#
#print(bm.get_comments('https://vk.com/itpedia_youtube?w=wall-88245281_8026263'))
#
#
#for i in bm2.communities('На приеме у Шевцова'):
#    print(i)
#
#for i in bm2.comments('https://vk.com/itpedia_youtube?w=wall-88245281_8026843', limit=30):
#    print(i)
#
bm2 = CustomBrowserManager()

for i in bm2.communities('На приеме у Шевцова', limit=2):
    for j in bm2.posts(i, limit=10):
        print('j: ', j)
        for m in bm2.comments(j):
            pass
            #print(m)