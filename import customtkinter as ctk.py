import customtkinter as ctk
import json

class WarehouseApp(ctk.CTk):
    def __init__(self, warehouses_dict):
        super().__init__()
        
        self.title("Выбор складов OZON")
        self.geometry("600x500")
        ctk.set_appearance_mode("Dark")
        
        self.warehouses = warehouses_dict
        self.selected_warehouses = {}
        
        self.create_widgets()
    
    def create_widgets(self):
        # Заголовок
        title = ctk.CTkLabel(self, text="Выберите склады:", 
                            font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Прокручиваемая область
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Создаем чекбоксы для каждого склада
        self.checkbox_vars = {}
        
        for warehouse_id, warehouse_name in self.warehouses.items():
            # Создаем переменную для чекбокса
            var = ctk.BooleanVar()
            
            # Создаем сам чекбокс
            checkbox = ctk.CTkCheckBox(
                self.scroll_frame,
                text=f"{warehouse_name} (ID: {warehouse_id})",
                variable=var,
                command=lambda wid=warehouse_id, wn=warehouse_name: self.on_checkbox_toggle(wid, wn)
            )
            checkbox.pack(pady=5, anchor="w")
            
            self.checkbox_vars[warehouse_id] = var
        
        # Кнопки управления
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)
        
        select_all_btn = ctk.CTkButton(button_frame, text="Выбрать все", 
                                     command=self.select_all)
        select_all_btn.pack(side="left", padx=5)
        
        clear_all_btn = ctk.CTkButton(button_frame, text="Очистить все", 
                                    command=self.clear_all)
        clear_all_btn.pack(side="left", padx=5)
        
        show_selected_btn = ctk.CTkButton(button_frame, text="Показать выбранные", 
                                        command=self.show_selected)
        show_selected_btn.pack(side="left", padx=5)
        
        # Поле для вывода результатов
        self.result_text = ctk.CTkTextbox(self, height=100)
        self.result_text.pack(pady=10, padx=20, fill="x")
    
    def on_checkbox_toggle(self, warehouse_id, warehouse_name):
        """Обрабатывает нажатие чекбокса"""
        if self.checkbox_vars[warehouse_id].get():
            self.selected_warehouses[warehouse_id] = warehouse_name
        else:
            self.selected_warehouses.pop(warehouse_id, None)
    
    def select_all(self):
        """Выбирает все склады"""
        for warehouse_id, var in self.checkbox_vars.items():
            var.set(True)
            warehouse_name = self.warehouses[warehouse_id]
            self.selected_warehouses[warehouse_id] = warehouse_name
    
    def clear_all(self):
        """Очищает все выборы"""
        for var in self.checkbox_vars.values():
            var.set(False)
        self.selected_warehouses.clear()
        self.result_text.delete("1.0", "end")
    
    def show_selected(self):
        """Показывает выбранные склады"""
        self.result_text.delete("1.0", "end")
        
        if not self.selected_warehouses:
            self.result_text.insert("1.0", "Не выбрано ни одного склада")
            return
        
        result_text = "Выбранные склады:\n"
        for warehouse_id, warehouse_name in self.selected_warehouses.items():
            result_text += f"• {warehouse_name} (ID: {warehouse_id})\n"
        
        self.result_text.insert("1.0", result_text)

# Ваши данные
warehouses_data = {
    23589573193000: 'M1',
    23906366567000: 'Гомель', 
    1020000290471000: 'B1toM1',
    1020000718625000: 'M1 Express',
    1020000859528000: 'CarsBig',
    1020000869958000: 'V11',
    1020000915891000: 'Анапа',
    1020001108294000: 'V11S',
    1020001197935000: 'Cars',
    1020001542285000: 'V11Big',
    1020001709667000: 'Красноярск',
    1020001724494000: 'Пенза',
    1020001791539000: 'Волжский',
    1020001807791000: 'СПБ_Гатчина',
    1020001824274000: 'Ростов-на-Дону',
    1020002006521000: 'Торжок',
    1020002010996000: 'Челябинск',
    1020002083071000: 'Ханты-Мансийск',
    1020005000087144: 'Воронеж',
    1020005000087158: 'Оренбург',
    1020005000090572: 'Астрахань',
    1020005000129715: 'Барнаул',
    1020005000182002: 'Уфа',
    1020005000240465: 'Пятигорск',
    1020005000653122: 'M1S',
    1020005000653289: 'M1Big'
}

if __name__ == "__main__":
    app = WarehouseApp(warehouses_data)
    app.mainloop()