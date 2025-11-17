import requests 
import pandas as pd
import time 

'''
Обновляем остататки на складах M1 и B1 в кабинетах :
Получаем уникаольный код через метод озона https://api-seller.ozon.ru//v1/report/warehouse/stock
После получаем ссылку с помощью  https://api-seller.ozon.ru/v1/report/info
Качаем, убираем склады снулевым наличием через пандас
'''

def warehouse_body(id_warehaus, url_met, head):

    print('Начинаем')
    warehouse_body_m1 = {
    "language": "DEFAULT",
    "warehouseId": id_warehaus  # Замените на реальный ID склада
    }

    response = requests.post(url_met, headers=head, json=warehouse_body_m1)
    response = response.json()
    while not response:
        time.sleep(5)
        response = requests.post(url_met, headers=head, json=warehouse_body_m1)
        response = response.json()
        print(f"Ответ:{response}")

    print(f"Ответ:{response}")

    return response


def file_info_body(value, url_met, head):

    file_info_body = {
    "code": value['result']['code']
    } 
    response_info = requests.post(url_met, headers=head, json=file_info_body)
    response_info = response_info.json()

    print(f'Response Info:{response_info}')

    while response_info['result']['status'] != 'success':
        print(response_info)
        time.sleep(5)
        response_info = requests.post(url_met, headers=head, json=file_info_body)
        response_info = response_info.json()
        if response_info['result']['status'] != 'failed':
            print(f'Ошибка в получении кода{response_info['result']['error']}')
            break
        print('Новая попытка')


    url_stock_m1 = response_info['result']['file']
    print(f"Метод применён :{response_info}\n")

    return url_stock_m1


# скачиваем файл по ссылке что получили ранее
def download_file(url, filename):

    print(f"Начинаем качать файл {filename}")
    if not url:
        return print('Ошибка в получении ссылки')
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    print(f"Файл сохранён: {filename}\n")

    # Теперь файл полностью записан, можно читать
    df = pd.read_excel(filename, engine='openpyxl')
    df.columns = ['Идентификатор склада', 'Название склада', 'Артикул','Название товара','Доступно на моем складе, шт','Зарезервировано на моем складе, шт']
    # df = df[df['Доступно на моем складе, шт'] != 0] # если надо встроить какую-нибудь логику 
    print(f'Подготовлен склад {df["Идентификатор склада"]}')
    df['Идентификатор склада'] = df['Идентификатор склада'].astype(str)
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Товары на складах')
    
    print("Файл прочитан pandas успешно.")
    return df

def actual_m1(file_in, file_out, stock_name):
    # Чтение файла
    df_m1 = pd.read_excel(
        file_in, 
        engine='openpyxl'
    )

    df_clean = pd.DataFrame({
        "Название склада (идентификатор склада)": stock_name,
        'Артикул': df_m1['Артикул'],
        'Название товара': df_m1['Название товара'],
        'Доступно на складе, шт': df_m1["Доступно на моем складе, шт"]
    })
    
    df_clean.to_excel(
        file_out, 
        engine='openpyxl', 
        index=False, 
        sheet_name='Товары на складах'
    )

url_stock = "https://api-seller.ozon.ru//v1/report/warehouse/stock"
url_info = "https://api-seller.ozon.ru/v1/report/info" 

#заполняем информацией которая надо для метода апи
arr = [
{#Interparts RU - M1S
'head': {"Client-Id": "482702",  
"Api-Key": "7ae789b7-93ff-4ca7-aae0-4f47f48ffdec",    
"Content-Type": "application/json"},
"warehaus": [1020005000653122],
"local_file" : r"C:\Users\User\Desktop\СКЛАДЫ\Для обнуления\stockM1S.xlsx",
"stock_name" : 'M1S (1020005000653122)',
"local_m1" : r"\\xen\DATAW\Dropbox\InterParts\Ежедневные\исключения\stockM1.xlsx",
"m1_to_m1" : r"C:\Users\User\Desktop\СКЛАДЫ\Для обнуления\stockM1_TO_M1S.xlsx",
},
{#Interparts RU - M1 Express 
'head': {"Client-Id": "482702",  
"Api-Key": "7ae789b7-93ff-4ca7-aae0-4f47f48ffdec",     
"Content-Type": "application/json"},
"warehaus": [1020000718625000],
"local_file" : r"C:\Users\User\Desktop\СКЛАДЫ\Для обнуления\stockM1Expr.xlsx",
"stock_name" : 'M1 Express (1020000718625000)',
"local_m1" : r"\\xen\DATAW\Dropbox\InterParts\Ежедневные\исключения\stockM1.xlsx",
"m1_to_m1" :r"C:\Users\User\Desktop\СКЛАДЫ\Для обнуления\stockM1_TO_M1Expr.xlsx",
}
]

for ar in arr:
    print('-----------------------Поехали---------------------------------')

    # code_value = warehouse_body(ar['warehaus'], url_stock, ar['head'])
    # print(code_value)
    # url_stock_m1 = file_info_body(code_value, url_info, ar['head'])
    # download_file(url_stock_m1, ar["local_file"])

    actual_m1(ar["local_m1"],ar["m1_to_m1"],ar["stock_name"])
    print('-----------------------Готово---------------------------------')
print('-----------------------ВСЁ ГОТОВО---------------------------------')


