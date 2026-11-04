
import subprocess
import time
from datetime import datetime

layers = [
    "Application",
    "Presentation",
    "Session",
    "Transport",
    "Network",
    "Data Link",
    "Physical"
]

def show_layers(title, layer_list):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)

    for i, layer in enumerate(layer_list, 1):
        print(f"Layer {7-i+1 if 'ENCAPSULATION' in title else i}: {layer}")
        time.sleep(0.4)

        if i % 2 == 0 or i == len(layer_list):
            print(f">>> Progress: {i}/{len(layer_list)} layers completed")

def main():
    print("=" * 50)
    print("       OSI 7 LAYER SIMULATION")
    print("=" * 50)

    print("Date & Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    message = input("\nEnter your message: ")

    print("\nSENDER: ENCAPSULATION")
    show_layers("ENCAPSULATION: Layer 7 to Layer 1", layers)

    print("\nStarting C Client...")
    result = subprocess.run(
        ["./client.exe", message],
        capture_output=False
    )

    if result.returncode != 0:
        print("\nClient failed! Check whether the server is running.")
        return

    print("\nRECEIVER: DECAPSULATION")
    show_layers(
        "DECAPSULATION: Layer 1 to Layer 7",
        list(reversed(layers))
    )

    print("\n" + "=" * 50)
    print("       SIMULATION COMPLETED!")
    print("=" * 50)

if __name__ == "__main__":
    main()
