from tkinter import * 
from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk  # เพิ่มนี้เพื่อใช้ในการย่อขนาดรูปภาพ

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('925x500+300+200')
        self.title('ระบบจัดการเงิน')
        self.resizable(False,False)

        self.navbar_frame = tk.Frame(self, bg="#333",height=50)
        self.navbar_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.shop_button = tk.Button(self.navbar_frame,bg="#333",border=0,font=('Browallia',14),fg='white', text="ร้านค้า 1", command=lambda: self.select_frame_by_name("shop"))
        self.shop_button.pack(side=tk.LEFT, padx=10,pady=5)

        self.point_button = tk.Button(self.navbar_frame,bg="#333",border=0,font=('Browallia',14),fg='white', text="แลกพ้อย", command=lambda: self.select_frame_by_name("point"))
        self.point_button.pack(side=tk.LEFT, padx=10,pady=5)

        self.profile_button = tk.Button(self.navbar_frame,bg="#333",border=0,font=('Browallia',14),fg='white', text="โปรไฟล์", command=lambda: self.select_frame_by_name("profile"))
        self.profile_button.pack(side=tk.LEFT, padx=10,pady=5)

        self.topup_button = tk.Button(self.navbar_frame,bg="#333",border=0,font=('Browallia',14),fg='white', text="เติมเงิน", command=lambda: self.select_frame_by_name("topup"))
        self.topup_button.pack(side=tk.LEFT, padx=10,pady=5)

        self.logout_button = tk.Button(self.navbar_frame,bg="#333",border=0,font=('Browallia',14),fg='white', text="ออกจากระบบ", command=lambda: self.select_frame_by_name("login"))
        self.logout_button.pack(side=tk.RIGHT, padx=10,pady=5)

        #=================================================หน้า login=====================================================#

        self.login_frame = tk.Frame(self,bg="green")

        self.login_label_frame = tk.Frame(self.login_frame,width=925/2,height=500,bg='white')
        self.login_label_frame.pack(side=tk.RIGHT)

        self.login_label = tk.Label(self.login_label_frame,text="แสกนบัตรเพื่อเข้าสู่ระบบ",font=('Browallia New',16),bg='white')
        self.login_label.place(x=150,y=130)

        self.login_scancard_btn = tk.Button(self.login_label_frame,text="แสกนบัตร",bg="#FFBF00",fg="white",width=10,height=1,border=0,font=('Browallia New',15,'bold'))
        self.login_scancard_btn.place(x=180,y=220)

        self.login_label = tk.Label(self.login_label_frame,text="คุณยังไม่ได้สมัครสมาชิก?",font=('Browallia New',16),bg='white')
        self.login_label.place(x=105,y=320)

        self.signup_label = Button(self.login_label_frame,text='สมัครสมาชิก',bg='white',cursor='hand2',fg='#57a1f8',border=0, command=lambda: self.select_frame_by_name("register"),font=('Browallia New',16))
        self.signup_label.place(x=260,y=315)

        self.login_logo_frame = tk.Frame(self.login_frame,width=925/2,height=500,bg='white')
        self.login_logo_frame.pack(side=tk.LEFT)
        img = Image.open('logo.png')
        img = img.resize((300, 300))
        img = ImageTk.PhotoImage(img)
        img_label = Label(self.login_logo_frame, image=img, bg='white')
        img_label.image = img  # เก็บอ้างอิงภาพเพื่อป้องกันการลบไปโดยอัตโนมัติ
        img_label.place(x=155, y=90)

        #=================================================จบ login=====================================================#

        #=================================================หน้า register=====================================================#

        self.register_frame = tk.Frame(self,bg="white")

        self.register_logo_frame = tk.Frame(self.register_frame,width=925/2,height=500,bg='white')
        self.register_logo_frame.pack(side=tk.LEFT)
        img = Image.open('logo.png')
        img = img.resize((300, 300))
        img = ImageTk.PhotoImage(img)
        img_label = Label(self.register_logo_frame, image=img, bg='white')
        img_label.image = img  # เก็บอ้างอิงภาพเพื่อป้องกันการลบไปโดยอัตโนมัติ
        img_label.place(x=155, y=90)


        self.register_label_frame = tk.Frame(self.register_frame,width=925/2,height=500,bg='white')
        self.register_label_frame.pack(side=tk.TOP)

        self.register_label = tk.Label(self.register_label_frame,text="สมัครสมาชิก",font=('Browallia New',20,'bold'),bg='white')
        self.register_label.place(x=160,y=70)

        self.register_number_input = tk.Entry(self.register_label_frame,width=32,fg='black',border=0,bg="#fff",font=('Browallia New',18))
        self.register_number_input.place(x=77,y=120)
        self.register_number_input.insert(0,'กรุณากรอกรหัสนิสิต')
        tk.Frame(self.register_label_frame,width=295,height=2,bg='black').place(x=78,y=153)

        self.register_user_input = tk.Entry(self.register_label_frame,width=32,fg='black',border=0,bg="#fff",font=('Browallia New',18))
        self.register_user_input.place(x=77,y=170)
        self.register_user_input.insert(0,'กรุณากรอก username')
        tk.Frame(self.register_label_frame,width=295,height=2,bg='black').place(x=78,y=203)

        self.register_label_2 = tk.Label(self.register_label_frame,text="ไม่ต้องกรอก @.ku.th",font=('Browallia New',12,'bold'),bg='white',fg='red')
        self.register_label_2.place(x=260,y=190)

        self.register_fname_input = tk.Entry(self.register_label_frame,width=32,fg='black',border=0,bg="#fff",font=('Browallia New',18))
        self.register_fname_input.place(x=77,y=220)
        self.register_fname_input.insert(0,'กรุณากรอกชื่อ')
        tk.Frame(self.register_label_frame,width=295,height=2,bg='black').place(x=78,y=253)

        self.register_lname_input = tk.Entry(self.register_label_frame,width=32,fg='black',border=0,bg="#fff",font=('Browallia New',18))
        self.register_lname_input.place(x=77,y=270)
        self.register_lname_input.insert(0,'กรุณากรอกนามสกุล')
        tk.Frame(self.register_label_frame,width=295,height=2,bg='black').place(x=78,y=303)

        self.register_lname_input = tk.Label(self.register_label_frame,width=32,text="ข้อมูล Card ID : ",fg='black',border=0,bg="#fff",font=('Browallia New',18))
        self.register_lname_input.place(x=0,y=315)

        self.register_scancard_btn = tk.Button(self.register_label_frame,text="แสกนบัตร",bg="#FFBF00",fg="white",width=10,height=1,border=0,font=('Browallia New',15,'bold'))
        self.register_scancard_btn.place(x=288,y=315)

        self.register_button_submit = tk.Button(self.register_label_frame,text="สมัครสมาชิก",bg="#4C956C",fg="white",width=13,height=1,border=0,font=('Browallia New',15,'bold'))
        self.register_button_submit.place(x=75,y=360)

        self.register_button_back = tk.Button(self.register_label_frame,text="ยกเลิก",bg="#D82F2F",fg="white",width=13,height=1,border=0,font=('Browallia New',15,'bold'),command=lambda: self.select_frame_by_name("login"))
        self.register_button_back.place(x=265,y=360)


        #=================================================จบ register=====================================================#

        #=================================================หน้า ร้านค้า=====================================================#
        self.products = [
            {"name": "เข็มขัด", "price": 50},
            {"name": "เสื้อ", "price": 30},
            {"name": "กางเกง", "price": 30},
            {"name": "2", "price": 30},
            {"name": "เ3ข็มขัด", "price": 30},
            {"name": "เข็4มขัด", "price": 30},
            {"name": "เข็ม5ขัด", "price": 30},
            {"name": "5", "price": 30},
            {"name": "เข็ม52ขัด", "price": 30},
            {"name": "เข็ม53ขัด", "price": 30},
        ]

        self.shopping_cart = []

        self.shop_frame = tk.Frame(self, bg="white")

        self.shop_menu_frame = tk.Frame(self.shop_frame, bg='white', width=650, height=500)
        self.shop_menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(self.shop_menu_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas for products
        self.canvas = tk.Canvas(self.shop_menu_frame, yscrollcommand=scrollbar.set, bg='white', width=650, height=500)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        # Frame to contain the products
        self.products_frame = tk.Frame(self.canvas, bg='white')
        self.canvas.create_window((0, 0), window=self.products_frame, anchor=tk.NW)

        self.display_products()

        # Configure canvas to update scroll region
        self.products_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Shop Cart Frame
        self.shop_cart_frame = tk.Frame(self.shop_frame, width=275, height=500, bg='#D9D9D9')
        self.shop_cart_frame.pack(side=tk.RIGHT)
        
        # เพิ่ม Scrollbar
        cart_scrollbar = tk.Scrollbar(self.shop_cart_frame, orient=tk.VERTICAL)
        cart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # สร้าง Canvas ใน shop_cart_frame
        cart_canvas = tk.Canvas(self.shop_cart_frame, yscrollcommand=cart_scrollbar.set, bg='#D9D9D9', width=275, height=500)
        cart_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # สร้าง Frame ภายใน Canvas เพื่อใส่ข้อมูลในตะกร้า
        cart_items_frame = tk.Frame(cart_canvas, bg='#D9D9D9')
        cart_canvas.create_window((0, 0), window=cart_items_frame, anchor=tk.NW)

        # เชื่อมต่อ Scrollbar กับ Canvas
        cart_scrollbar.config(command=cart_canvas.yview)

        self.shop_label_2 = tk.Label(self.shop_cart_frame, text="รถเข็น", font=('Browallia New', 20, 'bold'), fg='black', bg='#D9D9D9')
        self.shop_label_2.place(x=100, y=0)
                
        #=================================================จบ ร้านค้า=====================================================#

        #=================================================หน้า แลกของ=====================================================#
        self.point_products = [
            {"name": "เข็มขัด", "point": 5},
            {"name": "เสื้อ", "point": 5},
            {"name": "กางเกง", "point": 5},
            {"name": "เข็มขัด", "point": 5},
            {"name": "เข็มขัด", "point": 5},
            {"name": "เข็มขัด", "point": 5},
            {"name": "เข็มขัด", "point": 5},   
        ]

        self.shopping_cart_point = []

        self.point_frame = tk.Frame(self,bg="white")

        self.point_menu_frame = tk.Frame(self.point_frame, bg='white', width=650, height=500)
        self.point_menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_point = tk.Scrollbar(self.point_menu_frame, orient=tk.VERTICAL)
        scrollbar_point.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_point = tk.Canvas(self.point_menu_frame, yscrollcommand=scrollbar_point.set, bg='white', width=650, height=500)
        self.canvas_point.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_point.config(command=self.canvas_point.yview)

        self.product_point_frame = tk.Frame(self.canvas_point, bg='white')
        self.canvas_point.create_window((0, 0), window=self.product_point_frame, anchor=tk.NW)

        self.display_points()   

        self.product_point_frame.update_idletasks()
        self.canvas_point.config(scrollregion=self.canvas_point.bbox("all"))

        self.point_kart_frame = tk.Frame(self.point_frame,width=275,height=500,bg='#D9D9D9')
        self.point_kart_frame.pack(side=tk.RIGHT)

        self.point_label_2 = tk.Label(self.point_kart_frame, text="รถเข็น", font=('Browallia New', 20, 'bold'), fg='black', bg='#D9D9D9')
        self.point_label_2.place(x=100, y=0)

        #=================================================จบ แลกของ=====================================================#

        #=================================================หน้า โปรไฟล์=====================================================

        self.profile_frame = tk.Frame(self,bg="white")

        self.profile_logo_frame = tk.Frame(self.profile_frame,width=925/2,height=500,bg='white')
        self.profile_logo_frame.pack(side=tk.LEFT)
        img = Image.open('logo.png')
        img = img.resize((300, 300))
        img = ImageTk.PhotoImage(img)
        img_label = Label(self.profile_logo_frame, image=img, bg='white')
        img_label.image = img  # เก็บอ้างอิงภาพเพื่อป้องกันการลบไปโดยอัตโนมัติ
        img_label.place(x=155, y=70)

        self.profile_label_frame = tk.Frame(self.profile_frame,width=925/2,height=500,bg='white')
        self.profile_label_frame.pack(side=tk.TOP)

        self.profile_name = tk.Label(self.profile_label_frame,text="ชื่อ : ",font=('Browallia New',20,'bold'),fg='black',bg='white')
        self.profile_name.place(x=120,y=150)

        self.profile_money = tk.Label(self.profile_label_frame,text="เงินคงเหลือ : ",font=('Browallia New',20,'bold'),fg='black',bg='white')
        self.profile_money.place(x=120,y=210)

        self.profile_point = tk.Label(self.profile_label_frame,text="พ้อย : ",font=('Browallia New',20,'bold'),fg='black',bg='white')
        self.profile_point.place(x=120,y=270)

        #=================================================จบ โปรไฟล์=====================================================#

        #=================================================หน้า เติมเงิน=====================================================#
        self.topup_frame = tk.Frame(self,bg="white")

        self.topup_label_frame = tk.Frame(self.topup_frame,width=925,height=500,bg='white')
        self.topup_label_frame.pack(side=tk.TOP)

        self.topup_label = tk.Label(self.topup_label_frame,text="เติมเงิน",font=('Browallia New',20,'bold'),fg='black',bg='white')
        self.topup_label.place(x=440,y=0)

        self.topup_scancard_btn = tk.Button(self.topup_label_frame,text="แสกนบัตร",bg="#FFBF00",fg="white",width=10,height=1,border=0,font=('Browallia New',15,'bold'))
        self.topup_scancard_btn.place(x=650,y=95)

        self.topup_num = tk.Label(self.topup_label_frame,text="รหัสนิสิต : ",font=('Browallia New',20),fg='black',bg='white')
        self.topup_num.place(x=520,y=145)

        self.topup_name = tk.Label(self.topup_label_frame,text="ชื่อ : ",font=('Browallia New',20),fg='black',bg='white')
        self.topup_name.place(x=520,y=185)

        self.topup_money = tk.Label(self.topup_label_frame,text="เงินคงเหลือ : ",font=('Browallia New',20),fg='black',bg='white')
        self.topup_money.place(x=520,y=225)

        self.topup_point = tk.Label(self.topup_label_frame,text="พ้อยคงเหลือ : ",font=('Browallia New',20),fg='black',bg='white')
        self.topup_point.place(x=520,y=265)


        self.topup_user_input = tk.Entry(self.topup_label_frame,width=32,fg='black',border=0,bg="#fff",font=('Browallia New',18))
        self.topup_user_input.place(x=127,y=160)
        self.topup_user_input.insert(0,'กรุณากรอกจำนวนเงินที่ต้องการเติม')
        tk.Frame(self.topup_label_frame,width=255,height=2,bg='black').place(x=128,y=193)

        self.topup_button_submit = tk.Button(self.topup_label_frame,text="เติมเงิน",bg="#4C956C",fg="white",width=13,height=1,border=0,font=('Browallia New',15,'bold'))
        self.topup_button_submit.place(x=195,y=230)

        #=================================================จบ เติมเงิน=====================================================#
    
        self.select_frame_by_name("shop")

    def select_frame_by_name(self, name):
        if name == "login" or name == "register":
            self.navbar_frame.pack_forget()
            self.navbar_frame.place_forget()
            self.navbar_frame.grid_forget()
        else:
            self.navbar_frame.pack(side=tk.BOTTOM, fill=tk.X)

        if name == "login":
            self.login_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.login_frame.pack_forget()
            self.login_frame.place_forget()
            self.login_frame.grid_forget()
        if name == "register":
            self.register_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.register_frame.pack_forget()
            self.register_frame.place_forget()
            self.register_frame.grid_forget()
        if name == "shop" :
            self.shop_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.shop_frame.pack_forget()
            self.shop_frame.place_forget()
            self.shop_frame.grid_forget()
        if name == "point" :
            self.point_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.point_frame.pack_forget()
            self.point_frame.place_forget()
            self.point_frame.grid_forget()
        if name == "profile" :
            self.profile_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.profile_frame.pack_forget()
            self.profile_frame.place_forget()
            self.profile_frame.grid_forget()
        if name == "topup" :
            self.topup_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.topup_frame.pack_forget()
            self.topup_frame.place_forget()
            self.topup_frame.grid_forget()
    
    def display_products(self):
        # Loop through the products and create a widget for each
        for idx, product in enumerate(self.products):
            product_frame = tk.Frame(self.products_frame, bg='white')
            product_frame.grid(row=idx // 5, column=idx % 5, padx=20, pady=20)

            # Product name
            name_label = tk.Label(product_frame, text=product["name"], font=('Browallia New', 12), bg='white')
            name_label.grid(row=0, column=1, padx=10)

            # Product price
            price_label = tk.Label(product_frame, text=f"ราคา : {product['price']} บาท", font=('Browallia New', 12), bg='white')
            price_label.grid(row=1, column=1, padx=10)

            # Add to cart button
            add_to_cart_button = tk.Button(product_frame, text="Add to Cart", bg="#4C956C", fg="white", width=10, height=1, border=0, font=('Browallia New', 10, 'bold'), command=lambda product=product: self.add_to_cart(product))
            add_to_cart_button.grid(row=2, column=1, padx=10)


    def display_cart(self):
        # Clear existing widgets in the shop_cart_frame
        for widget in self.shop_cart_frame.winfo_children():
            widget.destroy()

        cart_counts = {}  # Dictionary to keep track of the quantity of each item in the cart
        total_cost = 0

        # Count the quantity of each item in the cart and calculate the total cost
        for product in self.shopping_cart:
            total_cost += product["price"]
            if product["name"] in cart_counts:
                cart_counts[product["name"]] += 1
            else:
                cart_counts[product["name"]] = 1

        # Display the items in the shopping cart with quantities
        for idx, (product_name, quantity) in enumerate(cart_counts.items()):
            cart_item_frame = tk.Frame(self.shop_cart_frame, bg='#D9D9D9')
            cart_item_frame.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

            # Product name with quantity
            name_label = tk.Label(cart_item_frame, text=f"{product_name} x{quantity}", font=('Browallia New', 12), bg='#D9D9D9')
            name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

            remove_button = tk.Button(cart_item_frame, text="Remove", bg="red", fg="white", width=8, height=1, border=0, font=('Browallia New', 10, 'bold'), command=lambda product_name=product_name: self.remove_from_cart(product_name))
            remove_button.grid(row=0, column=1, padx=5)

        # Display the total cost
        total_label = tk.Label(self.shop_cart_frame, text=f"รวมทั้งหมด: {total_cost} บาท", font=('Browallia New', 14, 'bold'), bg='#D9D9D9')
        total_label.grid(row=len(cart_counts), column=0, padx=10, pady=10, sticky="e")

        # Add a confirm button
        confirm_button = tk.Button(self.shop_cart_frame, text="ยืนยันการซื้อ", bg="#4C956C", fg="white", width=15, height=1, border=0, font=('Browallia New', 12, 'bold'), command=self.confirm_purchase)
        confirm_button.grid(row=len(cart_counts) + 1, column=0, padx=30, pady=10, sticky="e")

    def confirm_purchase(self):
        
        # Add your logic for confirming the purchase here
        # For example, you can show a messagebox or perform further actions
        messagebox.showinfo("Confirmation", "การซื้อของได้รับการยืนยัน!")

        # Clear the shopping cart after confirmation
        self.shopping_cart.clear()

        # Update the displayed cart
        self.display_cart()

    def add_to_cart(self, product):
        # Add the product to the shopping cart
        self.shopping_cart.append(product)

        # Display the items in the shopping cart
        self.display_cart()

    def remove_from_cart(self, product_name):
        # Remove the item from the shopping cart
        for idx, product in enumerate(self.shopping_cart):
            if product["name"] == product_name:
                del self.shopping_cart[idx]
                break

        # Display the updated shopping cart
        self.display_cart()

    def display_points(self):
        # Clear existing widgets in the product_point_frame
        for widget in self.product_point_frame.winfo_children():
            widget.destroy()

        # Loop through the point products and create a widget for each
        for idx, product in enumerate(self.point_products):
            product_point_frame = tk.Frame(self.product_point_frame, bg='white')
            product_point_frame.grid(row=idx // 5, column=idx % 5, padx=17, pady=20)

            # Product name
            name_label = tk.Label(product_point_frame, text=product["name"], font=('Browallia New', 12), bg='white')
            name_label.grid(row=0, column=1, padx=5)

            # Product points
            points_label = tk.Label(product_point_frame, text=f"แลกแต้ม : {product['point']} แต้ม", font=('Browallia New', 12), bg='white')
            points_label.grid(row=1, column=1, padx=5)

            # Add to cart button
            add_to_cart_button = tk.Button(product_point_frame, text="ใส่รถเข็น", bg="#4C956C", fg="white", width=10, height=1, border=0, font=('Browallia New', 10, 'bold'), command=lambda product=product: self.add_to_cart_point(product))
            add_to_cart_button.grid(row=2, column=1, padx=5)
    
    def display_cart_point(self):
        # Clear existing widgets in the point_kart_frame
        for widget in self.point_kart_frame.winfo_children():
            widget.destroy()

        cart_counts = {}  # Dictionary to keep track of the quantity of each item in the cart
        total_points = 0

        # Count the quantity of each item in the cart and calculate the total points
        for point_products in self.shopping_cart_point:
            total_points += point_products["point"]
            if point_products["name"] in cart_counts:
                cart_counts[point_products["name"]] += 1
            else:
                cart_counts[point_products["name"]] = 1

        # Display the items in the shopping cart with quantities
        for idx, (product_name, quantity) in enumerate(cart_counts.items()):
            cart_item_frame = tk.Frame(self.point_kart_frame, bg='#D9D9D9')
            cart_item_frame.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

            # Product name with quantity
            name_label = tk.Label(cart_item_frame, text=f"{product_name} x{quantity}", font=('Browallia New', 12), bg='#D9D9D9')
            name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

            remove_button = tk.Button(cart_item_frame, text="Remove", bg="red", fg="white", width=8, height=1, border=0, font=('Browallia New', 10, 'bold'), command=lambda product_name=product_name: self.remove_from_cart_point(product_name))
            remove_button.grid(row=0, column=1, padx=5)

        # Display the total points
        total_label = tk.Label(self.point_kart_frame, text=f"รวมทั้งหมด: {total_points} แต้ม", font=('Browallia New', 14, 'bold'), bg='#D9D9D9')
        total_label.grid(row=len(cart_counts), column=0, padx=10, pady=10, sticky="e")

        input_otp_point = tk.Entry(self.point_kart_frame,width=7,fg='black',border=0,bg="#fff",font=('Browallia New',18))
        input_otp_point.grid(row=len(cart_counts) + 1, column=0, padx=50, pady=10, sticky="e")

        otp_need_label = tk.Label(self.point_kart_frame,text="กรุณาใส่ otp",fg='red',border=0,bg='#D9D9D9',font=('Browallia New',14))
        otp_need_label.grid(row=len(cart_counts) + 2, column=0, padx=50, pady=10, sticky="e")

        # Add a confirm button
        confirm_button = tk.Button(self.point_kart_frame, text="ชำระ", bg="#4C956C", fg="white", width=15, height=1, border=0, font=('Browallia New', 12, 'bold'), command=self.confirm_purchase_point)
        confirm_button.grid(row=len(cart_counts) + 3, column=0, padx=30, pady=10, sticky="e")


    def confirm_purchase_point(self):
        # Add your logic for confirming the point redemption here
        # For example, you can show a messagebox or perform further actions
        messagebox.showinfo("Confirmation", "การแลกของได้รับการยืนยัน!")

        # Clear the shopping cart after confirmation
        self.shopping_cart.clear()

        # Update the displayed cart
        self.display_cart_point()

    def add_to_cart_point(self, product):
        # Add the product to the shopping cart
        self.shopping_cart_point.append(product)

        # Display the items in the shopping cart
        self.display_cart_point()

    def remove_from_cart_point(self, product_name):
        # Remove the item from the shopping cart
        for idx, product in enumerate(self.shopping_cart_point):
            if product["name"] == product_name:
                del self.shopping_cart_point[idx]
                break

        # Display the updated shopping cart
        self.display_cart_point()

if __name__ == "__main__":
    app = App()
    app.mainloop()