import os, platform, locale, json
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

DATABASE = json.load(open('./database.json'))
AVAIABLE_ACTIONS = (1, 2, 3, 4)


def format_value(value):
    return locale.currency(value, grouping=True, symbol=True)


def clear_terminal():
    system = platform.system()
    command = 'clear'

    if system == 'Windows':
        command = 'cls'

    os.system(command)


def ask_to_continue():
    print('')   
    input('Aperte "Enter" para continuar... ')

    clear_terminal()


def ask_action():
    print('------------------------------')
    print('')

    print('Ações disponíveis: ')
    print(' - 1. Lista de produtos;')
    print(' - 2. Realizar venda;')
    print(' - 3. Faturamento total;')
    print(' - 4. Sair;')

    print('')

    return int(input("O'que deseja fazer? (1, 2, 3 ou 4) "))


def list_products():
    for product in DATABASE['products']:
        print(f'- Código: {product["id"]}')
        print(f'- Nome: {product["name"]}')
        print(f'- Valor: {format_value(product["value"])}')
        print('')


def list_purchases(purchases):
    if len(purchases) == 0:
        print('Nenhuma venda realizada!')
    
        return

    total = 0

    for purchase in purchases:
        total += purchase["total"]

        print(f'- Horário: {purchase["created_at"]}')
        print(f'- Valor: {format_value(purchase["total"])}')
        print('')

    print(f'Total: {format_value(total)}')


def get_product_by_id(id):
    product_found = None

    for product in DATABASE['products']:
        if str(product['id']) == str(id):
            product_found = product
            break

    return product_found


def make_purchase():
    print('--------- Nova venda --------')
    print('')

    total = 0
    product_count = 1
    stop_purchase = False

    while stop_purchase is False:
        product_id = input(f'Informe o código do produto {product_count}: (ou F para finalizar) ')

        if product_id.upper() == 'F':
            stop_purchase = True
            break

        product = get_product_by_id(product_id)

        if product is not None:
            product_count += 1
            total += product['value']
        else:
            print('Produto não encontrado!')

    return total


choose_action = None
all_purchases = []


print('--------- Bem-vindo! ---------')
print('')

while choose_action != 4:
    if choose_action == None:
        choose_action = ask_action()

        if choose_action not in AVAIABLE_ACTIONS:
            print('')
            print('Ops... Você deve selecionar uma opção válida!')

            ask_to_continue()
            choose_action = None
    
        print('')
    else:
        if choose_action == 1:
            list_products()
            
        if choose_action == 2:
            total = make_purchase()

            if total == 0:
                print('')
                print('Venda não registrada!')
            else:
                current_date = datetime.now()
                formatted_date = current_date.strftime('%H:%M:%S')

                all_purchases.append({
                    'created_at': formatted_date,
                    'total': total,
                })

                print('')
                print(f'Total da venda: {format_value(total)}')

        if choose_action == 3:
            list_purchases(all_purchases)
        
        ask_to_continue()
        choose_action = None

print('')
print('------- Até a próxima! -------')
