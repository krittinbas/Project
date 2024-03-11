from smartcard.scard import *
import tkinter as tk
from tkinter import messagebox
import smtplib
import random
import json


def newuser_Otp(uid, register_number_input, register_user_input, register_fname_input, register_lname_input, register_otp_input):
    def generate_otp():
        return ''.join(random.choices('0123456789', k=6))

    def send_email_with_otp():
        sender_email = "nopanon.ve@ku.th"
        password = "Nope$$2945"
        email = register_user_input.get().strip()
        username = register_fname_input.get().strip()
        lastname = register_lname_input.get().strip()
        nitsitId = register_number_input.get().strip()

        if not email or not username or not lastname or not nitsitId:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # ตรวจสอบว่าอีเมล์มีโดเมน @ku.th หรือไม่
        if not email.endswith("@ku.th"):
            messagebox.showerror("Error", "Please enter an email with domain '@ku.th'.")
            return

        receiver_email = f"{email}"
        subject = "OTP Verification"
        otp = generate_otp()
        message = f"Hello {username},\nYour OTP is: {otp}"

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
                if email_exists(email):
                    messagebox.showerror("Error", f"Email '{email}' already exists.")
                    return
                else:
                    server.sendmail(sender_email, receiver_email, body)
                    print("OTP Email sent successfully to", receiver_email)
                    show_otp_window(otp, email, uid)  # Pass the UID to show_otp_window function
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

    def show_otp_window(otp, email, uid):
        otp_window = tk.Toplevel(root)
        otp_window.title("Enter OTP")
        
        otp_label = tk.Label(otp_window, text="Enter OTP:")
        otp_label.pack()
        otp_entry = tk.Entry(otp_window)
        otp_entry.pack()
        print(otp)
        def verify_otp():
            entered_otp = otp_entry.get()
            if entered_otp == otp:
                messagebox.showinfo("Success", "OTP Verified Successfully!")
                otp_window.destroy()
                update_json(email, uid, "USER")
                update_SHOP1(email, uid, "SHOP1")
                update_SHOP2(email, uid, "SHOP2")
                root.destroy()
            else:
                messagebox.showerror("Error", "Invalid OTP. Please try again.")

        verify_button = tk.Button(otp_window, text="Verify", command=verify_otp)
        verify_button.pack()

    def update_json(Email, uid, group=""):
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
            "NitsitId": nitsitId_var.get().strip(),
            "UserName": username_var.get().strip(),
            "LastName": lastname_var.get().strip(),
            "Email": Email, 
            "Money": 0
        }

        data[group].append(new_user)

        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)

    def update_SHOP1(Email, uid, group=""):
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
            "NitsitId": nitsitId_var.get(),
            "ShopID": "S001",
            "Point": 0
        }

        data[group].append(shopnew_user)

        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)

    def update_SHOP2(Email, uid, group=""):
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
            "NitsitId": nitsitId_var.get(),
            "ShopID": "S002",
            "Point": 0
        }

        data[group].append(shopnew_user)

        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)


    root = tk.Tk()
    root.title("Send Email with OTP")
    root.pack_propagate(False)

    email_label = tk.Label(root, text="Enter Email:")
    email_label.pack()
    email_var = tk.StringVar()
    email_entry = tk.Entry(root, textvariable=email_var)
    email_entry.pack()

    username_label = tk.Label(root, text="Enter Username:")
    username_label.pack()
    username_var = tk.StringVar()
    username_entry = tk.Entry(root, textvariable=username_var)
    username_entry.pack()

    lastname_label = tk.Label(root, text="Enter Lastname:")
    lastname_label.pack()
    lastname_var = tk.StringVar()
    lastname_entry = tk.Entry(root, textvariable=lastname_var)
    lastname_entry.pack()

    nitsitId_label = tk.Label(root, text="Enter NitsitId:")
    nitsitId_label.pack()
    nitsitId_var = tk.StringVar()
    nitsitId_entry = tk.Entry(root, textvariable=nitsitId_var)
    nitsitId_entry.pack()

    submit_button = tk.Button(root, text="Send OTP", command=send_email_with_otp)
    submit_button.pack()

    root.mainloop() 