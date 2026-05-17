import customtkinter as ctk
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ===== FUNCTIONS =====

def run_edge():
    output.insert("end", "\n[+] Running Edge Simulator...\n")
    os.system("python edge_simulator.py")

def run_encrypt():
    output.insert("end", "\n[+] Running Encryption...\n")
    os.system("python encrypt_module.py")

def run_server():
    output.insert("end", "\n[+] Running Server...\n")
    os.system("python server_module.py")

def run_logs():
    output.insert("end", "\n[+] Verifying Logs...\n")
    os.system("python verify_logs.py")

def run_ai():
    output.insert("end", "\n[+] Running AI Analysis...\n")
    os.system("python ai_module.py")

def run_full():
    output.insert("end", "\n🚀 Running Full System...\n")
    run_edge()
    run_encrypt()
    run_server()
    run_logs()
    run_ai()
    output.insert("end", "\n✅ System Completed\n")


# ===== WINDOW =====

app = ctk.CTk()
app.title("Secure Edge Transmission System")
app.geometry("900x550")

# ===== TITLE =====

title = ctk.CTkLabel(app, text="🔐 Secure Edge Data Transmission Dashboard",
                     font=("Arial", 20, "bold"))
title.pack(pady=10)

# ===== FRAME =====

frame = ctk.CTkFrame(app)
frame.pack(pady=10, padx=10, fill="both", expand=True)

# ===== BUTTONS =====

btn_frame = ctk.CTkFrame(frame)
btn_frame.pack(side="left", fill="y", padx=10, pady=10)

ctk.CTkButton(btn_frame, text="Generate Data", command=run_edge).pack(pady=8)
ctk.CTkButton(btn_frame, text="Encrypt Data", command=run_encrypt).pack(pady=8)
ctk.CTkButton(btn_frame, text="Run Server", command=run_server).pack(pady=8)
ctk.CTkButton(btn_frame, text="Verify Logs", command=run_logs).pack(pady=8)
ctk.CTkButton(btn_frame, text="Run AI", command=run_ai).pack(pady=8)

ctk.CTkButton(btn_frame, text="🚀 Run Full System", fg_color="green",
              command=run_full).pack(pady=20)

# ===== OUTPUT AREA =====

output = ctk.CTkTextbox(frame, width=500)
output.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# ===== RUN =====

app.mainloop()