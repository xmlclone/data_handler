import time
import click

from data_handler.models.base import DB_BASE, DB_ENGINE


@click.group()
def main():
    ...


@click.command(help='！！！！慎重！！！，初始化数据库，此操作会删除数据库并重新创建表')
def init_db():
    ipt = input('确认要执行此操作？？？如果确认输入Y: ')
    if ipt == 'Y':
        # print('5s后执行此操作，如果需要取消请按ctrl+c')
        for i in range(5):
            print(f'{5-i}s后执行此操作，如果需要取消请按ctrl+c')
            time.sleep(1)
    DB_BASE.metadata.drop_all(DB_ENGINE)
    DB_BASE.metadata.create_all(DB_ENGINE)
    print('执行完毕！！！')


for cmd in [
    init_db,
]:
    main.add_command(cmd)


if __name__ == '__main__':
    main()