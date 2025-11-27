import numpy as np
import matplotlib.pyplot as plt
import streamlit as st # 1. Import Streamlit

# ====================
# การตั้งค่าแอป Streamlit
# ====================
st.title('⚡️ การจำลองสนามไฟฟ้าจากประจุ (Electric Field Simulation)')
st.write('แสดงสนามไฟฟ้าของระบบไดโพลไฟฟ้า (Electric Dipole) ในรูปแบบเวกเตอร์')

# ====================
# ค่าคงที่และคลาส (Constants and Class)
# ====================

# ค่าคงที่ของคูลอมบ์ (k)
k = 8.9875e9

class Charge:
    """Class สำหรับจัดเก็บข้อมูลตำแหน่งและปริมาณประจุ"""
    def __init__(self, position, charge_amount):
        self.position = np.array(position) # ตำแหน่ง [x, y]
        self.charge = charge_amount # ปริมาณประจุ (C)

# ====================
# ฟังก์ชันคำนวณ (Calculation Function)
# ====================

def calculate_E_field(k, q, r_vec):
    """คำนวณเวกเตอร์สนามไฟฟ้าจากประจุเดี่ยว E = k * q * r_unit / |r|^2"""
    r_mag = np.linalg.norm(r_vec)
    
    # หลีกเลี่ยงการหารด้วยศูนย์เมื่อจุดสังเกตตรงกับตำแหน่งประจุ
    if r_mag == 0:
        # อาจคืนค่าที่สูงมากหรือค่าที่จัดการได้ (0 ในที่นี้)
        return np.array([0.0, 0.0])
        
    r_unit = r_vec / r_mag
    E_mag = k * q / r_mag**2
    return E_mag * r_unit

# ====================
# การทำงานหลักของโปรแกรม (Main Program Logic)
# ====================

# การตั้งค่าประจุ (สามารถเปลี่ยนได้)
charges = [
    Charge([-0.4, 0], 1e-6), # ประจุบวก
    Charge([0.4, 0], -1e-6) # ประจุลบ
]

# สร้างตารางจุดสังเกต (Meshgrid)
# สามารถใช้ st.slider เพื่อให้ผู้ใช้ปรับจำนวนจุดได้
num_points = st.slider('จำนวนจุดในแต่ละแกน (Resolution)', 10, 50, 20)
x = np.linspace(-1, 1, num_points)
y = np.linspace(-1, 1, num_points)
X, Y = np.meshgrid(x, y)
Ex_total = np.zeros_like(X)
Ey_total = np.zeros_like(Y)

# คำนวณสนามไฟฟ้าที่แต่ละจุด
# ใช้ st.spinner เพื่อแสดงสถานะการโหลด
with st.spinner(f'กำลังคำนวณสนามไฟฟ้าในพื้นที่ {num_points}x{num_points}...'):
    for i in range(len(x)):
        for j in range(len(y)):
            obs_point = np.array([X[i, j], Y[i, j]])
            E_total = np.array([0.0, 0.0])
            
            # ใช้หลักการซ้อนทับ (Superposition)
            for charge in charges:
                r_vec = obs_point - charge.position
                E_total += calculate_E_field(k, charge.charge, r_vec)
            
            Ex_total[i, j] = E_total[0]
            Ey_total[i, j] = E_total[1]

# ====================
# การแสดงผลใน Matplotlib (Visualization)
# ====================

# ใช้วิธี Object-Oriented ของ Matplotlib โดยการสร้าง Figure object
fig, ax = plt.subplots(figsize=(6, 6))

# ปรับ scale ของลูกศรเพื่อการแสดงผลที่ดีขึ้น
ax.quiver(X, Y, Ex_total, Ey_total, scale=5e9, color='blue', alpha=0.8) 

# แสดงตำแหน่งประจุ
for charge in charges:
    color = 'red' if charge.charge > 0 else 'blue'
    ax.plot(charge.position[0], charge.position[1], 'o', color=color, markersize=8)
    ax.text(charge.position[0] + 0.05, charge.position[1] + 0.05, 
            f'Q={charge.charge:.1e}C', fontsize=8) # เพิ่มข้อความกำกับ

# ตั้งค่ากราฟ
ax.set_title('Electric Field Vector Map (E-Dipole)')
ax.set_xlabel('X position (m)')
ax.set_ylabel('Y position (m)')
ax.set_aspect('equal') # ทำให้แกน X และ Y มีสัดส่วนเท่ากัน
ax.grid(True, linestyle=':', alpha=0.6)

# 2. แสดง Figure object ใน Streamlit แทน plt.show()
st.pyplot(fig) 

# แสดงข้อมูลเพิ่มเติม
st.subheader("ข้อมูลการจำลอง")
st.code(f"ประจุ 1: ตำแหน่ง {charges[0].position}, ปริมาณ {charges[0].charge} C (สีแดง)")
st.code(f"ประจุ 2: ตำแหน่ง {charges[1].position}, ปริมาณ {charges[1].charge} C (สีน้ำเงิน)")
st.caption(f"ค่าคงที่คูลอมบ์ (k) = {k:.4e} N·m²/C²")
