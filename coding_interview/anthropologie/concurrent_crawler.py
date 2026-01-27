from typing import List, Dict, Any
import asyncio
import time


class Crawler:
    """
    1. search algorithm, needs a queue to store upcoming pages and visited pages
    
    Attributes:
        visited_pages: set() -> total pages crawled
        queue: []
        total_links: int, total links found
        all_discovered_urls: set()
        broken_links: set()
    """
    def __init__(self):
        self.queue = []
        self.visited_pages = set()
        self.total_links = 0
        self.all_discovered_urls = set()
        self.broken_links = set()
        self.last_crawl_time = None

    def extract_links(self, url):
        """extract all links from each page
        """
        return []
        
    def filter_qualified_links(self, current_url, links):
        """
        Attributes:
            current_url: "https://www.joeylol.im/"
        """
        domain = self.extract_domain(current_url)
        if not domain:  # no qualified domain, then return empty
            return []

        result = []
        for link in links:
            link_domain = self.extract_domain(link)
            if link_domain != domain:  # invalid link
                continue      
            if link in self.visited_pages:  # already visited
                continue
            if link in self.queue:  # already in the queue to be visited
                continue
            
            # passed all validation
            result.append(link)
        return result
            
        
    def extract_domain(self, url):
        split_dashes = url.split("/")
        if len(split_dashes) < 3:
            print("error! malformed url that couldn't find domain")
            self.broken_links.add(url)
            return None
        return split_dashes[2]
        

    def crawl(self, seed_url: str, max_pages: int = 100) -> List[str]:
        """
        Crawl pages starting from seed_url, staying within same domain.
        
        1. extract all links belong to current url
        2. filter qualified links (same domain, not visited)
        3. add them into queue for next crawl
        
        Args:
            seed_url: Starting URL (e.g., "https://example.com/page1")
            max_pages: Maximum pages to crawl
        
        Returns:
            List of all discovered URLs
            
        TODO(zhaoyu): need to add exception handling
        """
        self.queue = [seed_url]
        
        while self.queue:
            current_url = self.queue.pop(0)
            # mark this page visited
            self.visited_pages.add(current_url)
            # exit if max_pages reached
            if len(self.visited_pages) >= max_pages:
                return list(self.visited_pages)
            
            all_links = self.extract_links(seed_url)
            
            qualified_links = self.filter_qualified_links(current_url, all_links)
            
            self.queue.extend(qualified_links)
            # finish processing this url
        return list(self.visited)
    
    def crawl_with_stats(self, seed_url: str, max_pages: int = 100) -> Dict[str, Any]:
        """
        Returns:
            {
                "urls": List[str],           # All discovered URLs
                "total_pages": int,           # Number of pages crawled
                "total_links": int,           # Total links found
                "broken_links": List[str]     # URLs that returned errors
            }
        """
        self.queue = [seed_url]
        
        while self.queue:
            current_url = self.queue.pop(0)
            # mark this page visited
            self.visited_pages.add(current_url)
            # exit if max_pages reached
            if len(self.visited_pages) >= max_pages:
                return self.get_stats()
            
            all_links = self.extract_links(seed_url)
            # increase total links found
            self.total_links += len(all_links)
            self.all_discovered_urls.add(all_links)
            
            qualified_links = self.filter_qualified_links(current_url, all_links)
            
            self.queue.extend(qualified_links)
            # finish processing this url
        return self.get_stats()
            
    def get_stats(self):
        return {
            "urls": list(self.all_discovered_urls),
            "total_pages": len(self.visited_pages),
            "total_links": self.total_links,
            "broken_links": list(self.broken_links),
        }
    
    async def crawl_concurrent(self, seed_url: str, max_pages: int = 100, 
                          max_concurrent: int = 10) -> List[str]:
        """
        Implement concurrent crawling using asyncio or threading.
        Control concurrency with max_concurrent parameter.
        
        1. start concurrent threads like 10
        2. need to ensure thread-safety, e.g., locking on common datastructure
        wait, Python is always single thread, so it should be OK
        3. each concurrent task would pop queue and start with that url
        """
        self.max_pages = max_pages
        
        self.queue = [seed_url]
        
        tasks = [self.start_one_crawler(i) for i in range(max_concurrent)]
    
        # Run all tasks concurrently and wait for all of them to complete
        await asyncio.gather(*tasks)
        
        print("Main: All tasks completed.")
        
    def found_max_pages(self):
        """check whether max pages found so far
        """
        return len(self.visited_pages) >= self.max_pages
        
    def at_least_one_crawler_is_working(self):
        """check whether at least crawler is working
        
        Attributes:
            status: {
                crawler1: working | waiting
            }
        """
        for value in self.status.values():
            if value == "working":
                return True
        return False
        
    def should_stop_working(self):
        """each crawler should determine whether it should stop working
        
        1. if exceed max_pages
        2. if queue is empty and no crawler is working
        """
        if self.found_max_pages():
            return True
        
        if not self.queue and not self.at_least_one_crawler_is_working():
            return True
        return False
    
    async def start_one_crawler(self, task_id):
        """
        1. determine whether the whole job needs to keep going, if yes
        2. check whether it can find job
            if yes, then keep working
            if no, it must wait for other crawler
        """
        while not self.should_stop_working():
            if not self.queue:  # wait the other, let's sleep
                self.status[task_id] = "waiting"
                print("no task found, wait for a while for others")
                time.sleep(10)
                continue      
            current_url = self.queue.pop(0)
            # found item to work on
            self.status[task_id] = "working"
            
            # mark this page visited
            self.visited_pages.add(current_url)
            # exit if max_pages reached
            if len(self.visited_pages) >= max_pages:
                return self.get_stats()
            
            all_links = self.extract_links(seed_url)
            # increase total links found
            self.total_links += len(all_links)
            self.all_discovered_urls.add(all_links)
            
            qualified_links = self.filter_qualified_links(current_url, all_links)
            
            self.queue.extend(qualified_links)
            # finish processing this url
        return self.get_stats()
        
    async def crawl_polite(self, seed_url: str, max_pages: int = 100,
                      max_concurrent: int = 10,
                      delay_seconds: float = 1.0) -> List[str]:
        """
        Add rate limiting to be a polite crawler.
        Respect robots.txt (bonus).
        """
        self.queue = [seed_url]
        
        while self.queue:
            current_url = await self.find_next_url()
            # mark this page visited
            self.visited_pages.add(current_url)
            # exit if max_pages reached
            if len(self.visited_pages) >= max_pages:
                return self.get_stats()
                
            # check whether it is allowed by robots.txt
            if not self.allow_robot(current_url):
                continue
            
            all_links = await self.extract_links(seed_url)
            # increase total links found
            self.total_links += len(all_links)
            self.all_discovered_urls.add(all_links)
            
            qualified_links = self.filter_qualified_links(current_url, all_links)
            
            self.queue.extend(qualified_links)
            # finish processing this url
        return self.get_stats()
        
    def allow_robot(self, url:str):
        if url.endswith("robots.txt"):
            # TODO(zhaoyu): parsing robots.txt to see whether it is allowed
            return False
        return True
        
    async def find_next_url(self, delay_seconds):
        """
        """
        current_timestamp = time.time()
        if current_timestamp - self.last_crawl_time <= 60:
            time.sleep(delay_seconds)
        return self.queue.pop(0)