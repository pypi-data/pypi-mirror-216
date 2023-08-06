import io
import qrcode

import typer
from InquirerPy import prompt
from typing_extensions import Annotated

from mb_cli import settings
from mb_cli.cli.validation import CoinAddressValidator, LimitAmountValidator

app = typer.Typer()
qr = qrcode.QRCode()

from mb_cli.cli.api import API

from rich import print
from rich.table import Table
from rich.panel import Panel
from rich.style import Style
from rich.console import Console

error_console = Console(stderr=True, style="bold red")
console = Console()

from mb_cli import version_check

@app.command('rates')
@version_check
def exchange_rates(
        proxy: Annotated[bool, typer.Option('-p', '--proxy', prompt='Do you want to use Tor?', help='Toggle Tor proxy.')] = True):
    """
    Show rates and exit.

    Put --proxy to use Tor.
    """

    if proxy:
        api = API(proxy=settings.TOR_PROXY, address=settings.TOR_ADDRESS)
    else:
        api = API()

    with console.status('Getting exchange rates...', speed=0.5):
        rates = api.get_rates()

    coin = prompt([
        {
            'type': 'list',
            'message': 'Select the coin you want to get the rates of?',
            'choices': settings.COIN_LIST
        }
    ])

    selected_coin = coin[0]
    selected_rates = []

    for rate in rates:
        if rate.split('-')[0] == selected_coin:
            selected_rates.append(rate)

    rates_table = Table(f'[cadet_blue]Currencies', '[bold red]Value')

    for rate in selected_rates:
        if rate.split("-")[1] != 'USD':
            rates_table.add_row(f'[bold blue]{rate.split("-")[1]}', f'[green]{str(rates[rate])}')

    print(Panel.fit(rates_table, title=f'[orange1]{selected_coin} rates', title_align='center',
                    subtitle=f'[yellow italic]USD price - {rates[f"{selected_coin}-USD"]}', subtitle_align='center'))

    print('[blue italic][link=https://intercambio.app/]Find best rates')

    typer.Exit()


@app.command('start')
@version_check
def exchange_start(
        proxy: Annotated[bool, typer.Option('-p', '--proxy', prompt='Do you want to use Tor?', help='Toggle Tor proxy.')] = True):
    """
    Start exchange process.

    Put --proxy to use Tor.
    """
    if proxy:
        api = API(proxy=settings.TOR_PROXY, address=settings.TOR_ADDRESS)
    else:
        api = API()

    coins = prompt(
        [{
            'type': 'list',
            'message': 'Which coin do you want to SELL?',
            'choices': settings.COIN_LIST
        },
            {
                'type': 'list',
                'message': 'Which coin do you want to BUY?',
                'choices': settings.COIN_LIST,
                'invalid_message': "You can't sell and buy the same coin."
            }])

    sell_coin = str(coins[0])
    buy_coin = str(coins[1])

    if sell_coin == buy_coin:
        error_console.print("You can't SELL and BUY the same coin.")
        return exchange_start()

    with console.status('Getting amount limits...', speed=0.5):
        amount_limits = api.get_limits(sell_coin)

    ex_process = [
        {'type': 'input', 'message': f'How much {sell_coin} do you want to SELL?', 'name': 'sell_amount',
         'validate': LimitAmountValidator(sell_coin=sell_coin, min_amount=amount_limits['min'],
                                          max_amount=amount_limits['max'])},
        {'type': 'input', 'message': f'Type in your {buy_coin} address:', 'name': 'buy_address',
         'validate': CoinAddressValidator(coin=buy_coin)}
    ]

    exchange = prompt(ex_process)

    sell_amount = exchange['sell_amount']
    buy_address = exchange['buy_address']

    with console.status('Calculating your order...', speed=0.5):
        calc = api.calculate_order(sell_amount, sell_coin, buy_coin)

    calc_results = f'''
    You will sell: [red]{sell_amount} {sell_coin}[/red]
    You will receive: [green]{calc['receive_amount']} {buy_coin}[/green]
    Receiving address: [bold blue]{buy_address}[/bold blue]
    '''

    print(Panel.fit(calc_results, title='[orange1]Order calculation[/orange1]', title_align='center'))

    order_confirm = [
        {'type': 'confirm', 'message': 'Do you want to initiate the order?', 'default': True}
    ]

    confirm = prompt(order_confirm)

    if confirm[0]:
        ...
    else:
        print('[italic]Exiting...[italic]')
        typer.Exit()

    with console.status('Creating your order...', speed=0.5):
        order = api.create_order(sell_amount, sell_coin, buy_coin, buy_address)

    typer.clear()


    qr.add_data(order['address'])
    qr_ascii = io.StringIO()
    qr.print_ascii(out=qr_ascii)
    qr_ascii.seek(0)

    order_results = f'''
    {qr_ascii.read()} 
    Send [red]{order['from_amount']} {order['from_currency']}[/red] to the address [bold blue]{order['address']}[/bold blue]
    '''

    print(
        Panel.fit(order_results, title=f'[orange1]Order - {str(order["trx"]).upper()}[/orange1]', title_align='center',
              subtitle=f'[yellow italic]time left {order["expiration"] / 60} hours...'))

    print(f'Track your order with the command: [cyan]track {str(order["trx"]).upper()}')

    print('[blue italic][link=https://majesticbank.sc/track]Go to site')

    typer.Exit()


@app.command()
@version_check
def track(order_id: Annotated[str, typer.Argument(help="Majestic Bank's order id.")], proxy: Annotated[
    bool, typer.Option('-p', '--proxy', prompt='Do you want to use Tor?', help='Toggle Tor proxy.')] = True):
    """
    Track order and exit.

    Put --proxy to use Tor.
    """
    if proxy:
        api = API(proxy=settings.TOR_PROXY, address=settings.TOR_ADDRESS)
    else:
        api = API()

    with console.status('Getting order info...', speed=0.5):
        order_status = api.track_order(order_id)

    if order_status['status'] != 'Completed':
        qr.add_data(order_status['address'])
        qr_ascii = io.StringIO()
        qr.print_ascii(out=qr_ascii)
        qr_ascii.seek(0)

        status = f'''
        {qr_ascii.read()}
    Status: [medium_orchid]{order_status['status']}[/medium_orchid]
    Amount to send: [red]{order_status['from_amount']} {order_status['from_currency']}[/red]
    Receiving amount: [green]{order_status['receive_amount']} {order_status['receive_currency']}[/green]
    Address: [bold blue]{order_status['address']}[/bold blue]
        '''

        print(Panel.fit(status, title=f'[orange1]Order - {str(order_status["trx"]).upper()}[/orange1]',
                        title_align='center',
                        subtitle=f'[yellow italic] {order_status["from_currency"]} to {order_status["receive_currency"]}'))
    else:
        print(Panel.fit('\n[green]You order is completed!\n',
                        title=f'[orange1]Order - {str(order_status["trx"]).upper()}[/orange1]',
                        title_align='center'))

    print('[blue italic][link=https://majesticbank.sc/track]Go to site')

    typer.Exit()
