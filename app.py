import click
from database import create_db, register_user, authenticate_user, get_id, get_user_id_from_session, create_session, generate_report
from models import Transaction

@click.group()
@click.pass_context
def cli(ctx):
    create_db()
    ctx.obj = {}

@cli.command()
@click.option('--username', '-u', type=str, help='Username for registration')
@click.option('--password', '-p', type=str, help='Password for registration')
@click.pass_context
def register(ctx, username, password):
    create_db()
    register_user(username, password)
    print('User registered successfully!')

@cli.command()
@click.pass_context
def login(ctx):
    username = click.prompt('Enter your username')
    password = click.prompt('Enter your password', hide_input=True)

    user_id = get_id(username)
    if authenticate_user(username,password):
        session_token = create_session(user_id)
        print(f"Login successful! Your session token is: {session_token}")
        # Store the session token in a secure way, e.g., environment variable or a configuration file
    else:
        print('Invalid credentials')

@cli.command()
@click.pass_context
def add_transaction(ctx):
    session_token = input("Enter your session token: ")  # Prompt for token
    user_id = get_user_id_from_session(session_token)
    if not user_id:
        print("Invalid session token or session expired.")
        return
    transaction_type = click.prompt("Enter transaction type (income/expense): ", type=click.Choice(['i', 'e']))
    amount = float(click.prompt("Enter the amount: "))
    category = click.prompt("Enter the category: ")
    date = click.prompt("Enter the date (YYYY-MM-DD): ")

    if transaction_type == 'i' :
        transaction_type = 'income'
    else : 
        transaction_type = 'expense'
    
    is_income = True if transaction_type == 'i' else False
    transaction = Transaction(user_id, amount, category, date, is_income)
    transaction.save_to_db()
    print(f"{transaction_type.capitalize()} added successfully!")

@cli.command()
@click.pass_context
def report(ctx):
    session_token = input("Enter your session token: ")  # Prompt for token
    user_id = get_user_id_from_session(session_token)
    if not user_id:
        print("Invalid session token or session expired.")
        return
    
    report_type = click.prompt("Select report type (monthly/yearly/categorized): ", type=click.Choice(['m', 'y', 'c']))

    if report_type in ('m', 'y'):
        year = click.prompt("Enter the year: ")
        if report_type == 'm':
            month = int(input("Enter the month (1-12): "))
        else:
            month = None  
    else:
        year = None  
        month = None
    
    if report_type == 'm':
        report_type = 'monthly'
    elif report_type == 'y':
        report_type = 'yearly'
    else :
        report_type = 'categorized'
    generate_report(report_type, year, month)

if __name__ == '__main__':
    cli()