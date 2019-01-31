from utils import upload_data_s3
# import the filename of your scraper
import scraper_file
import json

def handler(event, context):

    # Call the function from your imported file
    data = json.dumps(scraper_file.scrapeStuff())

    # Update where the file will be saved
    bucket_filepath = 'data-store/2018/<file-name>.csv'

    # Upload it - JSON
    upload_data_s3(data, bucket_filepath, 'json')

    # Upload it - CSV
    # upload_data_s3(data, bucket_filepath, 'csv')


# this function is just for our testing purposes,
# just calling the main handler function
if __name__ == '__main__':
    handler(1, 2)
