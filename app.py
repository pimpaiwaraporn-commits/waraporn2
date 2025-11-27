import numpy as np
import matplotlib.pyplot as plt

# ค่าคงที่ของคูลอมบ์ (k) 
k = 8.9875e9 

class Charge:
    def __init__(self, position, charge_amount):
        self.position = np.array(position) # ตำแหน่ง [x, y]
        self.charge = charge_amount # ปริมาณประจุ (C)

def calculate_E_field(k, q, r_vec):
    # E = k * q * r_unit / |r|^2
    r_mag = np.linalg.norm(r_vec)
    if r_mag == 0:
        return np.array([0.0, 0.0])
    r_unit = r_vec / r_mag
    E_mag = k * q / r_mag**2
    return E_mag * r_unit

# การตั้งค่า
charges = [
    Charge([-0.4, 0], 1e-6), # ประจุบวก
    Charge([0.4, 0], -1e-6) # ประจุลบ
]

# สร้างตารางจุดสังเกต (Meshgrid)
x = np.linspace(-1, 1, 20)
y = np.linspace(-1, 1, 20)
X, Y = np.meshgrid(x, y)
Ex_total = np.zeros_like(X)
Ey_total = np.zeros_like(Y)

# คำนวณสนามไฟฟ้าที่แต่ละจุด
for i in range(len(x)):
    for j in range(len(y)):
        obs_point = np.array([X[i, j], Y[i, j]])
        E_total = np.array([0.0, 0.0])
        
        for charge in charges:
            r_vec = obs_point - charge.position
            E_total += calculate_E_field(k, charge.charge, r_vec)
        
        Ex_total[i, j] = E_total[0]
        Ey_total[i, j] = E_total[1]

# การแสดงผล (Visualization)
plt.figure(figsize=(6, 6))
plt.quiver(X, Y, Ex_total, Ey_total, scale=5e9, color='blue') # สร้างแผนภูมิเวกเตอร์

for charge in charges:
    color = 'red' if charge.charge > 0 else 'blue'
    plt.plot(charge.position[0], charge.position[1], 'o', color=color, markersize=8)

plt.title('Electric Field Vector Map')
plt.xlabel('X position')
plt.ylabel('Y position')
plt.show()
   
