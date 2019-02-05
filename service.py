from utils import upload_data_s3
# import the filename of your scraper
import get_division_data


def handler(event, context):

    # Call the function from your imported file
    data = get_division_data.scrape_division()

    # Update where the file will be saved
    bucket_filepath = '2018/fusion/division-data.csv'

    # Upload it - JSON
    # upload_data_s3(data, bucket_filepath, 'json')

    # Upload it - CSV
    upload_data_s3(data, bucket_filepath, 'csv')


# this function is just for our testing purposes,
# just calling the main handler function
if __name__ == '__main__':
    handler(1, 2)
