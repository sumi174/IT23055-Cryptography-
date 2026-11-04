
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import subprocess
import threading
from pathlib import Path
from datetime import datetime

LAYERS = [
    "Application",
    "Presentation",
    "Session",
    "Transport",
    "Network",
    "Data Link",
    "Physical"
]

# Project directory and C client path
PROJECT_DIR = Path(__file__).resolve().parent.parent
CLIENT_PATH = PROJECT_DIR / "client.exe"

class OSISimulationGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("OSI 7 Layer Communication Simulation")
        self.root.geometry("1000x760")
        self.root.minsize(850, 650)
        self.root.configure(bg="#101827")

        self.step = 0
        self.busy = False
        self.message = ""

        self.build_gui()

    def build_gui(self):
        # Header
        header = tk.Frame(self.root, bg="#101827")
        header.pack(fill="x", pady=15)

        tk.Label(
            header,
            text="OSI 7 LAYER SIMULATION",
            font=("Arial", 23, "bold"),
            fg="#38BDF8",
            bg="#101827"
        ).pack()

        tk.Label(
            header,
            text="Client - Server Communication Visualization",
            font=("Arial", 11),
            fg="#CBD5E1",
            bg="#101827"
        ).pack(pady=5)

        self.date_label = tk.Label(
            header,
            text="Date & Time: " + datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            font=("Arial", 10),
            fg="#94A3B8",
            bg="#101827"
        )
        self.date_label.pack(pady=3)

        # Message input
        input_frame = tk.Frame(self.root, bg="#1E293B", padx=15, pady=12)
        input_frame.pack(fill="x", padx=25, pady=10)

        tk.Label(
            input_frame,
            text="Enter Your Message:",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#1E293B"
        ).pack(anchor="w")

        self.message_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            bg="#F8FAFC",
            fg="#111827"
        )
        self.message_entry.pack(fill="x", pady=8)
        self.message_entry.bind("<Return>", lambda event: self.start_simulation())

        self.send_button = tk.Button(
            input_frame,
            text="START SIMULATION",
            font=("Arial", 11, "bold"),
            bg="#0284C7",
            fg="white",
            activebackground="#0369A1",
            command=self.start_simulation,
            padx=15,
            pady=7,
            cursor="hand2"
        )
        self.send_button.pack(pady=5)

        # Layer visualization
        main_frame = tk.Frame(self.root, bg="#101827")
        main_frame.pack(fill="both", expand=True, padx=25, pady=10)

        tk.Label(
            main_frame,
            text="SENDER",
            font=("Arial", 14, "bold"),
            fg="#38BDF8",
            bg="#101827"
        ).grid(row=0, column=0, pady=10)

        tk.Label(
            main_frame,
            text="DATA FLOW",
            font=("Arial", 12, "bold"),
            fg="#FACC15",
            bg="#101827"
        ).grid(row=0, column=1, padx=15)

        tk.Label(
            main_frame,
            text="RECEIVER",
            font=("Arial", 14, "bold"),
            fg="#4ADE80",
            bg="#101827"
        ).grid(row=0, column=2, pady=10)

        self.sender_boxes = []
        self.receiver_boxes = []

        for i, layer in enumerate(LAYERS):

            sender = tk.Label(
                main_frame,
                text=f"Layer {7-i}: {layer}",
                font=("Arial", 10, "bold"),
                bg="#334155",
                fg="white",
                width=28,
                height=2,
                relief="ridge",
                bd=2
            )
            sender.grid(row=i+1, column=0, padx=8, pady=4)
            self.sender_boxes.append(sender)

            arrow = tk.Label(
                main_frame,
                text="⇄",
                font=("Arial", 20, "bold"),
                bg="#101827",
                fg="#64748B"
            )
            arrow.grid(row=i+1, column=1, padx=15)
            
            receiver = tk.Label(
                main_frame,
                text=f"Layer {i+1}: {LAYERS[6-i]}",
                font=("Arial", 10, "bold"),
                bg="#334155",
                fg="white",
                width=28,
                height=2,
                relief="ridge",
                bd=2
            )
            receiver.grid(row=i+1, column=2, padx=8, pady=4)
            self.receiver_boxes.append(receiver)

        # Progress
        progress_frame = tk.Frame(self.root, bg="#101827")
        progress_frame.pack(fill="x", padx=35, pady=5)

        self.status_label = tk.Label(
            progress_frame,
            text="Status: Waiting for message...",
            font=("Arial", 11, "bold"),
            fg="#FACC15",
            bg="#101827"
        )
        self.status_label.pack()

        self.progress = ttk.Progressbar(
            progress_frame,
            orient="horizontal",
            length=500,
            mode="determinate",
            maximum=7
        )
        self.progress.pack(fill="x", pady=8)

        # Output log
        tk.Label(
            self.root,
            text="Simulation Log",
            font=("Arial", 12, "bold"),
            fg="#38BDF8",
            bg="#101827"
        ).pack()

        self.log = ScrolledText(
            self.root,
            height=7,
            font=("Consolas", 9),
            bg="#020617",
            fg="#A7F3D0",
            insertbackground="white"
        )
        self.log.pack(fill="both", expand=True, padx=25, pady=8)

        self.write_log("OSI Simulation GUI Ready.")
        self.write_log("Enter a message and click START SIMULATION.")

    def write_log(self, text):
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)

    def reset_layers(self):
        for box in self.sender_boxes + self.receiver_boxes:
            box.config(bg="#334155", fg="white")

        self.progress["value"] = 0

    def start_simulation(self):
        if self.busy:
            return

        self.message = self.message_entry.get().strip()

        if not self.message:
            messagebox.showwarning(
                "Missing Message",
                "Please enter a message first."
            )
            return

        if not CLIENT_PATH.exists():
            messagebox.showerror(
                "Client Not Found",
                f"Cannot find client.exe:\n{CLIENT_PATH}"
            )
            return

        self.busy = True
        self.step = 0
        self.reset_layers()
        self.log.delete("1.0", tk.END)

        self.send_button.config(state="disabled")
        self.message_entry.config(state="disabled")

        self.status_label.config(
            text="Status: Sender encapsulation started...",
            fg="#38BDF8"
        )

        self.write_log("Date & Time: " + datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ))
        self.write_log("Message: " + self.message)
        self.write_log("\nSENDER: ENCAPSULATION")

        self.animate_encapsulation()

    def animate_encapsulation(self):
        if self.step >= 7:
            self.write_log("\nEncapsulation completed.")
            self.write_log("Starting C Client socket communication...")
            self.status_label.config(
                text="Status: Sending data to server...",
                fg="#FACC15"
            )

            threading.Thread(
                target=self.send_to_server,
                daemon=True
            ).start()
            return

        i = self.step
        self.sender_boxes[i].config(
            bg="#16A34A",
            fg="white"
        )

        layer_number = 7 - i
        self.write_log(
            f"Layer {layer_number}: {LAYERS[i]} - Encapsulation"
        )

        self.step += 1
        self.progress["value"] = self.step

        if self.step % 2 == 0 or self.step == 7:
            self.write_log(
                f">>> Progress: {self.step}/7 layers completed"
            )

        self.root.after(550, self.animate_encapsulation)

    def send_to_server(self):
        try:
            result = subprocess.run(
                [str(CLIENT_PATH), self.message],
                cwd=str(PROJECT_DIR),
                capture_output=True,
                text=True,
                timeout=30
            )

            output = result.stdout.strip()
            error = result.stderr.strip()

            self.root.after(
                0,
                lambda: self.handle_client_result(
                    result.returncode, output, error
                )
            )

        except subprocess.TimeoutExpired:
            self.root.after(
                0,
                lambda: self.handle_client_result(
                    1, "", "Connection timed out."
                )
            )

        except Exception as e:
            error_text = str(e)
            self.root.after(
                0,
                lambda: self.handle_client_result(
                    1, "", error_text
                )
            )

    def handle_client_result(self, returncode, output, error):
        if output:
            self.write_log("\nC Client Output:")
            self.write_log(output)

        if error:
            self.write_log("Error: " + error)

        if returncode != 0:
            self.write_log("\nClient failed!")
            self.write_log("Please check whether server.exe is running.")

            self.status_label.config(
                text="Status: Communication failed!",
                fg="#F87171"
            )
            self.finish_simulation()
            return

        self.write_log("\nServer communication successful!")
        self.write_log("\nRECEIVER: DECAPSULATION")

        self.step = 0
        self.status_label.config(
            text="Status: Receiver decapsulation started...",
            fg="#4ADE80"
        )

        self.animate_decapsulation()

    def animate_decapsulation(self):
        if self.step >= 7:
            self.write_log("\n" + "=" * 45)
            self.write_log("SIMULATION COMPLETED SUCCESSFULLY!")
            self.write_log("=" * 45)

            self.status_label.config(
                text="Status: SIMULATION COMPLETED!",
                fg="#4ADE80"
            )

            self.progress["value"] = 7
            self.finish_simulation()
            return

        i = self.step

        self.receiver_boxes[i].config(
            bg="#16A34A",
            fg="white"
        )

        layer_number = i + 1
        layer_name = LAYERS[6-i]

        self.write_log(
            f"Layer {layer_number}: {layer_name} - Decapsulation"
        )

        self.step += 1
        self.progress["value"] = self.step

        if self.step % 2 == 0 or self.step == 7:
            self.write_log(
                f">>> Progress: {self.step}/7 layers completed"
            )

        self.root.after(550, self.animate_decapsulation)

    def finish_simulation(self):
        self.busy = False
        self.send_button.config(state="normal")
        self.message_entry.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = OSISimulationGUI(root)
    root.mainloop()
