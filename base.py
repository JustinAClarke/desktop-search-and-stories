import json
import urllib.request
import os,sys,time

class base():
    def __init__(self):
        self.getLatest()
        self.getCategories()
        
    def download(self,url,file):
        print("Downloading")
        u = urllib.request.urlopen(url)
        f = open(file, 'wb')
        meta = u.info()
#        file_size = float(u.getheader("Content-Length",0))
#        string="Downloading: {} Bytes: {}".format(file, file_size)
#        print(string)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
#            if file_size:
#                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
#                status = status + chr(8)*(len(status)+1)
#                print(status)

        f.close()
        
    def getLatest(self):
        url = "https://watrcoolr.duckduckgo.com/watrcoolr.js?o=json"
        file_name = "watrcoolr.js"
        if not os.path.isfile("watrcoolr.js"):
                self.download(url,file_name)
        time_diff=time.time()-os.path.getmtime(file_name)
        print("timeDiff: {}".format(time_diff))
        if time_diff > 300:
                self.download(url,file_name)

    def dumpLatest(self):
        self.getLatest()
        with open('watrcoolr.js') as json_data:
            stories = json.load(json_data)
            for story in stories:    
                print(story)
                print("\n")
                
    def getStories(self):
        self.getLatest()
        with open('watrcoolr.js') as json_data:
            stories = json.load(json_data)
            return stories
                
    def getStoriesCategory(self,cat):
        self.getLatest()
        catStories =[]
        with open('watrcoolr.js') as json_data:
            stories = json.load(json_data)
            for story in stories:    
                if story['category'] in cat:
                    catStories.append(story)
        return catStories

    def getStoriesProvider(self,prov):
        self.getLatest()
        catStories =[]
        with open('watrcoolr.js') as json_data:
            stories = json.load(json_data)
            for story in stories:    
                if story['type'] in prov:
                    catStories.append(story)
        return catStories

    def getStory(self,id):
        self.getLatest()
        with open('watrcoolr.js') as json_data:
            stories = json.load(json_data)
            for story in stories:    
                if story['id'] in id:
                    return story
                
    def showStories(self,story):
# {
#     'feed': 'http://medium.com/',
#     'favicon': 'http://duckduckgo.com/watrcoolr/icons/medium2.png',
#     'description': '',
#     'proof': 64,
#     'image': 'https://d3n6ab9lij5r0c.cloudfront.net/86c47fb674d51ec96ca5696bd6ddfd0c.jpeg',
#     'timestamp': '2016-03-04 22:35:26.994505',
#     'url': 'https://medium.com/@matthewpennell/how-eve-online-spoiled-every-other-mmo-in-the-world-for-me-2d6033043044',
#     'type': '91',
#     'title': 'How EVE Online spoiled every other MMO in the world for me',
#     'id': '134439',
#     'category': 'Features'
# }
        string = "Website: {site}\n Link: {link}\n Category: {category}\nTitle: {title}\n".format(site=story['feed'],link=story['url'],category=story['category'],title=story['title'])
        print(string)
    
    def showStoriesCategory(self,story,cat):
        if story['category'] in cat :
            string = "Website: {site}\n Link: {link}\n Category: {category}\n Image: {image}\nTitle: {title}\n".format(site=story['feed'],link=story['url'],image=story['image'],category=story['category'],title=story['title'])
            print(string)
            
    def getProviders(self):
        url="https://watrcoolr.duckduckgo.com/watrcoolr.js?o=json&type_info=1"
        file_name = "watrcoolrProv.js"
        if not os.path.isfile(file_name):
                self.download(url,file_name)
        with open(file_name) as json_data:
            self.providers = json.load(json_data)
            return self.providers

    def getProvider(self,id):
        self.getProviders()
        for providers in self.providers:    
            if providers['id'] == id:
                return providers


    def getCategories(self):
        self.getProviders()
        self.cat=[]
        for providers in self.providers:    
            if not providers['category'] in self.cat:
                self.cat.append(providers['category'])
        self.cat.sort()
        return self.cat
                    
    def listCategories(self):
        #if not self.cat:
        self.getCategories()
        print("Available Categories:\n")
        print("All")
        self.cat.sort()
        for cat in self.cat:
            print("{}".format(cat))
    
if __name__ == '__main__':
    app = cli()
    if len(sys.argv) > 1:
        if sys.argv[1] == 'All':
            app.getStories()
        else:
            app.getStoriesCategory(sys.argv)
    else:
        app.listCategories()
