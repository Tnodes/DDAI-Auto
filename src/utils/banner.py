from tabulate import tabulate

def print_banner():
    banner_data = [
        ["DDAI BOT"],
        ["Automated Referral & Auto Ping Extension"],
        ["Author: Tnodes"]
    ]
    
    print("\n" + tabulate(banner_data, tablefmt="grid", numalign="center", stralign="center"))
    print()