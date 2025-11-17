import requests 
import pandas as pd
import time 

'''
Обновляем остататки на складах M1 и B1 в кабинетах :
ID Складов
Interparts RU M1 - 23589573193000
Interparts RU B1 - 1020000290471000
Interparts_OOO - 1020001178818000
Interparts+ - 1020001530352000
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
        print('Новая попытка')

    url_stock_m1 = response_info['result']['file']
    print(f"Метод применён :{response_info}\n")

    return url_stock_m1


# скачиваем файл по ссылке что получили ранее
def download_file(url, filename):

    print(f"Начинаем качать файл {filename}")
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    print(f"Файл сохранён: {filename}\n")

    # Теперь файл полностью записан, можно читать
    df = pd.read_excel(filename, engine='openpyxl', skiprows=1, header=None)
    df.columns = ['Идентификатор склада', 'Название склада', 'Артикул','Название товара','Доступно на моем складе, шт','Зарезервировано на моем складе, шт']
    df = df[df['Доступно на моем складе, шт'] != 0]
    print(f'Подготовлен склад {df["Идентификатор склада"]}')
    df['Идентификатор склада'] = df['Идентификатор склада'].astype(str)
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Товары на складах')
    
    print("Файл прочитан pandas успешно.")
    return df

'''
id_warehaus_RU = [23589573193000, 1020000290471000] M1 B1
id_warehaus_OOO = [1020001178818000] M1
id_warehaus_+ = [1020001530352000] M1
id_warehais_BY = [23113079960000] B1

'''

url_stock = "https://api-seller.ozon.ru//v1/report/warehouse/stock"
url_info = "https://api-seller.ozon.ru/v1/report/info" 

#заполняем информацией которая надо для метода апи
arr = [
{#Interparts RU - M1
'head': {"Client-Id": "482702",  
"Api-Key": "7ae789b7-93ff-4ca7-aae0-4f47f48ffdec",    
"Content-Type": "application/json"},
"warehaus": [23589573193000],
"local_file" : r"\\xen\DATAW\Dropbox\InterParts\Ежедневные\исключения\stockM1.xlsx"
},
{#Interparts + - M1
    'head': {"Client-Id": "1478853",  
    "Api-Key": "9be92024-67c5-477e-bd97-85412f5144df",     
    "Content-Type": "application/json"},
    "warehaus": [1020001530352000],
    "local_file" : r"\\xen\DATAW\Dropbox\InterParts\Ежедневные\Исключения+\stockM1.xlsx"
},
{#Interparts RU - B1
    'head': {"Client-Id": "482702",  
    "Api-Key": "33b925bb-50af-4a2c-87e1-c7d66e36c3ea",     
    "Content-Type": "application/json"},
    "warehaus": [1020000290471000],
    "local_file" : r"\\xen\DATAW\Dropbox\InterParts\Ежедневные\исключения\stockB1.xlsx"
},
{#Interparts OOO - M1
    'head': {"Client-Id": "1303860",  
    "Api-Key": "887ced9a-7ada-4678-8349-fd5edd421571",     
    "Content-Type": "application/json"},
    "warehaus": [1020001178818000],
    "local_file" : r"\\xen\DATAW\Dropbox\InterParts\Ежедневные\Исключения_ООО\stock_M1.xlsx"
},
{#Interparts BY -  B1
    'head': {"Client-Id": "370459",  
    "Api-Key": "419643b0-8150-4ba5-b5b7-32767f6b860f",     
    "Content-Type": "application/json"},
    "warehaus": [23113079960000],
    "local_file" : r"\\xen\DATAW\Dropbox\InterParts\Ежедневные\Исключения BY\B1.xlsx"
},
{#Interparts RU - M1Big
    'head': {"Client-Id": "482702",  
    "Api-Key": "7ae789b7-93ff-4ca7-aae0-4f47f48ffdec",     
    "Content-Type": "application/json"},
    "warehaus": [1020005000653289],
    "local_file" : r"\\xen\DATAW\Dropbox\InterParts\Ежедневные\исключения\stockM1Big.xlsx"
}
]

for ar in arr:
    print('-----------------------Поехали---------------------------------')

    code_value = warehouse_body(ar['warehaus'], url_stock, ar['head'])
    print(code_value)
    url_stock_m1 = file_info_body(code_value, url_info, ar['head'])

    download_file(url_stock_m1, ar["local_file"])
    print('-----------------------Готово---------------------------------')
print('-----------------------ВСЁ ГОТОВО---------------------------------')


