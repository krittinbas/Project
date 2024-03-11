from tkinter import * 
from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk
import json
from NCF import NFC_Reader
import smtplib
import random

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.geometry('925x500+300+200')
        self.title('ระบบจัดการเงิน')
        self.resizable(False,False)
        
        self.otp = 0

        shops = ["ร้านค้า1", "ร้านค้า2"]

        self.navbar_frame = tk.Frame(self, bg="#333",height=50)
        self.navbar_frame.pack(side=tk.BOTTOM, fill=tk.X)

        for shop_name in shops:
            shop_button = tk.Button(self.navbar_frame, bg="#333", border=0, font=('Browallia', 14), fg='white', text=shop_name, command=lambda shop_name=shop_name: self.select_frame_by_name(shop_name.lower()))
            shop_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.point_button = tk.Button(self.navbar_frame,bg="#333",border=0,font=('Browallia',14),fg='white', text="แลกพ้อย", command=lambda: self.select_frame_by_name("point"))
        self.point_button.pack(side=tk.LEFT, padx=10,pady=5)

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

        self.login_scancard_btn = tk.Button(self.login_label_frame,text="แสกนบัตร",bg="#FFBF00",fg="white",width=10,height=1,border=0,font=('Browallia New',15,'bold'), command=lambda:self.login(uid))
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
        self.register_label.place(x=160,y=20)

        self.register_number_input = tk.Entry(self.register_label_frame,width=32,fg='black',border=0,bg="#fff",font=('Browallia New',18))
        self.register_number_input.place(x=77,y=70)
        self.register_number_input.insert(0,'กรุณากรอกรหัสนิสิต')
        tk.Frame(self.register_label_frame,width=295,height=2,bg='black').place(x=78,y=103)
        self.register_number_input.bind('<FocusIn>', self.on_enter_reg_num)
        self.register_number_input.bind('<FocusOut>', self.on_leave_reg_num)

        self.register_user_input = tk.Entry(self.register_label_frame,width=32,fg='black',border=0,bg="#fff",font=('Browallia New',18))
        self.register_user_input.place(x=77,y=120)
        self.register_user_input.insert(0,'กรุณากรอก email')
        tk.Frame(self.register_label_frame,width=295,height=2,bg='black').place(x=78,y=153)
        self.register_user_input.bind('<FocusIn>', self.on_enter_reg_user)
        self.register_user_input.bind('<FocusOut>', self.on_leave_reg_user)

        self.register_fname_input = tk.Entry(self.register_label_frame,width=32,fg='black',border=0,bg="#fff",font=('Browallia New',18))
        self.register_fname_input.place(x=77,y=170)
        self.register_fname_input.insert(0,'กรุณากรอกชื่อ')
        tk.Frame(self.register_label_frame,width=295,height=2,bg='black').place(x=78,y=203)
        self.register_fname_input.bind('<FocusIn>', self.on_enter_reg_fname)
        self.register_fname_input.bind('<FocusOut>', self.on_leave_reg_fname)

        self.register_lname_input = tk.Entry(self.register_label_frame,width=32,fg='black',border=0,bg="#fff",font=('Browallia New',18))
        self.register_lname_input.place(x=77,y=220)
        self.register_lname_input.insert(0,'กรุณากรอกนามสกุล')
        tk.Frame(self.register_label_frame,width=295,height=2,bg='black').place(x=78,y=253)
        self.register_lname_input.bind('<FocusIn>', self.on_enter_reg_lname)
        self.register_lname_input.bind('<FocusOut>', self.on_leave_reg_lname)

        self.register_idcard_label = tk.Label(self.register_label_frame,width=32,text="ข้อมูล Card ID : ",fg='black',border=0,bg="#fff",font=('Browallia New',18))
        self.register_idcard_label.place(x=0,y=265)

        self.register_scancard_btn = tk.Button(self.register_label_frame,text="แสกนบัตร",bg="#FFBF00",fg="white",width=10,height=1,border=0,font=('Browallia New',15,'bold'),command=lambda: self.scan_card_for_reg(uid))
        self.register_scancard_btn.place(x=288,y=265)
        
        self.register_otp_input = tk.Entry(self.register_label_frame,width=32,fg='black',border=0,bg="#fff",font=('Browallia New',18))
        self.register_otp_input.place(x=77,y=330)
        self.register_otp_input.insert(0,'กรุณากรอก OTP')
        tk.Frame(self.register_label_frame,width=295,height=2,bg='black').place(x=78,y=363)
        self.register_otp_input.bind('<FocusIn>', self.on_enter_otp)
        self.register_otp_input.bind('<FocusOut>', self.on_leave_otp)
        
        self.get_otp_button = tk.Button(self.register_label_frame, text="ขอ OTP", bg="#ffa500", fg="white", width=10, height=1, border=0, font=('Browallia New', 12, 'bold'), command=self.send_email_with_otp)
        self.get_otp_button.place(x=305, y=330)


        self.register_button_submit = tk.Button(self.register_label_frame, text="สมัครสมาชิก", bg="#4C956C", fg="white", width=13, height=1, border=0, font=('Browallia New', 15, 'bold'), command=lambda: self.verify_otp(uid))
        self.register_button_submit.place(x=75,y=390)

        self.register_button_back = tk.Button(self.register_label_frame,text="ยกเลิก",bg="#D82F2F",fg="white",width=13,height=1,border=0,font=('Browallia New',15,'bold'),command=lambda: self.select_frame_by_name("login"))
        self.register_button_back.place(x=265,y=390)


        #=================================================จบ register=====================================================#

        #=================================================หน้า ร้านค้า=====================================================#
        self.products = [
            {"name": "เข็มขัด", "price": 30},
            {"name": "เสื้อ", "price": 30},
            {"name": "กางเกง", "price": 30 },
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

        scrollbar = tk.Scrollbar(self.shop_menu_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self.shop_menu_frame, yscrollcommand=scrollbar.set, bg='white', width=650, height=500)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        self.products_frame = tk.Frame(self.canvas, bg='white')
        self.canvas.create_window((0, 0), window=self.products_frame, anchor=tk.NW)

        self.display_products()

        self.products_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.shop_cart_frame = tk.Frame(self.shop_frame, width=275, height=500, bg='#D9D9D9')
        self.shop_cart_frame.pack(side=tk.RIGHT)
        
        cart_scrollbar = tk.Scrollbar(self.shop_cart_frame, orient=tk.VERTICAL)
        cart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        cart_canvas = tk.Canvas(self.shop_cart_frame, yscrollcommand=cart_scrollbar.set, bg='#D9D9D9', width=275, height=500)
        cart_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        cart_items_frame = tk.Frame(cart_canvas, bg='#D9D9D9')
        cart_canvas.create_window((0, 0), window=cart_items_frame, anchor=tk.NW)

        cart_scrollbar.config(command=cart_canvas.yview)

        self.shop_label_2 = tk.Label(self.shop_cart_frame, text="รถเข็น", font=('Browallia New', 20, 'bold'), fg='black', bg='#D9D9D9')
        self.shop_label_2.place(x=100, y=0)
                
        #=================================================จบ ร้านค้า=====================================================#

        #=================================================หน้า ร้านค้า2=====================================================#

        self.products_shop2 = [
            {"name": "สินค้า1", "price": 50, "point" : 5},
            {"name": "สินค้า2", "price": 50 , "point" : 5},
            {"name": "สินค้า3", "price": 50 , "point" : 5},
            {"name": "สินค้า4", "price": 50 , "point" : 5},
            {"name": "สินค้า5", "price": 50 , "point" : 5},
            {"name": "สินค้า6", "price": 50 , "point" : 5},
            {"name": "สินค้า7", "price": 50 , "point" : 5},
            {"name": "สินค้า8", "price": 50 , "point" : 5},
            {"name": "สินค้า9", "price": 50 , "point" : 5},
            {"name": "สินค้า10", "price": 50 , "point" : 5},
        ]

        self.shopping_cart2 = []

        self.shop_frame2 = tk.Frame(self, bg="white")

        self.shop_menu_frame2 = tk.Frame(self.shop_frame2, bg='white', width=650, height=500)
        self.shop_menu_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_shop2 = tk.Scrollbar(self.shop_menu_frame2, orient=tk.VERTICAL)
        scrollbar_shop2.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_shop2 = tk.Canvas(self.shop_menu_frame2, yscrollcommand=scrollbar_shop2.set, bg='white', width=650, height=500)
        self.canvas_shop2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_shop2.config(command=self.canvas_shop2.yview)

        self.products_frame_shop2 = tk.Frame(self.canvas_shop2, bg='white')
        self.canvas_shop2.create_window((0, 0), window=self.products_frame_shop2, anchor=tk.NW)

        self.display_products_shop2()

        self.products_frame_shop2.update_idletasks()
        self.canvas_shop2.config(scrollregion=self.canvas_shop2.bbox("all"))

        self.shop_cart_frame2 = tk.Frame(self.shop_frame2, width=275, height=500, bg='#D9D9D9')
        self.shop_cart_frame2.pack(side=tk.RIGHT)

        cart_scrollbar_shop2 = tk.Scrollbar(self.shop_cart_frame2, orient=tk.VERTICAL)
        cart_scrollbar_shop2.pack(side=tk.RIGHT, fill=tk.Y)

        cart_canvas_shop2 = tk.Canvas(self.shop_cart_frame2, yscrollcommand=cart_scrollbar_shop2.set, bg='#D9D9D9', width=275, height=500)
        cart_canvas_shop2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        cart_items_frame_shop2 = tk.Frame(cart_canvas_shop2, bg='#D9D9D9')
        cart_canvas_shop2.create_window((0, 0), window=cart_items_frame_shop2, anchor=tk.NW)

        cart_scrollbar_shop2.config(command=cart_canvas_shop2.yview)

        self.shop_label_22 = tk.Label(self.shop_cart_frame2, text="รถเข็น", font=('Browallia New', 20, 'bold'), fg='black', bg='#D9D9D9')
        self.shop_label_22.place(x=100, y=0)

        #=================================================จบ ร้านค้า=====================================================#
        #=================================================หน้า แลกของ=====================================================#
        self.point_products = [
            {"shop" : "ร้านค้า 1","name": "เข็มขัด", "point": 5},
            {"shop" : "ร้านค้า 1","name": "เสื้อ", "point": 5},
            {"shop" : "ร้านค้า 1","name": "กางเกง", "point": 5},
            {"shop" : "ร้านค้า 1","name": "เข็มขัด", "point": 5},
            {"shop" : "ร้านค้า 1","name": "เข็มขัด", "point": 5},
            {"shop" : "ร้านค้า 2","name": "เข็มขัด", "point": 5},
            {"shop" : "ร้านค้า 2","name": "เข็มขัด", "point": 5},
            {"shop" : "ร้านค้า 2","name": "เข็มขัด", "point": 5},
            {"shop" : "ร้านค้า 2","name": "เข็มขัด", "point": 5},
            {"shop" : "ร้านค้า 2","name": "เข็มขัด", "point": 5},
            {"shop" : "ร้านค้า 2","name": "เข็มขัด", "point": 5},
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

        #=================================================หน้า เติมเงิน=====================================================#
        self.topup_frame = tk.Frame(self,bg="white")

        self.topup_label_frame = tk.Frame(self.topup_frame,width=925,height=500,bg='white')
        self.topup_label_frame.pack(side=tk.TOP)

        self.topup_label = tk.Label(self.topup_label_frame,text="เติมเงิน",font=('Browallia New',20,'bold'),fg='black',bg='white')
        self.topup_label.place(x=440,y=0)

        self.topup_scancard_btn = tk.Button(self.topup_label_frame,text="แสกนบัตร",bg="#FFBF00",fg="white",width=10,height=1,border=0,font=('Browallia New',15,'bold'), command=lambda:self.scan_card(uid))
        self.topup_scancard_btn.place(x=650,y=95)

        self.topup_num = tk.Label(self.topup_label_frame,text="รหัสนิสิต : ",font=('Browallia New',20),fg='black',bg='white')
        self.topup_num.place(x=520,y=145)

        self.topup_name = tk.Label(self.topup_label_frame,text="ชื่อ : ",font=('Browallia New',20),fg='black',bg='white')
        self.topup_name.place(x=520,y=195)

        self.topup_money = tk.Label(self.topup_label_frame,text="เงินคงเหลือ : ",font=('Browallia New',20),fg='black',bg='white')
        self.topup_money.place(x=520,y=245)

        self.topup_point = tk.Label(self.topup_label_frame,text="พ้อยคงเหลือ SHOP1 : ",font=('Browallia New',20),fg='black',bg='white')
        self.topup_point.place(x=520,y=295)
        
        self.topup_point2 = tk.Label(self.topup_label_frame,text="พ้อยคงเหลือ SHOP2 : ",font=('Browallia New',20),fg='black',bg='white')
        self.topup_point2.place(x=520,y=345)


        self.topup_user_input = tk.Entry(self.topup_label_frame,width=32,fg='black',border=0,bg="#fff",font=('Browallia New',18))
        self.topup_user_input.place(x=127,y=160)
        self.topup_user_input.insert(0,'กรุณากรอกจำนวนเงินที่ต้องการเติม')
        tk.Frame(self.topup_label_frame,width=255,height=2,bg='black').place(x=128,y=193)
        self.topup_user_input.bind('<FocusIn>',self.on_enter_topup)
        self.topup_user_input.bind('<FocusOut>',self.on_enter_topup)

        self.topup_button_submit = tk.Button(self.topup_label_frame, text="เติมเงิน", bg="#4C956C", fg="white", width=13, height=1, border=0, font=('Browallia New', 15, 'bold'), command=lambda: self.topup(uid))

        self.topup_button_submit.place(x=195,y=230)

        #=================================================จบ เติมเงิน=====================================================#
    
        self.select_frame_by_name("login")
    
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
        if name == "ร้านค้า1" :
            self.shop_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.shop_frame.pack_forget()
            self.shop_frame.place_forget()
            self.shop_frame.grid_forget()
        if name == "ร้านค้า2" :
            self.shop_frame2.pack(fill=tk.BOTH, expand=True)
        else:
            self.shop_frame2.pack_forget()
            self.shop_frame2.place_forget()
            self.shop_frame2.grid_forget()
        if name == "point" :
            self.point_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.point_frame.pack_forget()
            self.point_frame.place_forget()
            self.point_frame.grid_forget()
        if name == "topup" :
            self.topup_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.topup_frame.pack_forget()
            self.topup_frame.place_forget()
            self.topup_frame.grid_forget()
            
    #====================== funtion input =================#

    def on_enter_reg_num(self,e):
        self.register_number_input.delete(0, 'end')
    
    def on_leave_reg_num(self,e):
        num = self.register_number_input.get()
        if num == '' :
            self.register_number_input.insert(0,'กรุณากรอกรหัสนิสิต')
    
    def on_enter_reg_user(self,e):
        self.register_user_input.delete(0, 'end')
    
    def on_leave_reg_user(self,e):
        user = self.register_user_input.get()
        if user == '' :
            self.register_user_input.insert(0,'กรุณากรอก username')
            
    def on_enter_reg_fname(self,e):
        self.register_fname_input.delete(0, 'end')
    
    def on_leave_reg_fname(self,e):
        fname = self.register_fname_input.get()
        if fname == '' :
            self.register_fname_input.insert(0,'กรุณากรอกชื่อ')
            
    def on_enter_reg_lname(self,e):
        self.register_lname_input.delete(0, 'end')
    
    def on_leave_reg_lname(self,e):
        lname = self.register_lname_input.get()
        if lname == '' :
            self.register_lname_input.insert(0,'กรุณากรอกนามสกุล')
    
    def on_enter_topup(self,e):
        self.topup_user_input.delete(0, 'end')
    
    def on_leave_topup(self,e):
        money = self.topup_user_input.get()
        if money == '' :
            self.topup_user_input.insert(0,'กรุณากรอกนามสกุล')
    
    def on_enter_otp(self,e):
        self.register_otp_input.delete(0, 'end')
    
    def on_leave_otp(self,e):
        otp = self.register_otp_input.get()
        if otp == '' :
            self.register_otp_input.insert(0,'กรุณากรอกนามสกุล')
    
    
    #===================================================แสดงสินค้าหน้า ร้านค้า1=================================================#
    
    def display_products(self):
        for idx, product in enumerate(self.products):
            product_frame = tk.Frame(self.products_frame, bg='white')
            product_frame.grid(row=idx // 5, column=idx % 5, padx=20, pady=20)

            name_label = tk.Label(product_frame, text=product["name"], font=('Browallia New', 12), bg='white')
            name_label.grid(row=0, column=1, padx=10)

            price_label = tk.Label(product_frame, text=f"ราคา : {product['price']} บาท", font=('Browallia New', 12), bg='white')
            price_label.grid(row=1, column=1, padx=10)

            add_to_cart_button = tk.Button(product_frame, text="ใส่รถเข็น", bg="#4C956C", fg="white", width=10, height=1, border=0, font=('Browallia New', 10, 'bold'), command=lambda product=product: self.add_to_cart(product))
            add_to_cart_button.grid(row=2, column=1, padx=10)

    def display_cart(self):
        for widget in self.shop_cart_frame.winfo_children():
            widget.destroy()

        cart_counts = {}
        total_cost = 0

        for product in self.shopping_cart:
            total_cost += product["price"]
            if product["name"] in cart_counts:
                cart_counts[product["name"]] += 1
            else:
                cart_counts[product["name"]] = 1

        for idx, (product_name, quantity) in enumerate(cart_counts.items()):
            cart_item_frame = tk.Frame(self.shop_cart_frame, bg='#D9D9D9')
            cart_item_frame.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

            name_label = tk.Label(cart_item_frame, text=f"{product_name} x{quantity}", font=('Browallia New', 12), bg='#D9D9D9')
            name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

            remove_button = tk.Button(cart_item_frame, text="Remove", bg="red", fg="white", width=8, height=1, border=0, font=('Browallia New', 10, 'bold'), command=lambda product_name=product_name: self.remove_from_cart(product_name))
            remove_button.grid(row=0, column=1, padx=5)

        total_label = tk.Label(self.shop_cart_frame, text=f"รวมทั้งหมด: {total_cost} บาท", font=('Browallia New', 14, 'bold'), bg='#D9D9D9')
        total_label.grid(row=len(cart_counts), column=0, padx=10, pady=10, sticky="e")

        confirm_button = tk.Button(self.shop_cart_frame, text="ชำระเงินผ่านบัตร", bg="#4C956C", fg="white", width=15, height=1, border=0, font=('Browallia New', 12, 'bold'), command=lambda total_cost=total_cost, cart_items=cart_counts.items(): self.confirm_purchase(total_cost, cart_items, uid))
        confirm_button.grid(row=len(cart_counts) + 1, column=0, padx=30, pady=10, sticky="e")

    def confirm_purchase(self, total_cost, cart_items, card_owner_uid):
        self.shopping_cart.clear()
        self.display_cart()
        
        with open('data.json', 'r') as file:
            data = json.load(file)

        card_owner_info = None
        for user in data['USER']:
            if user['UID'] == card_owner_uid:
                card_owner_info = user
                break

        new_window = tk.Toplevel(self)
        new_window.title('ยืนยันการชำระ')
        new_window.geometry("925x500+300+200")
        new_window.configure(background='white')

        for idx, (product_name, quantity) in enumerate(cart_items):
            product_label = tk.Label(new_window, text=f"{product_name} x{quantity}", font=('Browallia New', 16),bg='white')
            y_offset = 20 + idx * 30 
            product_label.place(anchor='e', x=900, y=y_offset) 

        total_cost_label = tk.Label(new_window, text=f"รวมทั้งหมด: {total_cost} บาท", font=('Browallia New', 16),bg='white')
        total_cost_label.place(x=760, y=390)

        confirm_button = tk.Button(new_window, text="ยืนยันการชำระเงิน", bg="#4C956C", fg="white", width=15, height=1, border=0, font=('Browallia New', 16, 'bold'), command=lambda total_cost=total_cost:self.buyitem(total_cost, uid))
        confirm_button.place(x=765,y=440)

        scan_card_label = tk.Button(new_window,text="แสกนบัตร",bg="#FFBF00",fg="white",width=15,height=1,border=0,font=('Browallia New',15,'bold'), command=lambda: self.scan_card2(card_owner_uid))
        scan_card_label.place(x=240,y=100)
        
        self.nisit_id_label = tk.Label(new_window, text="รหัสนิสิต :", font=('Browallia New', 22), bg='white')
        self.name_label = tk.Label(new_window, text="ชื่อ-นามสกุล : ", font=('Browallia New', 22), bg='white')
        self.money_label = tk.Label(new_window, text="เงินคงเหลือ : ", font=('Browallia New', 22), bg='white')
        
        self.nisit_id_label.place(anchor='w', x=200, y=200)
        self.name_label.place(anchor='w', x=200, y=240)
        self.money_label.place(anchor='w', x=200, y=320)
        
        if card_owner_info:
            self.nisit_id_label.config(text=f"รหัสนิสิต : {card_owner_info['NisitID']}")
            self.name_label.config(text=f"ชื่อ-นามสกุล : {card_owner_info['UserName']} {card_owner_info['LastName']}")
            self.money_label.config(text=f"เงินคงเหลือ : {card_owner_info['Money']}")        

        else:
            error_label = tk.Label(new_window, text="ไม่พบข้อมูลเจ้าของบัตร")
            error_label.place(x=10, y=150)

        self.shopping_cart.clear()

        self.display_cart()
        
    def add_to_cart(self, product):
        self.shopping_cart.append(product)
        self.display_cart()

    def remove_from_cart(self, product_name):
        for idx, product in enumerate(self.shopping_cart):
            if product["name"] == product_name:
                del self.shopping_cart[idx]
                break

        self.display_cart()

    #===================================================จบ แสดงสินค้าหน้า ร้านค้า 1==============================================#
        
    #=====================================================แสดงสินค้าหน้า แลกพ้อย=================================================#

    def display_points(self):
        for widget in self.product_point_frame.winfo_children():
            widget.destroy()

        for idx, product in enumerate(self.point_products):
            product_point_frame = tk.Frame(self.product_point_frame, bg='white')
            product_point_frame.grid(row=idx // 5, column=idx % 5, padx=17, pady=20)

            shop_label = tk.Label(product_point_frame, text=product["shop"], font=('Browallia New', 13), bg='white')
            shop_label.grid(row=0, column=1, padx=5)

            name_label = tk.Label(product_point_frame, text=product["name"], font=('Browallia New', 12), bg='white')
            name_label.grid(row=1, column=1, padx=5)

            points_label = tk.Label(product_point_frame, text=f"แลกแต้ม : {product['point']} แต้ม", font=('Browallia New', 12), bg='white')
            points_label.grid(row=2, column=1, padx=5)

            add_to_cart_button = tk.Button(product_point_frame, text="ใส่รถเข็น", bg="#4C956C", fg="white", width=10, height=1, border=0, font=('Browallia New', 10, 'bold'), command=lambda product=product: self.add_to_cart_point(product))
            add_to_cart_button.grid(row=3, column=1, padx=5)
    
    def display_cart_point(self):
        for widget in self.point_kart_frame.winfo_children():
            widget.destroy()

        cart_by_shop = {}
        total_points_by_shop = {}

        for item in self.shopping_cart_point:
            shop_name = item["shop"]
            if shop_name not in cart_by_shop:
                cart_by_shop[shop_name] = []
                total_points_by_shop[shop_name] = 0
            cart_by_shop[shop_name].append(item)
            total_points_by_shop[shop_name] += item["point"]

        row_offset = 0
        for shop_name, items in cart_by_shop.items():
            shop_label = tk.Label(self.point_kart_frame, text=f"ร้าน {shop_name}", font=('Browallia New', 14, 'bold'), bg='#D9D9D9')
            shop_label.grid(row=row_offset, column=0, padx=10, pady=5, sticky="w")
            row_offset += 1

            cart_counts = {}
            total_points = total_points_by_shop[shop_name]

            for item in items:
                if item["name"] in cart_counts:
                    cart_counts[item["name"]] += 1
                else:
                    cart_counts[item["name"]] = 1

            for idx, (product_name, quantity) in enumerate(cart_counts.items()):
                cart_item_frame = tk.Frame(self.point_kart_frame, bg='#D9D9D9')
                cart_item_frame.grid(row=row_offset, column=0, padx=10, pady=5, sticky="w")

                name_label = tk.Label(cart_item_frame, text=f"{product_name} x{quantity}", font=('Browallia New', 12), bg='#D9D9D9')
                name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

                remove_button = tk.Button(cart_item_frame, text="Remove", bg="red", fg="white", width=8, height=1, border=0, font=('Browallia New', 10, 'bold'), command=lambda product_name=product_name, shop_name=shop_name: self.remove_from_cart_point(product_name, shop_name))
                remove_button.grid(row=0, column=1, padx=5)

                row_offset += 1

            total_label = tk.Label(self.point_kart_frame, text=f"รวมทั้งหมด: {total_points} แต้ม", font=('Browallia New', 14, 'bold'), bg='#D9D9D9')
            total_label.grid(row=row_offset, column=0, padx=10, pady=10, sticky="e")
            row_offset += 1

            confirm_button = tk.Button(self.point_kart_frame, text="ชำระผ่านบัตร", bg="#4C956C", fg="white", width=15, height=1, border=0, font=('Browallia New', 12, 'bold'), command=lambda total_points=total_points, cart_items=cart_counts.items(): self.confirm_purchase_point(total_points, cart_items, uid))
            confirm_button.grid(row=row_offset, column=0, padx=30, pady=10, sticky="e")
            row_offset += 1

    def confirm_purchase_point(self, total_points, cart_items, card_owner_uid):
        self.shopping_cart.clear()
        self.display_cart()

        with open('data.json', 'r') as file:
            data = json.load(file)


        card_owner_info = None
        for user in data['USER']:
            if user['UID'] == card_owner_uid:
                card_owner_info = user
                break

        new_window = tk.Toplevel(self)
        new_window.title('ยืนยันการชำระ')
        new_window.geometry("925x500+300+200")
        new_window.configure(background='white')

        for idx, (product_name, quantity) in enumerate(cart_items):
            product_label = tk.Label(new_window, text=f"{product_name} x{quantity}", font=('Browallia New', 16),bg='white')
            y_offset = 20 + idx * 30 
            product_label.place(anchor='e', x=900, y=y_offset) 

        total_cost_label = tk.Label(new_window, text=f"รวมทั้งหมด: {total_points} แต้ม", font=('Browallia New', 16),bg='white')
        total_cost_label.place(x=760, y=390)

        confirm_button = tk.Button(new_window, text="ยืนยันการชำระเงิน", bg="#4C956C", fg="white", width=15, height=1, border=0, font=('Browallia New', 16, 'bold'))
        confirm_button.place(x=765,y=440)

        scan_card_label = tk.Button(new_window,text="แสกนบัตร",bg="#FFBF00",fg="white",width=15,height=1,border=0,font=('Browallia New',15,'bold'))
        scan_card_label.place(x=240,y=100)
        
        if card_owner_info:
            info_text = f"รหัสนิสิต : {card_owner_info['NisitID']}\n"
            info_text += f"ชื่อ : {card_owner_info['UserName']}\n"
            info_text += f"นามสกุล : {card_owner_info['LastName']}\n"
            info_text += f"แต้มคงเหลือ : {card_owner_info['Money']}"

            info_label = tk.Label(new_window, text=info_text, font=('Browallia New', 22),bg='white')
            info_label.place(anchor='w', x=200, y=240)

        else:
            error_label = tk.Label(new_window, text="ไม่พบข้อมูลเจ้าของบัตร")
            error_label.place(x=10, y=150)

        self.shopping_cart.clear()

        self.display_cart()

    def add_to_cart_point(self, product):
        self.shopping_cart_point.append(product)
        self.display_cart_point()

    def remove_from_cart_point(self, product_name, shop_name):
        self.shopping_cart_point = [item for item in self.shopping_cart_point if not (item["name"] == product_name and item["shop"] == shop_name)]
        self.display_cart_point()

    #=====================================================จบแสดงสินค้าหน้า แลกพ้อย===============================================#
        
    #===================================================แสดงสินค้าหน้า ร้านค้า 2=================================================#

    def display_products_shop2(self):
        for idx, product in enumerate(self.products_shop2):
            product_frame = tk.Frame(self.products_frame_shop2, bg='white')
            product_frame.grid(row=idx // 5, column=idx % 5, padx=20, pady=20)

            name_label = tk.Label(product_frame, text=product["name"], font=('Browallia New', 12), bg='white')
            name_label.grid(row=0, column=1, padx=10)

            price_label = tk.Label(product_frame, text=f"ราคา : {product['price']} บาท", font=('Browallia New', 12), bg='white')
            price_label.grid(row=1, column=1, padx=10)

            add_to_cart_button = tk.Button(product_frame, text="ใส่รถเข็น", bg="#4C956C", fg="white", width=10, height=1, border=0, font=('Browallia New', 10, 'bold'),
                                        command=lambda prod=product: self.add_to_cart_shop2(prod))
            add_to_cart_button.grid(row=2, column=1, padx=10)
    
    def display_cart_items_shop2(self):
        for widget in self.shop_cart_frame2.winfo_children():
            widget.destroy()

        cart_counts2 = {}
        total_cost2 = 0

        for product in self.shopping_cart2:
            total_cost2 += product["price"]
            if product["name"] in cart_counts2:
                cart_counts2[product["name"]] += 1
            else:
                cart_counts2[product["name"]] = 1

        for idx, (product_name, quantity) in enumerate(cart_counts2.items()):
            cart_item_frame = tk.Frame(self.shop_cart_frame2, bg='#D9D9D9')
            cart_item_frame.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

            name_label = tk.Label(cart_item_frame, text=f"{product_name} x{quantity}", font=('Browallia New', 12), bg='#D9D9D9')
            name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

            remove_button = tk.Button(cart_item_frame, text="Remove", bg="red", fg="white", width=8, height=1, border=0, font=('Browallia New', 10, 'bold'), command=lambda product_name=product_name: self.remove_from_cart_shop2(product_name))
            remove_button.grid(row=0, column=1, padx=5)

        total_label = tk.Label(self.shop_cart_frame2, text=f"รวมทั้งหมด: {total_cost2} บาท", font=('Browallia New', 14, 'bold'), bg='#D9D9D9')
        total_label.grid(row=len(cart_counts2), column=0, padx=10, pady=10, sticky="e")

        confirm_button = tk.Button(self.shop_cart_frame2, text="ชำระผ่านบัตร", bg="#4C956C", fg="white", width=15, height=1, border=0, font=('Browallia New', 12, 'bold'), command=lambda total_points=total_cost2, cart_items=cart_counts2.items(): self.confirm_purchase_shop2(total_points, cart_items, uid))
        confirm_button.grid(row=len(cart_counts2) + 1, column=0, padx=30, pady=10, sticky="e")
    
    def add_to_cart_shop2(self, product):
        self.shopping_cart2.append(product)
        self.display_cart_items_shop2()
    
    def confirm_purchase_shop2(self, total_points, cart_items, card_owner_uid):
        self.shopping_cart.clear()
        self.display_cart()

        with open('data.json', 'r') as file:
            data = json.load(file)


        card_owner_info = None
        for user in data['USER']:
            if user['UID'] == card_owner_uid:
                card_owner_info = user
                break

        new_window = tk.Toplevel(self)
        new_window.title('ยืนยันการชำระ')
        new_window.geometry("925x500+300+200")
        new_window.configure(background='white')

        for idx, (product_name, quantity) in enumerate(cart_items):
            product_label = tk.Label(new_window, text=f"{product_name} x{quantity}", font=('Browallia New', 16),bg='white')
            y_offset = 20 + idx * 30 
            product_label.place(anchor='e', x=900, y=y_offset) 

        total_cost_label = tk.Label(new_window, text=f"รวมทั้งหมด: {total_points} แต้ม", font=('Browallia New', 16),bg='white')
        total_cost_label.place(x=760, y=390)

        confirm_button = tk.Button(new_window, text="ยืนยันการชำระเงิน", bg="#4C956C", fg="white", width=15, height=1, border=0, font=('Browallia New', 16, 'bold'))
        confirm_button.place(x=765,y=440)

        scan_card_label = tk.Button(new_window,text="แสกนบัตร",bg="#FFBF00",fg="white",width=15,height=1,border=0,font=('Browallia New',15,'bold'))
        scan_card_label.place(x=240,y=100)
        
        if card_owner_info:
            info_text = f"รหัสนิสิต : {card_owner_info['NisitID']}\n"
            info_text += f"ชื่อ : {card_owner_info['UserName']}\n"
            info_text += f"นามสกุล : {card_owner_info['LastName']}\n"
            info_text += f"เงิน : {card_owner_info['Money']}"

            info_label = tk.Label(new_window, text=info_text, font=('Browallia New', 22),bg='white')
            info_label.place(anchor='w', x=200, y=240)

        else:
            error_label = tk.Label(new_window, text="ไม่พบข้อมูลเจ้าของบัตร")
            error_label.place(x=10, y=150)

        self.shopping_cart.clear()

        self.display_cart()
    
    def remove_from_cart_shop2(self, product):
        for idx, item in enumerate(self.shopping_cart2):
            if item["name"] == product:
                del self.shopping_cart2[idx]
                break
        self.display_cart_items_shop2()
    
    #==================================================จบแสดงสินค้าหน้า ร้านค้า 2=================================================#
    
    #================================================== function ซื้อของ=================================================#
    def buyitem(self, total_cost, uid):
        filename = 'data.json'
        
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return

        user_found = False
        for user in data['USER']:
            if user['UID'] == uid:
                if user['Money'] >= total_cost:
                    user['Money'] -= total_cost
                    user_found = True
                    print(f"ซื้อสินค้าสำเร็จ! ยอดเงินคงเหลือ {user['Money']} บาท.")
                else:
                    print("เงินไม่เพียงพอที่จะซื้อสินค้า")
                break

        if not user_found:
            print(f"UID {uid} not found.")
        else:
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)

    #==================================================จบ function ซื้อของ=================================================#
    
    #================================================== function แสกนการ์ด=================================================#
    def login(self, uid):
        with open('data.json') as f:
            data = json.load(f)
            
        user_found = False
        for user in data["USER"]:
            if user["UID"] == uid:
                user_found = True
                username = user["UserName"]
                welcome_message = f"ยินดีต้อนรับ {username}!"
                confirmation = messagebox.askquestion("ยินดีต้อนรับ", welcome_message, icon='info')
                if confirmation == 'yes':
                    self.select_frame_by_name("ร้านค้า1")
                    
        if not user_found:
            notfound_message = "ไม่พบข้อมูลผู้ใช้ กรุณาสมัครสมาชิก"
            confirmation = messagebox.askquestion("ไม่พบข้อมูล", notfound_message , icon='error')
            if confirmation == 'yes':
                    self.select_frame_by_name("register")
        
    
    def scan_card(self, uid):
        # อ่านข้อมูลจากไฟล์ JSON
        with open('data.json') as f:
            data = json.load(f)


        # ค้นหาข้อมูลผู้ใช้โดยใช้ UID
        user_info = None
        for user in data["USER"]:
            if user["UID"] == uid:
                user_info = user
                break
        
        user_shop_info = None
        for user in data["SHOP1"]:
            if user["UID"] == uid:
                user_shop_info = user
                break
        
        user_shop_info2 = None
        for user in data["SHOP2"]:
            if user["UID"] == uid:
                user_shop_info2 = user
                break
            
        # ถ้าพบข้อมูลผู้ใช้
        if user_info or user_shop_info:
            # นำข้อมูลที่ดึงมาแสดงบน Label
            self.topup_num.config(text=f"รหัสนิสิต : {user_info['NisitID']}")
            self.topup_name.config(text=f"ชื่อ : {user_info['UserName']} {user_info['LastName']}")
            self.topup_money.config(text=f"เงินคงเหลือ : {user_info['Money']}")
            self.topup_point.config(text=f"พ้อยคงเหลือ SHOP1: {user_shop_info['Point']}")
            self.topup_point2.config(text=f"พ้อยคงเหลือ SHOP2: {user_shop_info2['Point']}")
        else:
            print("ไม่พบข้อมูลผู้ใช้")
    
    def scan_card_for_reg(self,uid):
        self.register_idcard_label.config(text=f"ข้อมูล Card ID : {uid}")
    
        
    def scan_card2(self, card_owner_uid):
        with open('data.json', 'r') as file:
            data = json.load(file)
        

        card_owner_info = None
        for user in data['USER']:
            if user['UID'] == card_owner_uid:
                card_owner_info = user
                break        
        
        if card_owner_info:
            self.nisit_id_label.config(text=f"รหัสนิสิต : {card_owner_info['NisitID']}")
            self.name_label.config(text=f"ชื่อ-นามสกุล : {card_owner_info['UserName']} {card_owner_info['LastName']}")
            self.money_label.config(text=f"เงินคงเหลือ : {card_owner_info['Money']}")

        else:
            self.error_label.config(text="ไม่พบข้อมูลเจ้าของบัตร")

    
    #==================================================จบ function แสกนการ์ด=================================================#
    
    #==================================================function เติมเงิน=================================================#

    def showmoney(self, uid):
        filename = 'data.json'
        
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return

        user_found = False
        for user in data['USER']:
            if user['UID'] == uid:
                print(f"ยอดเงินคงเหลือ {user['Money']} บาท")
                user_found = True
                break

        if not user_found:
            print(f"UID {uid} not found.")
    
    def topup(self, uid):

        # Get the money input from the user
        money_str = self.topup_user_input.get()
        
        try:
            moneys = float(money_str)
        except ValueError:
            print("Invalid input for money. Please enter a valid number.")
            return

        filename = 'data.json'
        
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return

        user_found = False
        for user in data['USER']:
            if user['UID'] == uid:
                # Convert the money to float before adding
                user['Money'] = float(user['Money']) + moneys
                user_found = True
                print(f"Top-up successful. New balance for ID {user['ID']} is {user['Money']}.")
                break

        if not user_found:
            print(f"UID {uid} not found.")
            return

        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        
        self.showmoney(uid)
    
    #==================================================จบ function เติมเงิน=================================================#
    
    #==================================================function สมัครสมาชิก=================================================#
    def generate_otp(self):
        return ''.join(random.choices('0123456789', k=6))
    
    def send_email_with_otp(self):
        sender_email = "nopanon.ve@ku.th"
        password = "Nope$$2945"
        email = self.register_user_input.get().strip()
        username = self.register_fname_input.get().strip()
        lastname = self.register_lname_input.get().strip()
        nitsitId = self.register_number_input.get().strip()
        
        if not email or not username or not lastname or not nitsitId:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # ตรวจสอบว่าอีเมล์มีโดเมน @ku.th หรือไม่
        if not email.endswith("@ku.th"):
            messagebox.showerror("Error", "Please enter an email with domain '@ku.th'.")
            return

        receiver_email = f"{email}"
        subject = "OTP Verification"
        self.otp = self.generate_otp()
        message = f"Hello {username},\nYour OTP is: {self.otp}"

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            print("Connected to the server and logged in successfully") 
            body = '\r\n'.join(['To: %s' % receiver_email,
                                'From: %s' % sender_email,
                                'Subject: %s' % subject,
                                '', message, ''])

            try:
                # Check if the Email already exists in the JSON file
                if self.email_exists(email):
                    messagebox.showerror("Error", f"Email '{email}' already exists.")
                    return
                else:
                    server.sendmail(sender_email, receiver_email, body)
                    print("OTP Email sent successfully to", receiver_email)
            except Exception as e:
                print("Failed to send OTP email:", e)
                messagebox.showerror("Error", "Failed to send OTP email. Please try again later.")
            finally:
                server.quit()
        except smtplib.SMTPRecipientsRefused as e:
            print("Recipient email not found:", e)
            messagebox.showerror("Error", "Recipient email not found. Please check the email address.")
        except Exception as e:
            print("An error occurred:", e)
            messagebox.showerror("Error", "An error occurred. Please try again later.")

    def verify_otp(self,uid):
            entered_otp = self.register_otp_input.get()
            email = self.register_user_input.get()
            if entered_otp == self.otp:
                messagebox.showinfo("Success", "OTP Verified Successfully!")
                self.update_json(email, uid, "USER")
                self.update_SHOP1(email, uid, "SHOP1")
                self.update_SHOP2(email, uid, "SHOP2")
            else:
                messagebox.showerror("Error", "Invalid OTP. Please try again.")
    
    @staticmethod
    def email_exists(email):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                for user in data['USER']:
                    if user['Email'] == email:
                        return True
        except FileNotFoundError:
            pass
        return False

    def update_json(self,Email, uid, group=""):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                max_id = max([user['ID'] for user in data[group]])

        except (FileNotFoundError, ValueError):
            data = {group: []}
            max_id = 0

        new_user = {
            "ID": max_id + 1,
            "UID": uid,
            "NisitID": self.register_number_input.get().strip(),
            "UserName": self.register_fname_input.get().strip(),
            "LastName": self.register_lname_input.get().strip(),
            "Email": Email, 
            "Money": 0
        }

        data[group].append(new_user)

        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)

    def update_SHOP1(self,Email, uid, group=""):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                max_id = max([user['ID'] for user in data[group]])

        except (FileNotFoundError, ValueError):
            data = {group: []}
            max_id = 0

        shopnew_user = {
            "ID": max_id + 1,
            "UID": uid,
            "Email": Email,
            "NisitID": self.register_number_input.get(),
            "ShopID": "S001",
            "Point": 0
        }

        data[group].append(shopnew_user)

        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)

    def update_SHOP2(self,Email, uid, group=""):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                max_id = max([user['ID'] for user in data[group]])

        except (FileNotFoundError, ValueError):
            data = {group: []}
            max_id = 0

        shopnew_user = {
            "ID": max_id + 1,
            "UID": uid,
            "Email": Email,
            "NisitID": self.register_number_input.get(),
            "ShopID": "S002",
            "Point": 0
        }

        data[group].append(shopnew_user)

        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)


if __name__ == "__main__":
    my_obj = NFC_Reader()
    uid = my_obj.read_uid()
    app = App()
    app.mainloop()