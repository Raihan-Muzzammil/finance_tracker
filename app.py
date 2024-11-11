import click
from database import create_db, register_user

@click.command()
@click.option('--register', '-r', is_flag=True, help='Register a new user')
@click.option('--username', '-u', type=str, help='Username for registration')
@click.option('--password', '-p', type=str, help='Password for registration')
def main(register, username, password):
    create_db()
    if register:
        register_user(username, password)
        print('User registered successfully!')

if __name__ == '__main__':
    main()