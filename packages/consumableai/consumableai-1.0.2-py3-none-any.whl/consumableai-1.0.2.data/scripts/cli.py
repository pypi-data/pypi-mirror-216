import click
import yaml
import pandas as pd
import psycopg2
import requests


CONFIG_FILE = 'config.yaml'
DATABASE_OPTIONS = ['postgresql',
                    # 'snowflake', 'mysql', 'sqlite', 'trino'
                    ]


def save_config(config_data):
    with open(CONFIG_FILE, 'w') as file:
        yaml.dump(config_data, file)


def load_config():
    try:
        with open(CONFIG_FILE, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return {}


@click.group()
def main():
    pass


@main.command()
def init():
    click.echo('Welcome to ConsumableAI.\n')
    config_data = load_config()

    api_key = click.prompt(
        'Please enter your CONSUMABLEAI_API_KEY, if you dont have it handy, please visit https://platform.consumableai.com:', default=config_data.get('API_KEY', ''))
    host = click.prompt('Please enter your database host:',
                        default=config_data.get('HOST', ''))
    port = click.prompt('Please enter your database port:',
                        default=config_data.get('PORT', ''))
    database = click.prompt(
        'Please enter your database name:', default=config_data.get('DATABASE_NAME', ''))
    username = click.prompt(
        'Please enter your database username:', default=config_data.get('USERNAME', ''))
    password = click.prompt(
        'Please enter your database password:', default=config_data.get('PASSWORD', ''))
    database_type = click.prompt('Please enter your database type from the options:', type=click.Choice(
        DATABASE_OPTIONS), default=config_data.get('DATABASE_TYPE', 'postgresql'))

    schemas = click.prompt(
        'Please enter your database schemas, should be separated by space:', default=config_data.get('SCHEMAS', ''))

    tables = click.prompt(
        'Please enter your database tables, should be separated by space:', default=config_data.get('TABLES', ''))

    config_data['API_KEY'] = api_key
    config_data['HOST'] = host
    config_data['PORT'] = port
    config_data['DATABASE_NAME'] = database
    config_data['USERNAME'] = username
    config_data['PASSWORD'] = password
    config_data['DATABASE_TYPE'] = database_type
    config_data['SCHEMAS'] = schemas
    config_data['TABLES'] = tables

    save_config(config_data)

    click.echo('your details are saved in config.yaml.')
    click.echo(
        'Now we will register you with ConsumableAI. This process can take couple of minutes to share spreadsheet link.')
    user_input = click.confirm(
        'Press Enter to proceed', prompt_suffix=' ', default='Y')

    if user_input == False:
        click.echo('Exiting the installation process...')
        raise click.Abort()

    click.echo('Executing the update command...')
    all_schemas = ""
    all_tables = ""
    if schemas:
        all_schemas = schemas.split()
    if tables:
        all_tables = tables.split()

    if database_type == "postgresql":
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )

        if not all_schemas and all_tables:
            query = '''SELECT table_schema as schema, table_name as table, column_name as "column name", data_type as "data type", is_nullable as constraint
                    FROM information_schema.columns
                    where 1=1
                    and table_name in %s
                    '''
            df = pd.read_sql(query, conn, index_col=None, params=(
                tuple(all_tables)))

        if all_schemas and not all_tables:
            query = '''SELECT table_schema as schema, table_name as table, column_name as "column name", data_type as "data type", is_nullable as constraint
                    FROM information_schema.columns
                    where 1=1
                    and table_schema in %s
                    '''
            df = pd.read_sql(query, conn, index_col=None, params=(
                tuple(all_schemas)))
            
        if not all_schemas and not all_tables:
            query = '''SELECT table_schema as schema, table_name as table, column_name as "column name", data_type as "data type", is_nullable as constraint
                    FROM information_schema.columns
                    where 1=1
                    '''
            df = pd.read_sql(query, conn, index_col=None)

        if all_schemas and all_tables:
            query = '''SELECT table_schema as schema, table_name as table, column_name as "column name", data_type as "data type", is_nullable as constraint
                    FROM information_schema.columns
                    where 1=1
                    and table_schema in %s
                    and table_name in %s
                    '''
            
            df = pd.read_sql(query, conn, index_col=None, params=(
                tuple(all_schemas), tuple(all_tables)))

        csv_string = df.to_csv(index=False)

        # Print the comma-separated string
        data = {
            "csv": csv_string
        }
        conn.close()

        click.echo('Now we are registering you with ConsumableAI...')
        click.echo(
            'This will take couple of minutes, you will get email of spreadsheet once your schema is ready.')
        requests.post(
            'https://api.consumableai.com/api/generate_google_sheet'+"?api_key=" + api_key,  json=data, timeout=600)

        # click.echo(response.text)
        # click.echo(response.json())


@main.command()
def update():
    config_data = load_config()

    api_key = config_data.get('API_KEY')
    host = config_data.get('HOST')
    port = config_data.get('PORT')
    username = config_data.get('USERNAME')
    password = config_data.get('PASSWORD')
    database_type = config_data.get('DATABASE_TYPE')
    schemas = config_data.get('SCHEMAS')
    tables = config_data.get('TABLES')

    if not host or not port or not api_key or not username or not password or not database_type or not columns:
        click.echo(
            'Please run `consumableai init` to provide the required configuration.')
        return
    # Perform queries and generate the CSV file


if __name__ == '__main__':
    main()
