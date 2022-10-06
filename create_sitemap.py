from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET
import requests, time, os, datetime

def ask_for_url():
    global url
    url=input('Enter your domain here:')
    try:
        global response
        checking =url[-1] # Getting the last character ofthe string (URL)
        if checking =='/':
            response =requests.get(url)
            start_crawling()
        else:
            url=url+'/'
            respnonse = requests.get(url)
            start_crawling()
    except Exception as e:
        print('error: ',e)
        print('Please enter a valid url ex: https://www.yourdomain.com, http://yourdomain.com')
        
        
def start_crawling():
    #os.system('cls')
    print('crawling')
    time.sleep(3)
    global checked_links
    checked_links=[]
    checked_links.append(url)
    crawling_web_pages()
    
def crawling_web_pages():
    global responses
    control=0
    while control < len(checked_links):
        try:
            responses =requests.get(checked_links[control])
            source_code =responses.text
            soup=BeautifulSoup(source_code,'html.parser')
            new_links=[w['href'] for w in soup.findAll('a',href=True)] # Getting all links from that page
            counter=0
            if len(new_links) <= 50000:
                while counter< len(new_links):
                    # This code is for those relative links which start with / slash
                    if 'http' not in new_links[counter]: # check if the linking on this site is absolute or relative
                        verify = new_links[counter][0] #Getting first character of every link & if it starts with slash / then we will remove this / slashat the end of the domain
                        if verify == '/':
                            new_links[counter]=new_links[counter][:1].replace('/','')+new_links[counter][1:] # This will remove only first slash in the link / string not every slash
                            new_links[counter]= url+new_links[counter] # joining domain with relative links
                            counter+=1
                        else:
                            # This code is for those relative links which doesn't start with / slash
                            new_links[counter]= url+new_links[counter] # joining domain with relative links
                            counter+=1
                    else:
                        counter+=1
                else:
                    counter2=0
                    while counter2 < len(new_links):
                        if '#' not in new_links[counter2] and 'malito' not in new_links[counter2] and '.jpg' not in new_links[counter2] and new_links[counter2] not in checked_links and url in new_links[counter2]:# This condition is very important, this will never append a link in the array which already exist in the array without this conditionthis script will never end and start appending the same link again and again
                            checked_links.append(new_links[counter2])
                            #os.system('cls')
                            print(str(control)+'/'+str(len(checked_links)))
                            print('')
                            print(str(control)+'web pages crawled & '+str(len(checked_links))+'web pages Found' )
                            print('')
                            print(new_links[counter2])# Display the current Url
                            counter2+=1
                        else:
                            counter2+=1
                    else:
                        #os.system('cls')
                        print(str(control)+'/'+str(len(checked_links)))
                        print('')
                        print(str(control)+'web pages crawled & '+str(len(checked_links))+'web pages Found' )
                        print('')
                        print(checked_links[control])# Display the current Url
                        control+=1         
            else:
                print('links are more then 50000.')
        except :
            control+=1 
    else:
        print(str(len(checked_links))+' web pages crawled')
        time.sleep(2)
        create_sitemap()
            
            
def create_sitemap():
    print('Still working :p')
    urlset=ET.Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    count=0
    while count < len(checked_links):
        urls=ET.SubElement(urlset,'url')
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        ET.SubElement(urls,'loc',).text = str(checked_links[count])
        ET.SubElement(urls,'lastmod',).text = str(today)
        ET.SubElement(urls,'priority',).text = '1.00'
        count+=1
    else:
        tree= ET.ElementTree(urlset)
        tree.write('sitemap.xml')
        print('your sitemap is ready.')
        
                     
ask_for_url()        