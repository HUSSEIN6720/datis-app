
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from datetime import datetime
import json
import os

# تنظیم رنگ پس‌زمینه
Window.clearcolor = (0.95, 0.95, 0.95, 1)

# ============================================
# کلاس مدیریت دیتابیس (ذخیره در فایل JSON)
# ============================================
class Database:
    def __init__(self):
        self.products_file = 'products.json'
        self.production_file = 'production.json'
        self.sales_file = 'sales.json'
        self.inventory_file = 'inventory.json'
        self.purchases_file = 'purchases.json'
        self.customers_file = 'customers.json'
        
        # ایجاد فایل‌ها اگر وجود ندارن
        for file in [self.products_file, self.production_file, self.sales_file, 
                     self.inventory_file, self.purchases_file, self.customers_file]:
            if not os.path.exists(file):
                with open(file, 'w', encoding='utf-8') as f:
                    json.dump([], f)
    
    def load_data(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, filename, data):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_next_code(self, filename, prefix):
        data = self.load_data(filename)
        if not data:
            return f"{prefix}-001"
        last_code = data[-1].get('code', '')
        if last_code:
            num = int(last_code.split('-')[1]) + 1
            return f"{prefix}-{num:03d}"
        return f"{prefix}-001"

# ============================================
# صفحه اصلی (داشبورد)
# ============================================
class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # عنوان با نام داتیس
        title = Label(text='📊 داتیس - نرم‌افزار حسابداری', 
                     font_size=28, color=(0.2, 0.4, 0.6, 1),
                     size_hint_y=None, height=80)
        layout.add_widget(title)
        
        # زیرعنوان
        subtitle = Label(text='مدیریت هوشمند تولید و فروش', 
                        font_size=16, color=(0.4, 0.4, 0.4, 1),
                        size_hint_y=None, height=40)
        layout.add_widget(subtitle)
        
        # دکمه‌های منو
        buttons = [
            ('🏭 تولید روزانه', 'production'),
            ('📦 انبار', 'inventory'),
            ('💰 فروش', 'sales'),
            ('🛒 خرید', 'purchases'),
            ('📈 گزارشات', 'reports'),
            ('👥 مشتریان', 'customers'),
            ('⚙️ تنظیمات', 'settings')
        ]
        
        for text, screen_name in buttons:
            btn = Button(text=text, font_size=18, size_hint_y=None, height=55,
                        background_normal='', background_color=(0.3, 0.5, 0.8, 1),
                        color=(1, 1, 1, 1))
            btn.bind(on_press=lambda x, name=screen_name: setattr(self.manager, 'current', name))
            layout.add_widget(btn)
        
        # نسخه برنامه
        version = Label(text='نسخه 1.0.0 | داتیس', 
                       font_size=12, color=(0.6, 0.6, 0.6, 1),
                       size_hint_y=None, height=30)
        layout.add_widget(version)
        
        self.add_widget(layout)

# ============================================
# صفحه تولید روزانه
# ============================================
class ProductionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # عنوان
        layout.add_widget(Label(text='🏭 ثبت تولید روزانه - داتیس', font_size=24, size_hint_y=None, height=50))
        
        # فرم ورودی
        form = GridLayout(cols=2, spacing=10, size_hint_y=None, height=250)
        
        form.add_widget(Label(text='نوع محصول:', font_size=16))
        self.product_input = TextInput(text='', multiline=False, font_size=16)
        form.add_widget(self.product_input)
        
        form.add_widget(Label(text='تولیدکننده:', font_size=16))
        self.producer_spinner = Spinner(text='انتخاب کنید', values=['حسین', 'محمد', 'CNC'], font_size=16)
        form.add_widget(self.producer_spinner)
        
        form.add_widget(Label(text='تعداد تولید:', font_size=16))
        self.qty_input = TextInput(text='', multiline=False, font_size=16, input_filter='int')
        form.add_widget(self.qty_input)
        
        layout.add_widget(form)
        
        # دکمه ثبت
        btn_save = Button(text='✅ ثبت تولید', font_size=18, size_hint_y=None, height=50,
                         background_normal='', background_color=(0.2, 0.7, 0.3, 1))
        btn_save.bind(on_press=self.save_production)
        layout.add_widget(btn_save)
        
        # دکمه بازگشت
        btn_back = Button(text='🔙 بازگشت به داشبورد', font_size=16, size_hint_y=None, height=40,
                         background_normal='', background_color=(0.7, 0.2, 0.2, 1))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        layout.add_widget(btn_back)
        
        self.add_widget(layout)
    
    def save_production(self, instance):
        product = self.product_input.text.strip()
        producer = self.producer_spinner.text
        qty = self.qty_input.text.strip()
        
        if not product or producer == 'انتخاب کنید' or not qty:
            self.show_popup('خطا', 'لطفاً همه فیلدها را پر کنید!')
            return
        
        # ذخیره در دیتابیس
        data = self.db.load_data('production.json')
        new_record = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'product': product,
            'producer': producer,
            'quantity': int(qty)
        }
        data.append(new_record)
        self.db.save_data('production.json', data)
        
        # به‌روزرسانی انبار
        self.update_inventory(product, int(qty))
        
        self.show_popup('موفق', f'✅ تولید {product} با موفقیت ثبت شد!')
        self.product_input.text = ''
        self.qty_input.text = ''
    
    def update_inventory(self, product, qty):
        inventory = self.db.load_data('inventory.json')
        found = False
        for item in inventory:
            if item['product'] == product:
                item['quantity'] += qty
                found = True
                break
        if not found:
            inventory.append({
                'product': product,
                'quantity': qty
            })
        self.db.save_data('inventory.json', inventory)
    
    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        popup_layout.add_widget(Label(text=message, font_size=16))
        btn = Button(text='باشه', font_size=16, size_hint_y=None, height=40)
        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        btn.bind(on_press=popup.dismiss)
        popup_layout.add_widget(btn)
        popup.open()

# ============================================
# صفحه انبار
# ============================================
class InventoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        layout.add_widget(Label(text='📦 موجودی انبار - داتیس', font_size=24, size_hint_y=None, height=50))
        
        # دکمه نمایش موجودی
        btn_show = Button(text='🔄 نمایش موجودی', font_size=16, size_hint_y=None, height=40,
                         background_normal='', background_color=(0.3, 0.5, 0.8, 1))
        btn_show.bind(on_press=self.show_inventory)
        layout.add_widget(btn_show)
        
        # اسکرول ویو برای نمایش لیست
        self.scroll = ScrollView(size_hint=(1, 0.7))
        self.inventory_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.inventory_list.bind(minimum_height=self.inventory_list.setter('height'))
        self.scroll.add_widget(self.inventory_list)
        layout.add_widget(self.scroll)
        
        btn_back = Button(text='🔙 بازگشت به داشبورد', font_size=16, size_hint_y=None, height=40,
                         background_normal='', background_color=(0.7, 0.2, 0.2, 1))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        layout.add_widget(btn_back)
        
        self.add_widget(layout)
    
    def show_inventory(self, instance):
        self.inventory_list.clear_widgets()
        data = self.db.load_data('inventory.json')
        if not data:
            self.inventory_list.add_widget(Label(text='📭 انبار خالی است!', font_size=16))
            return
        
        # نمایش مجموع موجودی
        total = sum(item['quantity'] for item in data)
        self.inventory_list.add_widget(Label(
            text=f'📊 مجموع موجودی: {total} عدد',
            font_size=16, size_hint_y=None, height=35, color=(0.2, 0.5, 0.2, 1)
        ))
        self.inventory_list.add_widget(Label(text='-'*30, size_hint_y=None, height=20))
        
        for item in data:
            self.inventory_list.add_widget(Label(
                text=f"🔹 {item['product']}: {item['quantity']} عدد",
                font_size=16, size_hint_y=None, height=35
            ))

# ============================================
# صفحه فروش
# ============================================
class SalesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        layout.add_widget(Label(text='💰 ثبت فروش - داتیس', font_size=24, size_hint_y=None, height=50))
        
        form = GridLayout(cols=2, spacing=10, size_hint_y=None, height=350)
        
        form.add_widget(Label(text='محصول:', font_size=16))
        self.product_spinner = Spinner(text='انتخاب کنید', values=[], font_size=16)
        form.add_widget(self.product_spinner)
        
        form.add_widget(Label(text='مشتری:', font_size=16))
        self.customer_spinner = Spinner(text='انتخاب کنید', values=[], font_size=16)
        form.add_widget(self.customer_spinner)
        
        form.add_widget(Label(text='تعداد:', font_size=16))
        self.qty_input = TextInput(text='', multiline=False, font_size=16, input_filter='int')
        form.add_widget(self.qty_input)
        
        form.add_widget(Label(text='مبلغ (ریال):', font_size=16))
        self.price_input = TextInput(text='', multiline=False, font_size=16, input_filter='int')
        form.add_widget(self.price_input)
        
        form.add_widget(Label(text='نوع تسویه:', font_size=16))
        self.payment_spinner = Spinner(text='انتخاب کنید', values=['نقد', 'چک', 'حواله', 'اعتباری'], font_size=16)
        form.add_widget(self.payment_spinner)
        
        layout.add_widget(form)
        
        # دکمه ثبت فروش
        btn_save = Button(text='✅ ثبت فروش', font_size=18, size_hint_y=None, height=50,
                         background_normal='', background_color=(0.2, 0.7, 0.3, 1))
        btn_save.bind(on_press=self.save_sales)
        layout.add_widget(btn_save)
        
        # دکمه بازگشت
        btn_back = Button(text='🔙 بازگشت به داشبورد', font_size=16, size_hint_y=None, height=40,
                         background_normal='', background_color=(0.7, 0.2, 0.2, 1))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        layout.add_widget(btn_back)
        
        # بارگذاری لیست محصولات و مشتریان
        self.load_spinners()
        self.add_widget(layout)
    
    def load_spinners(self):
        # بارگذاری محصولات از انبار
        inventory = self.db.load_data('inventory.json')
        products = [item['product'] for item in inventory if item['quantity'] > 0]
        if products:
            self.product_spinner.values = products
            self.product_spinner.text = products[0] if products else 'انتخاب کنید'
        
        # بارگذاری مشتریان
        customers = self.db.load_data('customers.json')
        customer_names = [c.get('name', '') for c in customers if c.get('name')]
        if customer_names:
            self.customer_spinner.values = customer_names
            self.customer_spinner.text = customer_names[0] if customer_names else 'انتخاب کنید'
    
    def save_sales(self, instance):
        product = self.product_spinner.text
        customer = self.customer_spinner.text
        qty = self.qty_input.text.strip()
        price = self.price_input.text.strip()
        payment = self.payment_spinner.text
        
        if product == 'انتخاب کنید' or customer == 'انتخاب کنید' or not qty or not price or payment == 'انتخاب کنید':
            self.show_popup('خطا', 'لطفاً همه فیلدها را پر کنید!')
            return
        
        # کم کردن از موجودی
        inventory = self.db.load_data('inventory.json')
        found = False
        for item in inventory:
            if item['product'] == product:
                if item['quantity'] >= int(qty):
                    item['quantity'] -= int(qty)
                    found = True
                    break
                else:
                    self.show_popup('خطا', f'❗ موجودی کافی نیست! فقط {item["quantity"]} عدد موجود است.')
                    return
        
        if not found:
            self.show_popup('خطا', '❗ محصول در انبار موجود نیست!')
            return
        
        self.db.save_data('inventory.json', inventory)
        
        # ثبت در فروش
        sales = self.db.load_data('sales.json')
        sales.append({
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'product': product,
            'customer': customer,
            'quantity': int(qty),
            'price': int(price),
            'total': int(qty) * int(price),
            'payment': payment
        })
        self.db.save_data('sales.json', sales)
        
        self.show_popup('موفق', f'✅ فروش {product} به {customer} با موفقیت ثبت شد!')
        self.qty_input.text = ''
        self.price_input.text = ''
    
    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        popup_layout.add_widget(Label(text=message, font_size=16))
        btn = Button(text='باشه', font_size=16, size_hint_y=None, height=40)
        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        btn.bind(on_press=popup.dismiss)
        popup_layout.add_widget(btn)
        popup.open()

# ============================================
# کلاس اصلی برنامه
# ============================================
class DatisApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(ProductionScreen(name='production'))
        sm.add_widget(InventoryScreen(name='inventory'))
        sm.add_widget(SalesScreen(name='sales'))
        # صفحات دیگه رو می‌تونی اضافه کنی
        return sm
    
    def on_start(self):
        # ایجاد فایل‌های مورد نیاز در شروع
        db = Database()

if __name__ == '__main__':
    DatisApp().run()
