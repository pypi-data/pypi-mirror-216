import os
import click
from datetime import datetime, timezone, timedelta
import time
import logging
from taichu_dataflow.storage import create_storage

SERVICE_NAME = os.getenv('SERVICE_NAME', 'anonymous')
STORAGE_TYPE = os.getenv('STORAGE_MEDIA', 'MINIO')
storage_mgr = create_storage(STORAGE_TYPE)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--service', default='default', prompt='输入子服务名称', help='子服务名称')
@click.option('--start', default=datetime.now().strftime("%Y-%m-%d"), prompt='起始日期（默认为今天）（YYYY-MM-DD）', help='起始日期')
@click.option('--end', default=datetime.now().strftime("%Y-%m-%d"), prompt='结束日期（包含，默认为今天）（YYYY-MM-DD）', help='结束日期')
@click.option('--path', default='./', prompt='输入下载目录', help='下载目录')
def download(service, start, end, path):
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')
    if start_date > end_date:
        raise Exception('起止日期不正确')
    if not path.endswith('/'):
        path += '/'
        if not os.path.exists(path):
            raise Exception('下载目录不存在')
    for single_date in daterange(start_date, end_date):
        date_name = single_date.strftime("%Y-%m-%d")
        dest = f'{path}{date_name}/'
        logging.info(f'开始下载日期{date_name}的数据到路径[{dest}]...')
        storage_mgr.download_dir(f'sys/export_back/{SERVICE_NAME}/{service}/{date_name}/', dest)
        logging.info(f'完成下载日期{date_name}的数据到路径[{dest}]。')


if __name__ == '__main__':
    cli()
