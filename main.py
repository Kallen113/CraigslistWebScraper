# import Craigslist_Rentals class, which implements the webcrawler and web scraping functions
from Rentals.selenium_webcrawler import Craigslist_Rentals

from Rentals.clean_city_names import clean_city_names_for_sf, sf_neighborhoods, clean_given_city_names_data, sj_neighborhoods, oakland_neighborhoods, alameda_neighborhoods, hayward_neighborhoods, richmond_neighborhoods, santa_clara_neighborhoods  # import functions to clean SF city names data and import lists of all neighborhoods for given cities--e.g., SF neighborhoods (including various abbreviations used on craigslist)  
from Rentals.clean_santa_cruz_data import clean_mislabelled_santa_cruz_data, san_cruz_cities

# import inquirer library so we can prompt user in command line to select from a dropdown of values to select the desired subregion on which we will implement the webcrawler.
import inquirer

# import functions for selecting SF Bay Area region & subregion names and codes:
from determine_subregions_for_given_clist_region.sfbay_craigslist_subregion_definitions import print_sfbay_subregion_names, inquirer_prompt_user_at_terminal

# import functions for selecting *non-SF Bay* metropolitan regions & subregions-- e.g., Chicago, IL, Seattle, WA, etc.
from determine_subregions_for_given_clist_region.determine_subregions_for_given_clist_region import prompt_user_for_region_and_return_region_name, return_hompeage_URL_for_given_region, parse_region_code_for_craigslist_URL_main_webcrawler, parse_subregions_via_xpath,  prompt_user_for_subregion 


def main():
    ## Specify the arguments we will use for each component of the Craigslist_Rentals class, so that we will scrape rental data for the given region, subregion, etc.

    # specify names of metropolitan craigslist region names and their corresponding craigslist urls, store in dict
    clist_region_and_urls = {
        'SF Bay Area, CA':'https://sfbay.craigslist.org/',
        'San Diego, CA':'https://sandiego.craigslist.org/',
        'Chicago, IL':'https://chicago.craigslist.org/',
        'Seattle, WA':'https://seattle.craigslist.org/',
        # 'Tacoma, WA':'https://seattle.craigslist.org/tac/',
        'Los Angeles, CA':'https://losangeles.craigslist.org/',
        'Phoenix, AZ':'https://phoenix.craigslist.org/',
        'Portland, OR':'https://portland.craigslist.org/',
        'Dallas/Fort Worth, TX':'https://dallas.craigslist.org/',
        'Minneapolis/St. Paul, MN':'https://minneapolis.craigslist.org/',
        'Boston, MA':'https://boston.craigslist.org/',
        'Washington, D.C.':'https://washingtondc.craigslist.org/',
        'Atlanta, GA':'https://atlanta.craigslist.org/',
        'Miami, FL':'https://miami.craigslist.org/',
        'Hawaii (subregions by island)':'https://honolulu.craigslist.org/',
        'Detroit, MI':'https://detroit.craigslist.org/',
        'New York City, NY':'https://newyork.craigslist.org/',
        'Vancouver, Canada':'https://vancouver.craigslist.org/',
        'Toronto, Canada':'https://toronto.craigslist.org/'
        }
    
    # Prompt user for region:
    region_name  = prompt_user_for_region_and_return_region_name(clist_region_and_urls) #  Prompt user to select specific region on craigslist to search, from terminal, among the various listed metropolitan areas in the U.S. and Canada:

    # return hompage URL for the selected region, which we will use to parse corresponding subregion codes
    region_URL = return_hompeage_URL_for_given_region(clist_region_and_urls, region_name) # return hompage URL for region, which we will use to parse corresponding subregion codes

    # specify region craigslist code, for webcrawler's starting URL-- parse the region_URL to craigslist region codes:
    region = parse_region_code_for_craigslist_URL_main_webcrawler(region_URL)  # use split() method to parse the region code from the region_URL of the selected region!

    # Next, parse clist subregion (if needed), and prompt user to select a subregion corresponding to the selected region:

    # if selected region is *not* SF Bay Area, CA, we will need to parse the subregion codes for given (parent) region:
    if region_name != 'SF Bay Area, CA': 

        # specify xpath argument needed to parse the clist subregion codes for a given (parent) region 
        ul_subregions_xpath = '//*[@id="topban"]/div[1]/ul'

        # run parse_subregions_via_xpath() to parse subregion codes into a list, given the following args: region URLs list (ie, clist_region_urls), an empty list to be populated, and an xpath arg
        subregions_list = parse_subregions_via_xpath(region_URL, ul_subregions_xpath)

        # sanity check on list of subregions
        print(f'Subregion vals for given region:\n{subregions_list}\n')

        # select subregion val: ie, prompt user in terminal to select one of the subregions from the subregions_list:
        subregion = prompt_user_for_subregion(subregions_list)  # select a subregion from the list of parsed subregion codes, and parse the value selected

        # sanity check
        print(f'Subregion selected:\n{subregion}')
    
    # if user chose SF Bay Area, CA region, we can manually supply the relevant subregion codes and names:
    else:
        # rename SF Bay Area, CA to 
        print_sfbay_subregion_names() # print what each sfbay craglslist subregion actually represents--ie, which regions and/or cities. 
        ## specify each Sf Bay subregion:
        sfbay_subregion_vals = ['eby', 'nby', 'pen', 'sby', 'scz', 'sfc'] # specify a list of all Bay Area subregions for craigslist site-- NB: craigslist lumps Santa Cruz ('scz') within their sfbay site.  
        # select subregion val: ie, prompt user in terminal to select one of the subregions:
        subregion = inquirer_prompt_user_at_terminal(sfbay_subregion_vals)  # parse the specific value the user selected  
        

        # sanity check
        print(f'Subregion value selected:\n{subregion}')
    
    ## Specify all other parameters for Craigslist_Rentals() class, including min & max price for searchform, etc.:
    
    ## filter housing category to 'apa'-ie, rental listings (apartments & housing for rent)
    housing_category = 'apa'
    ## filter min & max rental price to avoid scraping unusual otn misclassified rental listings:
    min_price = 50 # filter out all unusual rental listings that do not specify rental price in the title of the listing--ie, the 'postingtitle' h1 (which are displated as $0 in when searching on craigslist)  
    max_price = 12000 # filter out all listings that have very high prices, since many of these listings are mislabelled and are oftentimes actually property lots for sale (even though we are searching for apartment-specific listings)   
    # filter rental period to monthly, to ensure rental prices are readily comparable:
    rent_period = 3  # ie, only show listings that show rental prices in monthly intervals. 
    # search for all current rental listings regardless of the sale date
    sale_date = "all+dates" # look up all current craigslist rental listings for given location, price range, and monthly rental periods: ie, regardless of when the listing will be available for moving into.
    
    # given above arguments, initialize a customized craigslist rental listing URL via the Craigslist_Rentals class, for the selenium webcrawler to access:
    craigslist_crawler = Craigslist_Rentals(region, subregion, housing_category, min_price, max_price, rent_period, sale_date)

    ## Access the craigslist URL via selenium Chrome webdriver
    craigslist_crawler.load_craigslist_form_URL()

    ## Implement the main web crawler via obtain_listing_urls() method, and obtain the rental listing href URLs from the pages of listings (and append to listing_urls list): 
    # 1st argument of obtain_listing_urls() method: specify all possible xpaths to the first listings on a given page, so we can wait until the listings have loaded before scraping data:
    xpaths_first_listing_url_on_page = '//*[@class="title-string"] | //*[@id="search-results-page-1"]/ol/li[1]/div/div[1]/div/div[2]/a | //*[@id="search-results-page-1"]/ol/li[1]/div/a[2] | //*[@id="search-results"]/li[1]/div'  # xpath to 1st inner listing hrefs on page. NB: the pipe (ie, |) is used as a Boolean "or" operator so that we can account for any one of multiple possible xpaths!!

    # 2nd argument of obtain_listing_urls() method: specify xpaths for 
    xpaths_listing_urls = '//a[@class="titlestring"] | //a[@class="post-title"] | //a[@class="result-title hdrlnk"]'
    
    # 3rd argument of obtain_listing_urls() method: specify the xpaths for the 'next' page button widget we need to click to navigate to each subsequent page: 
    next_page_button_xpaths = '//*[@class="bd-button cl-next-page icon-only"] | //*[@class="button next"]'
    
    # implement obtain_listing_urls() method to initiate webcrawler:
    listing_urls = craigslist_crawler.obtain_listing_urls(xpaths_first_listing_url_on_page, xpaths_listing_urls, next_page_button_xpaths)  # method requires 2 arguments: xpaths to first listings on given page, and xpaths to the next page button widgets

    ## scrape the rental listings' data, and store data as dict of lists:
    dict_scraped_lists = craigslist_crawler.scrape_listing_data(listing_urls)  

    ## Perform data cleaning on scraped data:
    dict_scraped_lists = craigslist_crawler.clean_scraped_data(dict_scraped_lists)
    
    ## Transform the dictionary of lists to Pandas' DataFrame, and peform additional data cleaning and wrangling:
    df = craigslist_crawler.dict_to_df_pipeline(dict_scraped_lists)

    ## Execute DataFrame to CSV data pipeline,after cleaning city names data for specific subregions 
    craigslist_crawler.df_to_CSV_data_pipeline(df)

if __name__== "__main__":
    main()