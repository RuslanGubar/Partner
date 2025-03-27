import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from database_connection import connect_to_database
from style_guide import FONT, HEADING_FONT, BG_COLOR, SECONDARY_BG_COLOR, BUTTON_COLOR
from add_edit_partner_form import AddEditPartnerForm
from PIL import Image, ImageTk

class PartnerModule(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.configure(bg=BG_COLOR)
        self.grid(row=0, column=0, sticky="nsew")
        self.selected_partner_id = None


        self.create_widgets()

    def calculate_discount(self, partner_id):
        conn = connect_to_database()
        if not conn:
            return 0

        try:
            cur = conn.cursor()
            query = """
            SELECT SUM(pp.partnerproductColisestvo)
            FROM zzz.partner_product pp
            WHERE pp.partnerID = %s
            """
            cur.execute(query, (partner_id,))
            total_sales = cur.fetchone()[0]
            if total_sales is None:
                total_sales = 0
        except psycopg2.Error as e:
            print(f"Ошибка: {e}")
            total_sales = 0
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

        if total_sales < 10000:
            return 0
        elif 10000 <= total_sales < 50000:
            return 0.05
        elif 50000 <= total_sales < 300000:
            return 0.10
        else:
            return 0.15

    def load_partners(self):
        conn = connect_to_database()
        if not conn:
            return

        try:
            cur = conn.cursor()
            query = """
                SELECT
                    p.partnerID,
                    tp.typeName,
                    p.partnerName,
                    p.partnerDirector,
                    p.partnerPhone,
                    p.partnerRaiting
                FROM zzz.partner p
                JOIN zzz.type_partner tp ON p.typeID = tp.typeID
                """
            cur.execute(query)
            partners = cur.fetchall()

            for widget in self.partner_container.winfo_children():
                widget.destroy()

            for partner in partners:
                partner_id, partner_type, partner_name, partner_director, partner_phone, partner_rating = partner
                discount = self.calculate_discount(partner_id)

                partner_frame = tk.Frame(self.partner_container, bg=SECONDARY_BG_COLOR, relief="groove", borderwidth=1)
                partner_frame.pack(pady=5, padx=10, fill="x")

                partner_frame.bind("<Button-1>", lambda event, id=partner_id: self.select_partner(id))

                name_label = tk.Label(partner_frame, text=f"{partner_type} | {partner_name}", font=FONT, bg=SECONDARY_BG_COLOR,
                                      anchor="w")
                name_label.pack(fill="x")
                director_label = tk.Label(partner_frame, text=f"Директор: {partner_director}", font=FONT, bg=SECONDARY_BG_COLOR,
                                          anchor="w")
                director_label.pack(fill="x")
                phone_label = tk.Label(partner_frame, text=f"Телефон: {partner_phone}", font=FONT, bg=SECONDARY_BG_COLOR,
                                       anchor="w")
                phone_label.pack(fill="x")
                rating_label = tk.Label(partner_frame, text=f"Рейтинг: {partner_rating}", font=FONT, bg=SECONDARY_BG_COLOR,
                                        anchor="w")
                rating_label.pack(fill="x")

                name_label.bind("<Button-1>", lambda event, id=partner_id: self.select_partner(id))
                director_label.bind("<Button-1>", lambda event, id=partner_id: self.select_partner(id))
                phone_label.bind("<Button-1>", lambda event, id=partner_id: self.select_partner(id))
                rating_label.bind("<Button-1>", lambda event, id=partner_id: self.select_partner(id))

                discount_label = tk.Label(partner_frame, text=f"{discount:.0%}", font=FONT, bg=SECONDARY_BG_COLOR, anchor="e")
                discount_label.pack(side="top", anchor="ne", padx=10)
                discount_label.bind("<Button-1>", lambda event, id=partner_id: self.select_partner(id))


        except psycopg2.Error as e:
            print(f"Ошибка загрузки партнера: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def create_widgets(self):
        self.heading_label = tk.Label(self, text="Партнеры", font=HEADING_FONT, bg=BG_COLOR)
        self.heading_label.pack(pady=10)

        self.canvas = tk.Canvas(self, bg=BG_COLOR, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.partner_container = tk.Frame(self.canvas, bg=BG_COLOR)

        self.partner_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.partner_container, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.button_frame = tk.Frame(self, bg=BG_COLOR)
        self.button_frame.pack(pady=5)

        self.add_button = tk.Button(self.button_frame, text="Добавить партнера", font=FONT, bg=BUTTON_COLOR, command=self.open_add_partner_form)
        self.add_button.grid(row=0, column=0, padx=5)

        self.edit_button = tk.Button(self.button_frame, text="Изменить партнера", font=FONT, bg=BUTTON_COLOR, command=self.open_edit_partner_form)
        self.edit_button.grid(row=0, column=1, padx=5)

        self.refresh_button = tk.Button(self.button_frame, text="Обновить", font=FONT, bg=BUTTON_COLOR, command=self.load_partners)
        self.refresh_button.grid(row=0, column=2, padx=5)

        self.load_partners()

    def open_add_partner_form(self):
        AddEditPartnerForm(self.parent, self, partner_id=None)

    def open_edit_partner_form(self):
        if self.selected_partner_id is None:
            messagebox.showinfo("Важно!", "Пожалуйста, выберите партнера для редактирования.")
            return

        AddEditPartnerForm(self.parent, self, partner_id=self.selected_partner_id)
        self.selected_partner_id = None

    def select_partner(self, partner_id):
        self.selected_partner_id = partner_id
        print(f"Выбранный партнер: {partner_id}")

