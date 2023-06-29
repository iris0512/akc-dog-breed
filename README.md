# akc-dog-breed-analysis
scraping data from the American Kennel Club website to build a visualization to help compare two breeds of dogs. The dataset can also be used for other analytical purpsoses to answer questions regarding family-friendly breeds, group dogs by their characteristics and so on.

#### Steps
1. **data_extraction.py**: This file contains the code to extract the data using Beautiful Soup and Selenium. Since the traits and characteristics we need is present inside multiple divs and is based on a whether the UI is filled or selected, we opted to use Selenium to gather the data.
2. **data_validation.py**: This file checks to see if all the columns values within the expected ranges and to clean up the text columns. The height,weight and life expectancy is further split to create new columns of min and max values.
3. **akc_utils**: This file contains all the functions defined for extraction and cleaning of the data.
  
#### Visualisation: [Which dog to adopt?](https://app.powerbi.com/view?r=eyJrIjoiY2M1NGYwOWYtZTRkZS00YmE3LTk5MzktMGY0ZjllMGRjZjg0IiwidCI6IjdjNjZhNjlmLTFmMTctNGEwZi05NGU5LTYxNzU2NTQyYzQ2ZiIsImMiOjZ9&embedImagePlaceholder=true)
