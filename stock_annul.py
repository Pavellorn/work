#stock_annul

import requests 
import pandas as pd
import time 
from take_stock import take_stock

#avail на что поменять наличие на складе
def stock_form(warehouse_id, offer_id, avail=0):
    """
    update_stock: False - обнулить, True - установить остатки из stock
    """

    stok = {
        "offer_id": offer_id,
        "warehouse_id": warehouse_id,
        "stock": avail 
    }
    return stok

def stock_annul(warehaus, url, stock, update_stock=False):
    """
    update_stock: False - обнулить, True - установить остатки из stock
    """ 

    max_retries = 10
    timeout_seconds = 5
    
    result = []

    # Формируем список структуру запроса с артикулами
    for item in stock:
        offer_id = item['offer_id']
        if update_stock:
            # Берем free_stock из переданного stock
            free_stock = item['free_stock']
            stocks = stock_form(warehaus, offer_id, free_stock)
        else:
            # Обнуляем - передаем 0
            stocks = stock_form(warehaus, offer_id, 0)
        result.append(stocks)
        
    if not result:
        print('❌ Список артикулов пуст')
        return
        
    i = 0
    j = 100
    
    while True:
        stock_batch = result[i:j]  # Переименовал переменную, чтобы не конфликтовало
        i += 100
        j += 100
        
        print(f'Обработано: {i}')
        print('--' * 50)
        
        payload = {
            "stocks": stock_batch
        }
        
        if update_stock:
            print("📈 Режим: ОБНОВЛЕНИЕ остатков")
        else:
            print("📉 Режим: ОБНУЛЕНИЕ остатков")
        
        retry_count = 0
        # Отправка запроса с логикой обработки ошибок
        while retry_count < max_retries:
            try:
                # Отправка запроса с таймаутом
                response = requests.post(url, headers=head, json=payload, timeout=timeout_seconds)
                response.raise_for_status()  # Проверка HTTP статуса
                
                data = response.json()
                print(f"✅ Успешно") 
                break  # Успешный запрос
                
            except requests.exceptions.Timeout:
                retry_count += 1
                print(f"⚠️ Таймаут запроса. Попытка {retry_count}/{max_retries}")
                if retry_count < max_retries:
                    time.sleep(2)
                else:
                    print("❌ Превышено максимальное количество попыток. Пропускаем партию.")
                    break
                    
            except requests.exceptions.ConnectionError:
                retry_count += 1
                print(f"⚠️ Ошибка соединения. Попытка {retry_count}/{max_retries}")
                if retry_count < max_retries:
                    time.sleep(3)
                else:
                    print("❌ Не удалось установить соединение. Пропускаем партию.")
                    break
                    
            except requests.exceptions.HTTPError as e:
                retry_count += 1
                print(f"⚠️ HTTP ошибка: {e}. Попытка {retry_count}/{max_retries}")
                if retry_count < max_retries:
                    time.sleep(2)
                else:
                    print(f"❌ HTTP ошибка сохраняется. Пропускаем партию.")
                    break
                    
            except requests.exceptions.RequestException as e:
                retry_count += 1
                print(f"⚠️ Ошибка запроса: {e}. Попытка {retry_count}/{max_retries}")
                if retry_count < max_retries:
                    time.sleep(2)
                else:
                    print("❌ Ошибка запроса сохраняется. Пропускаем партию.")
                    break
                    
            except ValueError as e:
                retry_count += 1
                print(f"⚠️ Ошибка парсинга JSON: {e}. Попытка {retry_count}/{max_retries}")
                if retry_count < max_retries:
                    time.sleep(2)
                else:
                    print("❌ Не удалось обработать ответ сервера. Пропускаем партию.")
                    break
        
        # Пауза между запросами
        time.sleep(2)
        
        # Проверка завершения
        if len(stock_batch) < 100:
            print("✅ Все артикулы обработаны")
            break
    
    print(f"✅ Завершено. Всего отправлено: {len(result)} артикулов")
    print("//"*50)

head = {"Client-Id": "482702",  
"Api-Key": "7ae789b7-93ff-4ca7-aae0-4f47f48ffdec",     
"Content-Type": "application/json"}

ar_m1s = '1020005000653122'
ar_m1expr = "1020000718625000"
ar_m1 = '23589573193000'

url_met = "https://api-seller.ozon.ru//v2/products/stocks"

# Получаем остатки с основного склада
stock_m1 = take_stock(ar_m1)
print(f"Получено {len(stock_m1)} артикулов с основного склада")

# M1S Обнуление
print("\nНачинаем обнуление M1S")
stock_m1s_current = take_stock(ar_m1s)
stock_annul(ar_m1s, url_met, stock_m1s_current, update_stock=False)

# M1Express обнуление
print("\nНачинаем обнуление M1Express")
stock_m1expr_current = take_stock(ar_m1expr)
stock_annul(ar_m1expr, url_met, stock_m1expr_current, update_stock=False)

time.sleep(60)
# Обновляем M1S из основного склада
print("\nНачинаем обновление M1S из основного склада")
stock_annul(ar_m1s, url_met, stock_m1, update_stock=True)

# Обновляем M1Express из основного склада
print("\nНачинаем обновление M1Express из основного склада")
stock_annul(ar_m1expr, url_met, stock_m1, update_stock=True)

print("\n Все операции завершены!")