'''
Sources:
https://www.youtube.com/watch?v=H2-5ecFwHHQ
https://playwright.dev/python/docs/api/class-playwright
https://builtin.com/data-science/asyncio
https://docs.python.org/3/library/asyncio-task.html
https://www.zenrows.com/blog/asynchronous-web-scraping-python#scrape-multiple-pages-asynchronously
'''
import asyncio
import json
import datetime
from playwright.async_api import async_playwright

url_list = [
    'https://infotel.ca/newsitem/police-crisis-intervention/cp67379207',
    'https://theprovince.com/news/local-news/capilano-university-hires-its-first-director-of-indigenous-education-and-affairs/wcm/68b28723-7d6a-4c19-957f-6230b2e4ce15',
    'https://www.brandonsun.com/local/2019/12/17/newspaper-letter-upsets-waywayseecappo-chief',
    'https://www.daily-times.com/story/news/local/navajo-nation/2019/12/24/navajo-quilter-featured-pbs-show-craft-america/2742016001/',
    'https://nanaimonewsnow.com/2020/01/17/inuit-women-in-canadas-north-encountering-racialized-policing-report-says-2/',
    'https://calgarysun.com/news/crime/supreme-court-to-hear-rough-sex-death-case-of-edmonton-prostitute/wcm/7b2b47b8-4464-4f88-a020-01d03f3e4954',
    'http://www.hilltimes.com/2018/02/12/trudeaus-cabinet-hosts-first-baby-shower-karina-gould/133851',
    'https://www.cbc.ca/news/politics/missing-and-murdered-indigenous-women-and-girls-in-spotlight-at-roundtable-1.2974970',
    'https://www.montereyherald.com/2023/05/04/event-in-seaside-to-raise-awareness-of-violence-but-also-celebrate-indigenous-women/',
    'https://globalnews.ca/news/9573238/shared-health-backup-plan-sexual-assault-program-replacement-nurses-train/',
    'https://fftimes.com/news/local-news/mayor-thanks-rrfn-for-their-annual-fish-fry-generosity/',
    'https://www.ottawaxpress.ca/people-still-waiting-for-the-mmiwg-cases-to-be-looked-into-by-the-task-forc/',
    'https://www.tricitynews.com/national-news/city-should-permanently-close-landfill-where-women-were-found-first-nations-leader-6812226',
    'https://vocm.com/2020/01/15/qalipu-mmiwg/',
    'https://www.cloverdalereporter.com/news/prime-minister-calls-discovery-of-indigenous-woman-in-winnipeg-landfill-heartbreaking-2449571',
    'https://www.cloverdalereporter.com/news/prime-minister-calls-discovery-of-indigenous-woman-in-winnipeg-landfill-heartbreaking-2449571',
    'https://www.kulr8.com/news/rescue-k--s-and-suspicious-vehicle-now-involved-in/article_b966064a-30d7-11ea-9b2f-9f53298b275a.html',
    'https://www.boisestatepublicradio.org/news/2023-08-22/canadian-protestors-call-for-search-for-missing-indigenous-women',
    'https://steinbachonline.com/articles/manitoba-ups-funding-for-missing-persons-response',
    'https://www.dailymirror.lk/breaking_news/Canada-has-no-right-here-NPF/108-264124'
]


async def fetch_data(url):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=0)
            title = await page.title()
            body_text = await page.inner_text("body")
            await browser.close()
            return {'URL': url, 'Title': title, 'Body Text': body_text}
    except asyncio.TimeoutError:
        print(f"Fetching data from {url} timed out.")
        return None
    except Exception as e:
        print(f"An error occurred while fetching data from {url}: {e}")
        return None


async def main():
    tasks = []
    for url in url_list:
        tasks.append(fetch_data(url))
    # groups and executes tasks concurrently
    results = await asyncio.gather(*tasks)
    # filter out none results (indicating errors)
    filtered_results = [result for result in results if result is not None]
    return filtered_results


start_time = datetime.datetime.now()

data = asyncio.run(main())

end_time = datetime.datetime.now()

elapsed_time = end_time - start_time

print(f"Code took {elapsed_time}.")

with open('webpage_data/webpage_data.json', 'w') as f:
    json.dump(data, f, indent=4)
