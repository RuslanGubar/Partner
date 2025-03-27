import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from database_connection import connect_to_database
from style_guide import FONT, HEADING_FONT, BG_COLOR, BUTTON_COLOR
from PIL import Image, ImageTk

class AddEditPartnerForm(tk.Toplevel):
    def __init__(self, parent, partner_module, partner_id=None):
        super().__init__(parent)
        self.parent = parent
        self.partner_module = partner_module
        self.partner_id = partner_id
        self.title("Создать/изменить партнера")
        self.configure(bg=BG_COLOR)
        self.geometry("600x450")

        self.type_id_map = {}

        self.create_widgets()
        if self.partner_id:
            self.load_partner_data()

    def load_partner_data(self):
        conn = connect_to_database()
        if not conn:
            return
        try:
            cur = conn.cursor()
            query = "SELECT partnerName, typeID, partnerRaiting, addressID, partnerDirector, partnerPhone, partnerMail, partnerINN FROM zzz.partner WHERE partnerID = %s"
            cur.execute(query, (self.partner_id,))
            partner_data = cur.fetchone()
            if partner_data:
                name, type_id, rating, address_id, director, phone, mail, inn = partner_data
                self.name_entry.insert(0, name)

                # Reverse lookup typeName from typeID:
                for type_name, type_id_from_map in self.type_id_map.items():
                    if type_id_from_map == type_id:
                        self.type_combo.set(type_name)
                        break

                self.rating_entry.insert(0, rating)
                self.address_entry.insert(0, address_id)
                self.director_entry.insert(0, director)
                self.phone_entry.insert(0, phone)
                self.mail_entry.insert(0, mail)
                self.inn_entry.insert(0, inn)
        except psycopg2.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка в загрузке партнера {e}")
        finally:
            if hasattr(cur, 'close') and callable(getattr(cur, 'close')):
                cur.close()
            if hasattr(conn, 'close') and callable(getattr(conn, 'close')):
                conn.close()

    def create_widgets(self):
        self.heading_label = tk.Label(self, text="Партнеры", font=HEADING_FONT, bg=BG_COLOR)
        self.heading_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.name_label = tk.Label(self, text="Название:", font=FONT, bg=BG_COLOR)
        self.name_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.name_entry = tk.Entry(self, font=FONT)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.type_label = tk.Label(self, text="Тип партнера:", font=FONT, bg=BG_COLOR)
        self.type_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        conn = connect_to_database()
        partner_types = []
        try:
            cur = conn.cursor()
            query = "SELECT typeID, typeName FROM zzz.type_partner"
            cur.execute(query)
            partner_types = cur.fetchall()

            for type_id, type_name in partner_types:
                self.type_id_map[type_name] = type_id

            partner_type_names = list(self.type_id_map.keys())

        except psycopg2.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при выборе типов партнеров: {e}")
        finally:
            if hasattr(conn, 'close') and callable(getattr(conn, 'close')):
                conn.close()

        self.type_combo = ttk.Combobox(self, values=partner_type_names, font=FONT)
        self.type_combo.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.rating_label = tk.Label(self, text="Рейтинг:", font=FONT, bg=BG_COLOR)
        self.rating_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.rating_entry = tk.Entry(self, font=FONT)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.address_label = tk.Label(self, text="Адрес:", font=FONT, bg=BG_COLOR)
        self.address_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.address_entry = tk.Entry(self, font=FONT)
        self.address_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        self.director_label = tk.Label(self, text="Директор:", font=FONT, bg=BG_COLOR)
        self.director_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.director_entry = tk.Entry(self, font=FONT)
        self.director_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        self.phone_label = tk.Label(self, text="Телефон:", font=FONT, bg=BG_COLOR)
        self.phone_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.phone_entry = tk.Entry(self, font=FONT)
        self.phone_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        self.mail_label = tk.Label(self, text="Почта:", font=FONT, bg=BG_COLOR)
        self.mail_label.grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.mail_entry = tk.Entry(self, font=FONT)
        self.mail_entry.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        self.inn_label = tk.Label(self, text="ИНН:", font=FONT, bg=BG_COLOR)
        self.inn_label.grid(row=8, column=0, padx=5, pady=5, sticky="e")
        self.inn_entry = tk.Entry(self, font=FONT)
        self.inn_entry.grid(row=8, column=1, padx=5, pady=5, sticky="w")

        self.button_frame = tk.Frame(self, bg=BG_COLOR)
        self.button_frame.grid(row=9, column=0, columnspan=2, pady=10)

        self.save_button = tk.Button(self.button_frame, text="Сохранить", font=FONT, bg=BUTTON_COLOR, command=self.save_partner)
        self.save_button.grid(row=0, column=0, padx=5)

        self.cancel_button = tk.Button(self.button_frame, text="Отменить", font=FONT, bg=BUTTON_COLOR, command=self.destroy)
        self.cancel_button.grid(row=0, column=1, padx=5)

    def save_partner(self):
        try:
            name = self.name_entry.get()
            selected_type_name = self.type_combo.get()
            type_id = self.type_id_map[selected_type_name]
            rating = int(self.rating_entry.get())
            address = self.address_entry.get()
            director = self.director_entry.get()
            phone = self.phone_entry.get()
            mail = self.mail_entry.get()
            inn = self.inn_entry.get()

            # Check if required fields are empty
            if not name or not director or not phone or not mail or not inn:
                messagebox.showerror("Ошибка", "все поля обязательны для заполнения.")
                return

            # Check if Rating is negative
            if rating < 0:
                messagebox.showerror("Ошибка", "Рейтинг не может быть отрицательным числом.")
                return

        except KeyError:
            messagebox.showerror("Error", "Invalid partner type selected.")
            return

        conn = connect_to_database()
        if not conn:
            return

        try:
            cur = conn.cursor()
            if self.partner_id:
                query = """
                    UPDATE zzz.partner
                    SET partnerName=%s, typeID=%s, partnerRaiting=%s, addressid=%s, partnerDirector=%s, partnerPhone=%s, partnerMail=%s, partnerINN=%s
                    WHERE partnerID=%s
                """
                params = (name, type_id, rating, address, director, phone, mail, inn, self.partner_id)
            else:
                query = """
                    INSERT INTO zzz.partner (partnerName, typeID, partnerRaiting, addressid, partnerDirector, partnerPhone, partnerMail, partnerINN)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = (name, type_id, rating, address, director, phone, mail, inn)
            cur.execute(query, params)
            conn.commit()
            messagebox.showinfo("Success", "Partner data saved successfully.")
            self.partner_module.load_partners()  # Refresh
            self.destroy()

        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Error saving partner {e}")
        finally:
            if hasattr(cur, 'close') and callable(getattr(cur, 'close')):
                cur.close()
            if hasattr(conn, 'close') and callable(getattr(conn, 'close')):
                conn.close()