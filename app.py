import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- 1. กำหนดตำแหน่งของประจุ (Electric Dipole) ---
q_pos = np.array([0.5, 0, 0])  # ประจุบวก
q_neg = np.array([-0.5, 0, 0]) # ประจุลบ

# --- 2. สร้าง Mesh Grid สำหรับพิกัด ---
# สร้างช่วงพิกัด
span = 1.5
n = 10 # จำนวนจุดในแต่ละแกน (ยิ่งมากยิ่งละเอียด)
x_lim = np.linspace(-span, span, n)
y_lim = np.linspace(-span, span, n)
z_lim = np.linspace(-span, span, n)
X, Y, Z = np.meshgrid(x_lim, y_lim, z_lim)

# กำหนดขนาดของสนามเวกเตอร์เริ่มต้นเป็นศูนย์
U, V, W = np.zeros((n, n, n)), np.zeros((n, n, n)), np.zeros((n, n, n))

# --- 3. คำนวณสนามไฟฟ้า (E-Field) ณ ทุกจุด (กฎของคูลอมบ์) ---
def calculate_e_field(charge_pos, X, Y, Z, sign=1):
    """คำนวณสนามไฟฟ้าจากประจุจุดเดียว"""
    # ตำแหน่งของจุดที่ต้องการคำนวณสนาม
    R_x = X - charge_pos[0]
    R_y = Y - charge_pos[1]
    R_z = Z - charge_pos[2]

    # ระยะทางจากประจุถึงจุดคำนวณ (r^2)
    R_sq = R_x**2 + R_y**2 + R_z**2
    # ป้องกันการหารด้วยศูนย์ที่ตำแหน่งของประจุ
    R_sq[R_sq < 1e-6] = 1e-6

    # ความแรงของสนาม (E proportional to 1/r^2)
    E_mag = sign / R_sq**1.5

    # ส่วนประกอบของเวกเตอร์สนาม (E = E_mag * R / r)
    E_x = E_mag * R_x
    E_y = E_mag * R_y
    E_z = E_mag * R_z
    return E_x, E_y, E_z

# สนามจากประจุบวก
E_pos_x, E_pos_y, E_pos_z = calculate_e_field(q_pos, X, Y, Z, sign=1)
# สนามจากประจุลบ (ทิศทางตรงกันข้ามกับประจุบวก)
E_neg_x, E_neg_y, E_neg_z = calculate_e_field(q_neg, X, Y, Z, sign=-1)

# สนามไฟฟ้ารวม (Superposition Principle)
U = E_pos_x + E_neg_x
V = E_pos_y + E_neg_y
W = E_pos_z + E_neg_z

# --- 4. การแสดงผลด้วย Quiver Plot 3D ---
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# วาด Quiver Plot
ax.quiver(
    X, Y, Z,
    U, V, W,
    length=0.2,
    normalize=True,   # ทำให้ลูกศรแสดงทิศทางหลักชัดเจน
    color='purple',
    alpha=0.7
)

# วาดจุดประจุ
ax.scatter(q_pos[0], q_pos[1], q_pos[2], color='red', marker='o', s=100, label='+ Charge')
ax.scatter(q_neg[0], q_neg[1], q_neg[2], color='blue', marker='o', s=100, label='- Charge')

# --- 5. การตกแต่ง ---
ax.set_title('Electric Dipole Field (Electrostatics)', fontsize=16, color='darkgreen')
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
ax.set_xlim([-span, span])
ax.set_ylim([-span, span])
ax.set_zlim([-span, span])
ax.legend()

