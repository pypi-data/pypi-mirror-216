from mb_utils.src import logging
import mb.pandas as pd
from pp_project_pkg.utils import site_date_res,check_report_close_date,download_upload_dates_report
import argparse
import hydra

@hydra.main(config_name='./config.yml')
def fetch_data_run(args,logger=None):
    site_number = args.site_id
    site_start_date = args.date

    site_res =  site_date_res(site_number,logger=logger)
    report_res = check_report_close_date(site_res,start_date=site_start_date)
    if logger:
        logger.info(report_res.head())

    report_dates_res  = download_upload_dates_report(report_res,logger=logger)
    if logger:
        logger.info(report_dates_res.head())

    return report_dates_res


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Pp_project training Script")
    parser.add_argument("-d","--date", type=str, default='2023-06-20' , help="Date for getting the waste/production plan for. Default : 2023-06-06")
    parser.add_argument("-s","--site_id", type=int,default=30607, help="Site id. Default: 30607")
    parser.add_argument("-l","--logger", type=str,default=None, help="Logger. Default: None")
    args = parser.parse_args()
    if args.logger:
        logger = logging.logger
    fetch_data_run(args,logger=logger)