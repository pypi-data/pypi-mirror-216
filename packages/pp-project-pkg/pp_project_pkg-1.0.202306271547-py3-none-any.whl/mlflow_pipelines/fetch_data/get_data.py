from mb_utils.src import logging
import mb.pandas as pd
from pp_project_pkg.utils import site_date_res,check_report_close_date,download_upload_dates_report
import hydra
from omegaconf import DictConfig


@hydra.main(config_name='./config.yml')
def fetch_data_run(config: DictConfig):
    # site_number = args.site_id
    # site_start_date = args.date
    
    if config['data']['logger']:
        logger = logging.logger
    else:
        logger = None

    site_res =  site_date_res(config['data']['site_res'],logger=logger)
    report_res = check_report_close_date(site_res,start_date=config['data']['site_res'])
    if logger:
        logger.info(report_res.head())

    report_dates_res  = download_upload_dates_report(report_res,logger=logger)
    if logger:
        logger.info(report_dates_res.head())

    return report_dates_res


if __name__ == '__main__':
    fetch_data_run()