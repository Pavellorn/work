#take_stock
import requests 
import time 

head = {"Client-Id": "482702",  
"Api-Key": "7ae789b7-93ff-4ca7-aae0-4f47f48ffdec",    
"Content-Type": "application/json"}

ar_m1s = '1020005000653122'
ar_m1expr = "1020000718625000"
ar_m1 = '23589573193000'


# берет на вход  ид склада. выводит список артикулов на этом складе 
def take_stock(werehaus_id):
    print(f'Старт сбора артикулов Склада:{werehaus_id}')
    
    url_met = "https://api-seller.ozon.ru//v1/product/info/warehouse/stocks"
    
    payload = {
        "cursor": "",
        "limit": 1000,
        "warehouse_id": werehaus_id
    }
    
    result = []
    max_retries = 10  # Максимальное количество попыток
    timeout_seconds = 5  # Таймаут ожидания ответа
    
    while True:
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # Отправка запроса с таймаутом
                response = requests.post(url_met, headers=head, json=payload, timeout=timeout_seconds)
                response.raise_for_status()  # Проверка HTTP статуса
                
                data = response.json()
                break  # Успешный запрос, выходим из цикла повторных попыток
                
            except requests.exceptions.Timeout:
                retry_count += 1
                print(f"⚠️ Таймаут запроса. Попытка {retry_count}/{max_retries}")
                if retry_count < max_retries:
                    time.sleep(2)  # Ждем перед повторной попыткой
                else:
                    print("❌ Превышено максимальное количество попыток. Завершение работы.")
                    return result
                    
            except requests.exceptions.ConnectionError:
                retry_count += 1
                print(f"⚠️ Ошибка соединения. Попытка {retry_count}/{max_retries}")
                if retry_count < max_retries:
                    time.sleep(3)
                else:
                    print("❌ Не удалось установить соединение. Завершение работы.")
                    return result
                    
            except requests.exceptions.HTTPError as e:
                retry_count += 1
                print(f"⚠️ HTTP ошибка: {e}. Попытка {retry_count}/{max_retries}")
                print(payload)
                if retry_count < max_retries:
                    time.sleep(2)
                else:
                    print("❌ HTTP ошибка сохраняется. Завершение работы.")
                    return result
                    
            except requests.exceptions.RequestException as e:
                retry_count += 1
                print(f"⚠️ Ошибка запроса: {e}. Попытка {retry_count}/{max_retries}")
                if retry_count < max_retries:
                    time.sleep(2)
                else:
                    print("❌ Ошибка запроса сохраняется. Завершение работы.")
                    return result
                    
            except ValueError as e:
                retry_count += 1
                print(f"⚠️ Ошибка парсинга JSON: {e}. Попытка {retry_count}/{max_retries}")
                if retry_count < max_retries:
                    time.sleep(2)
                else:
                    print("❌ Не удалось обработать ответ сервера. Завершение работы.")
                    return result
        
        # Если все попытки исчерпаны, выходим
        if retry_count >= max_retries:
            break
        
        # Обработка успешного ответа
        try:
            stock = data['stocks']
            
            for st in stock:
                    if st['free_stock'] > 0:
                        result.append({
                            'offer_id': st['offer_id'],
                            'free_stock': st['free_stock']
                        })
            print(f"✅ Успешно:") 
            
            payload["cursor"] = data['cursor']
            print(f"Cursor: {data['cursor']}")
            
            if not data.get('has_next', False):
                print('✅ Цикл завершен, has_next вернул False')
                break
                
        except KeyError as e:
            print(f"❌ Ошибка структуры ответа: отсутствует ключ {e}")
            print(f"Ответ сервера: {data}")
            break
        
        # Задержка между запросами
        time.sleep(1)
    
    print(f"✅ Сбор завершен. Всего артикулов: {len(result)}")
    return result


# res = take_stock(ar_m1)
# print(res)
