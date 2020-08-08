from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import os.path
import csv

option = Options()
option.headless = False

driver = webdriver.Firefox(options=option)
driver.maximize_window()
driver.implicitly_wait(5)

baseUrl = "https://youtube.com/"
keyword = "Analytics"


def getVideoUrl():
    driver.get(f"{baseUrl}/results?search_query={keyword}")
    time.sleep(3)

    for i in range(250):
        #scroll 500 px
        driver.execute_script('window.scrollTo(0,(window.pageYOffset+500))')
        #waiting for the page to load
        time.sleep(7) 



    allChannelList= driver.find_elements_by_css_selector("#video-title.yt-simple-endpoint.style-scope.ytd-video-renderer")
    links = list(dict.fromkeys(map(lambda a: a.get_attribute("href"),allChannelList)))
    return links


def getVideoDetails(urls):
    details = []
    ucount = 0
    
    for url in urls:
        driver.get(f"{url}/about")
        for i in range(1):
            driver.execute_script('window.scrollTo(0,(window.pageYOffset+500))')
            time.sleep(5)

        v_views = driver.find_element_by_css_selector("#count.style-scope.ytd-video-primary-info-renderer yt-view-count-renderer.style-scope.ytd-video-primary-info-renderer span.view-count.style-scope.yt-view-count-renderer").text
        vdate = driver.find_element_by_css_selector("yt-formatted-string.ytd-video-primary-info-renderer:nth-child(2)").text
        vlike = driver.find_element_by_css_selector("ytd-toggle-button-renderer.style-scope:nth-child(1) > a:nth-child(1) > yt-formatted-string:nth-child(2)").text
        vdislike = driver.find_element_by_css_selector("ytd-toggle-button-renderer.style-scope:nth-child(2) > a:nth-child(1) > yt-formatted-string:nth-child(2)").text
        vlink = url
        
       #storing all comments in a list
        vcomments = []
        totalcomments= len(driver.find_elements_by_xpath("""//*[@id="content-text"]"""))
        zerocomment = 0
        if totalcomments >  zerocomment:     
            for i in range(totalcomments):
            
                comments = driver.find_elements_by_xpath('//*[@id="content-text"]')[i].text.encode('utf8')         
                vcomments.append(comments)
            
        else:
            vcomments.append("No Comments")
        
        ucount+=1
        obj = [vlink,v_views,vdate,vcomments,vlike,vdislike] 
        
        #writing in file in csv file
        filename = "outputscrap.csv"             
        file_exists = os.path.isfile(filename)

        with open (filename, 'a') as csvfile:
             
             fieldnames = ['S.No.','video link','video views','uploaded date','comments','like','dislikes']
             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
             if not file_exists:
                writer.writeheader()
             writer.writerow({'S.No.': ucount, 'video link': vlink, 'video views': v_views, 'uploaded date': vdate, 'comments':vcomments, 'like':vlike, 'dislikes': vdislike})

        details.append(obj)
    return details

if __name__ == "__main__":
    allVideoUrls = getVideoUrl()
    allVideoDetails = getVideoDetails(allVideoUrls)
    #print on console
    print(allVideoDetails)
    