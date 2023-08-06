import re
import requests
from urllib.parse import urlsplit, urljoin
from lxml import html
import csv
import argparse

class EmailCrawler:

    processed_urls = set()
    unprocessed_urls = set()
    emails = set()

    def __init__(self, website: str, max_pages=None):
        self.website = website
        self.unprocessed_urls.add(website)
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/78.0.3904.70 Chrome/78.0.3904.70 Safari/537.36',
        }
        self.base_url = urlsplit(self.website).netloc
        self.outputfile = self.base_url.replace('.','_')+'.csv'
        self.garbage_extensions = ['.aif','.cda','.mid','.midi','.mp3','.mpa','.ogg','.wav','.wma','.wpl','.7z','.arj','.deb','.pkg','.rar','.rpm','.tar.gz','.z','.zip','.bin','.dmg','.iso','.toast','.vcd','.csv','.dat','.db','.dbf','.log','.mdb','.sav','.sql','.tar','.apk','.bat','.bin','.cgi','.pl','.exe','.gadget','.jar','.py','.wsf','.fnt','.fon','.otf','.ttf','.ai','.bmp','.gif','.ico','.jpeg','.jpg','.png','.ps','.psd','.svg','.tif','.tiff','.asp','.cer','.cfm','.cgi','.pl','.part','.py','.rss','.key','.odp','.pps','.ppt','.pptx','.c','.class','.cpp','.cs','.h','.java','.sh','.swift','.vb','.ods','.xlr','.xls','.xlsx','.bak','.cab','.cfg','.cpl','.cur','.dll','.dmp','.drv','.icns','.ico','.ini','.lnk','.msi','.sys','.tmp','.3g2','.3gp','.avi','.flv','.h264','.m4v','.mkv','.mov','.mp4','.mpg','.mpeg','.rm','.swf','.vob','.wmv','.doc','.docx','.odt','.pdf','.rtf','.tex','.txt','.wks','.wps','.wpd']
        self.email_count = 0
        self.max_pages = max_pages

    def crawl(self):
        if self.max_pages is not None and len(self.processed_urls) >= self.max_pages:
            return

        url = self.unprocessed_urls.pop()
        print("CRAWL : {}".format(url))
        self.parse_url(url)
        if len(self.unprocessed_urls)!=0:
            self.crawl()
        else:
            print('End of crawling for {} '.format(self.website))
            print('Total urls visited {}'.format(len(self.processed_urls)))
            print('Total Emails found {}'.format(self.email_count))
            print('Dumping processed urls to {}'.format(self.base_url.replace('.','_')+'.txt'))
            with open(self.base_url.replace('.','_')+'.txt' ,'w') as f:
                f.write('\n'.join(self.processed_urls))

    def parse_url(self, current_url: str):
        response = requests.get(current_url, headers=self.headers)
        tree = html.fromstring(response.content)
        urls = tree.xpath('//a/@href')  # getting all urls in the page
        urls = [urljoin(self.website,url) for url in urls]
        urls = [url for url in urls if self.base_url == urlsplit(url).netloc]
        urls = list(set(urls))
        
        parsed_url = []
        for url in urls:
            skip = False
            for extension in self.garbage_extensions:
                if not url.endswith(extension) and  not url.endswith(extension+'/'):
                    pass
                else:
                    skip = True
                    break
            if not skip:
                parsed_url.append(url)

        for url in parsed_url:
            if url not in self.processed_urls and url not in self.unprocessed_urls:
                self.unprocessed_urls.add(url)
        self.parse_emails(response.text)
        self.processed_urls.add(current_url)

    def parse_emails(self, text: str):
        emails = set(re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text, re.I))
        for email in emails:
            skip_email = False
            for checker in ['jpg','jpeg','png']:
                if email.endswith(checker):
                    skip_email = True
                    break

            if not skip_email:    
                if email not in self.emails:
                    with open(self.outputfile, 'a', newline='') as csvf:
                        csv_writer = csv.writer(csvf)
                        csv_writer.writerow([email])
                    self.email_count +=1
                    self.emails.add(email)
                    print(' {} Email found {}'.format(self.email_count,email))

        if len(emails)!=0:
            return True
        else:
            return False


def main():
    parser = argparse.ArgumentParser(description="A simple email crawler")
    parser.add_argument("website", help="The website to crawl for emails.")
    parser.add_argument("--max_pages", type=int, help="The maximum number of pages to crawl.")
    args = parser.parse_args()
    
    args = parser.parse_args()
    crawl = EmailCrawler(args.website, args.max_pages)
   
    crawl.crawl()

if __name__ == "__main__":
    main()
