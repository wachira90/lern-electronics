#!python
import tkinter as tk
from tkinter import ttk

def update_calculations(*args):
    """ฟังก์ชันนี้จะทำงานอัตโนมัติเมื่อมีการเลื่อน Slider หรือเปลี่ยนค่าใน Dropdown"""
    # ดึงค่าปัจจุบันจาก UI
    v_in = voltage_scale.get()
    r = resistor_scale.get()
    
    # ตรวจสอบชนิดของ LED เพื่อกำหนดแรงดันตกคร่อม (Vf)
    led_type = led_var.get()
    if "2.0V" in led_type:
        v_f = 2.0
    else:
        v_f = 3.0
        
    # ป้องกันกรณีผู้ใช้ปรับ V_in ต่ำกว่า V_f
    if v_in <= v_f:
        current_ma = 0.0
        power_mw = 0.0
        status = "แรงดันไฟจ่ายไม่พอ (Voltage too low)"
        color = "red"
    else:
        # คำนวณกระแส (mA) และ กำลังไฟ (mW)
        current_ma = ((v_in - v_f) / r) * 1000
        power_mw = (v_in - v_f) * (current_ma / 1000) * 1000
        
        # ประเมินระดับความสว่าง
        if current_ma < 1:
            status = "สว่างน้อยมาก / หรี่ (Very Dim)"
            color = "gray"
        elif 1 <= current_ma <= 5:
            status = "สว่างพอดี / กินกระแสน้อย (Dim/Low Power)"
            color = "green"
        elif 5 < current_ma <= 15:
            status = "สว่างปานกลาง (Normal)"
            color = "blue"
        else:
            status = "สว่างมาก (Bright)"
            color = "#d62728" # สีแดง
            
    # อัปเดตผลลัพธ์บนหน้าจอ
    lbl_current_result.config(text=f"{current_ma:.2f} mA")
    lbl_power_result.config(text=f"{power_mw:.2f} mW")
    lbl_status_result.config(text=status, fg=color)

# ==========================================
# การสร้างหน้าต่าง GUI หลัก (Main Window)
# ==========================================
root = tk.Tk()
root.title("LED Resistor Calculator")
root.geometry("450x550")
root.configure(padx=20, pady=20)

# กำหนดสไตล์ฟอนต์
font_title = ("Helvetica", 14, "bold")
font_label = ("Helvetica", 12)
font_result = ("Helvetica", 16, "bold")

# --- ส่วนที่ 1: แรงดันไฟจ่าย (V) ---
tk.Label(root, text="แรงดันไฟจ่าย (Source Voltage)", font=font_label).pack(anchor="w", pady=(0, 5))
voltage_scale = tk.Scale(
    root, from_=5, to=24, orient="horizontal", resolution=1, 
    length=400, command=update_calculations, font=font_label
)
voltage_scale.set(12) # ค่าเริ่มต้น 12V
voltage_scale.pack(pady=(0, 15))

# --- ส่วนที่ 2: ชนิด/สีของหลอด LED ---
tk.Label(root, text="ชนิด/สีของหลอด LED (LED Type)", font=font_label).pack(anchor="w", pady=(0, 5))
led_var = tk.StringVar()
led_combo = ttk.Combobox(
    root, textvariable=led_var, state="readonly", font=font_label,
    values=["แดง/เหลือง/เขียว (2.0V)", "ขาว/น้ำเงิน (3.0V)"]
)
led_combo.current(0) # เลือกค่าแรกเป็นเริ่มต้น
led_combo.bind("<<ComboboxSelected>>", update_calculations)
led_combo.pack(fill="x", pady=(0, 15))

# --- ส่วนที่ 3: ค่าความต้านทาน (Ohm) ---
tk.Label(root, text="ค่าความต้านทาน (Resistance - โอห์ม)", font=font_label).pack(anchor="w", pady=(0, 5))
resistor_scale = tk.Scale(
    root, from_=500, to=20000, orient="horizontal", resolution=100, 
    length=400, command=update_calculations, font=font_label
)
resistor_scale.set(4700) # ค่าเริ่มต้น 4700 โอห์ม (4.7k)
resistor_scale.pack(pady=(0, 20))

# --- เส้นคั่น ---
ttk.Separator(root, orient="horizontal").pack(fill="x", pady=10)

# --- ส่วนที่ 4: แสดงผลลัพธ์ (Results) ---
tk.Label(root, text="กระแสไฟฟ้าที่ไหลผ่าน:", font=font_label).pack(pady=(10, 0))
lbl_current_result = tk.Label(root, text="0.00 mA", font=font_result, fg="blue")
lbl_current_result.pack()

tk.Label(root, text="กำลังไฟที่ตัวต้านทานรับภาระ:", font=font_label).pack(pady=(10, 0))
lbl_power_result = tk.Label(root, text="0.00 mW", font=font_result, fg="orange")
lbl_power_result.pack()

tk.Label(root, text="ระดับความสว่าง:", font=font_label).pack(pady=(10, 0))
lbl_status_result = tk.Label(root, text="-", font=font_result)
lbl_status_result.pack()

# เรียกใช้ฟังก์ชันครั้งแรกเพื่อคำนวณค่าเริ่มต้น
update_calculations()

# เริ่มการทำงานของโปรแกรม
root.mainloop()
