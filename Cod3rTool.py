# THREADED PORT SCANNER

# IMPORTS
import threading
import socket
from rich.live import Live
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import ipaddress  # EXTRA TO VALIDATE THE IP
import pyfiglet
import time

# INITIALIZE CONSOLE // OBJECT
console = Console()
# STORE THE CONSOLE SIZE IN A VARIABLE
console_width = console.size.width

# GLOBAL VARIABLE // TARGET IP
target = ""


# COLLECT USER INPUT
def user():
    global target

    first_option = 1
    second_option = 2 

    # MAIN HEADER
    name = pyfiglet.figlet_format("Made by Cod3r V2 Scanner")
    panel_head = Panel(name, style="bold red", border_style="bold red", width=console_width)
    console.print(panel_head)
    print("\n\n")  # CONSOLE SPACE

    domain = pyfiglet.figlet_format("Instructions")
    panel_domain = Panel(f"{domain}\n1-Port Scanner \n2-Host \n", border_style="bold yellow", width=console_width, style="bold yellow")
    console.print(panel_domain)
    print("\n\n")
        
    while True:
        try:
            select_option = int(console.input("[bold red]Select an option:[/bold red]"))
            target_ip = (console.input("[bold red]Enter the Target IP:[/bold red] "))
            target = str(ipaddress.ip_address(target_ip))  # Validate and convert to string
            if select_option == first_option:
                console.print(f"Now Scanning {target}...")
                return
            elif select_option == second_option:    
                console.print("Host option is not implemented yet!")
            
                console.print(f"Now Scanning {target}...")
                return
        except Exception as e:
            console.print(f"INVALID IP: {e}, Please try again!")


# FUNCTION TO SCAN A SINGLE PORT
def port_scan(table, port):
    global target

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.5)
            result = s.connect_ex((target, port))
            if result == 0:
                table.add_row(f"{port}", "OPEN")  # Add open port to the table
    except socket.gaierror as e:
        console.print(f"[bold red]Socket error: {e}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")


# THREADING FUNCTION
def threader():
    global target

    start_time = time.time()

    ports = range(1, 1024)  # Scanning only the first 1023 ports (well-known ports)
    threads = []

    # Create a Rich table to display results
    table = Table(title="Port Scan", style="bold purple", header_style="bold red")
    table.add_column("Port", style="bold yellow")
    table.add_column("Status", style="bold green")

    # PRINT RESULTS LIVE
    with Live(table, console=console, refresh_per_second=4):
        for port in ports:
            t = threading.Thread(target=port_scan, args=(table, port))  # Pass the correct function and args
            threads.append(t)  # Add threads to list
            t.start()  # Start each thread

        for thread in threads:
            thread.join()  # Wait for all threads to complete

    total_time = time.time() - start_time  # Calculate elapsed time

    # Print completion message
    console.print(f"Scan Complete in {total_time:.2f} seconds")
    panel = Panel("Port scan completed", style="bold green", border_style="bold green", width=console_width)
    console.print(panel)


# MAIN PROGRAM
user()
threader()



