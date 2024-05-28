# Research project about Missing and Murdered Indigenous Women and Girls (MMIWG)

## Overview
Using data obtained from the GDELT project, specifically the Global Knowledge Graph (gkg) dataset, this project aims to study how MMIWG is represented in the news. By extracting and filtering data from the gkg that pertains to Canada and Indigenous people, I will analyze the resulting data and use various forms of data representation to identify different trends and truths about MMIWG.

## Coding Choices

### SQL Queries
When querying the data from the gkg, I used SQLite and made queries on tables of increasing size. When working on how to get the results I wanted from my query, I first looked at the document identifier (URLs) for entries that had Canada in the Counts, with the location being one of the simplest ways to filter. I also added that Counts should contain Indigenous as another basic filter. Although this kind of query brings a decent amount of results, the majority were not directly relevant to MMIWG, so I looked through the documentation to find a way to increase the relevant results that the query brought. The addition of KILL in counts or Murder in all names helped with the search results because KILL in Counts means that GDELT's algorithm picked up on an individual being killed in the article, while Murder in all names also made sure articles that directly use 'Murdered Indigenous Women' would be included. I also included First Nation in all names or themes like INDIGENOUS to make the people being discussed more likely to be Indigenous.

In addition to inclusive filters, I excluded results that had covid or corona in the document identifier (URL), which would mean that the article content will discuss COVID-19. To further avoid this, I also removed articles that had them PANDEMIC and CORONAVIRUS. However, the downside is that some relevant articles that may include previews or links to other articles that discussed the pandemic would also be removed. Still, the percentage is negligible compared to the number of articles it removes, just about the pandemic. The reason I specifically tried to filter out this event is that because COVID was a disease that killed people, my other filters led to a lot of articles simply being about COVID-19, which is not what this research project is about. When excluding topics, I also filtered for results that did not contain pipeline since a decent amount of the results that came up were about the oil pipeline running through Indigenous lands.

The last part of my query is filtering, excluding results whose themes start with EDUCATION, GENERAL GOVERNMENT< GENERAL HEALTH, MANMADE DISASTER IMPLIED, and TAX_DISEASES. I chose to do this because after grouping by theme, I found that articles were generally about the first theme that showed in their list of themes, so filtering to exclude results that start with themes unrelated to MMIWG reduced the amount of non-relevant results. Although other non-relevant themes showed up, I chose to filter against only the ones that showed up the most to be on the safer side.

### Data Clustering

### Helpful Links
* https://www.gdeltproject.org/
* https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/
* http://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf
* http://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf
