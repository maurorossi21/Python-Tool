import pyfiglet
import socket
import threading
import ipaddress
import time
import requests
import os 
import string
import random
from  rich.live import Live
from rich.panel import Panel 
from rich.table import Table 
from rich.console import Console


# INITIALIZE CONSOLE // OBJECT
console = Console()

#store the console size in a variable
console_width = console.size.width

#Global variable/Target IP
target = ""

login = pyfiglet.figlet_format("Admin LOGIN")
panel_domain = Panel(login, style= "bold purple", border_style="bold white", width=console_width)
console.print(panel_domain)
print("\n\n")
                
def get_admin_by_user(users, user_input):
    for admin in users:
        if admin["user"] == user_input:
            return admin
    return None

def validate_email(admin, email_input):
    return admin["email"] == email_input

def validate_password(admin, password_input):
    return admin["password"] == password_input

admins = [
    {"user": "maurofranco","email": "mrf21@gmail.com", "password": "vespa"},
    {"user": "nicolefranco","email": "nicolesantos24@gmail.com", "password": "golden"},
    {"user": "tomashenriques","email": "tomasvespa@gmail.com", "password": "jimmy"},
]


admin = None
while not admin:
    prompt = input("Enter your Username: ")
    admin = get_admin_by_user(admins, prompt)
    if not admin:
        print("Invalid user. Please try again.")
    else:
        print(f"Welcome you are logged as an admin, {admin['user']}")
        
while True:
    prompt2 = input("Enter your email please: ")
    if validate_email(admin, prompt2):
        print("Email corresponds to an admin.")
        break
    else:
        print("Invalid email. Please try again.")

while True:
    prompt3 = input("Enter your password: ")
    if validate_password(admin, prompt3):
        print("Password is correct. Welcome, admin!")
        os.system("clear" if os.name == "posix" else "cls")
        break
    else:
        print("Invalid password. Please try again.")


def user():
    global target

    first_option = 1
    second_option = 2
    third_option = 3
    forth_option = 4
    

    # Main header
    name = pyfiglet.figlet_format("Made by Cod3r V2 Developer")
    footer_text = "[bold cyan]Cod3r Script - 1.2[/bold cyan]"
    panel_content = f"{name.strip()}\n\n{footer_text}"
    panel_head = Panel(panel_content, style="bold red", border_style="bold red", width=console_width)
    console.print(panel_head)
    print("\n\n")  # Console space    

   


    menu = pyfiglet.figlet_format("Menu")
    panel_domain = Panel(f"{menu}\n1-Port Scanner \n2-Host \n3-Ping a Target \n4-Safe Passowrd Generator", border_style="bold green", width=console_width, style="bold green")
    console.print(panel_domain)
    print("\n\n")



    
    while True:
        try:
            # Prompt for user input
            select_option = int(console.input("[bold red]Select an option: [/bold red]"))

            os.system("clear" if os.name == "posix" else "cls")


            if select_option == first_option:
                name = pyfiglet.figlet_format("Port Scanner")
                panel_head = Panel(name, style="bold white", border_style="bold white", width=console_width)
                console.print(panel_head)
                print("\n\n")  # Console space

                # Collect target IP
                target_ip = console.input("[bold yellow]Enter the Target IP: [/bold yellow]")
                target = str(ipaddress.ip_address(target_ip))  # Validate IP
                console.print(f"Scanning Now {target}...")
                threader()

                return  # Exit the loop after setting the target
            elif select_option == second_option:
                host_lookup()
                return
            elif select_option == third_option:
                ping_target()
                return
            elif select_option == forth_option:
                safe_password()
            else:
                console.print("[bold red]Invalid option! Please select a valid option.[/bold red]")
        except Exception as e:
            console.print(f"[bold red]Invalid IP: {e}, Please enter a valid IP.[/bold red]")
        


def return_to_menu():
    console.input("[bold blue]Press any key to return to the main menu...[/bold blue]")
    os.system("clear" if os.name == "posix" else "cls")
    user()
    

def host_lookup():
   global target
   name = pyfiglet.figlet_format("Find Website IP")
   panel_head = Panel(name, style="bold purple", border_style="bold purple", width=console_width)
   console.print(panel_head)
   print("\n\n")  # Console space

   while True:
       
       try: 
           #Prompt the user to enter the Website
           website = console.input("[bold yellow] Enter the Website (e.g., www.example.com): [/bold yellow]")

           #Get The Ip address from the website
           ip_address = socket.gethostbyname(website)

           table = Table(title="Website Infos", style="bold purple", header_style="bold red" )
           table.add_column("Domain", justify="center", style="bold yellow")
           table.add_column("IP Target", justify="center", style="bold purple")

           table.add_row(website, ip_address)

           console.print(table)

           geo_lookup(ip_address)
           subdomain_lookup(website)
            

           # Update the global target with the resolved IP
           target = ip_address

           # Automatically start port scanning after getting the IP
           console.print(f"Now starting port scan on {target}...")
           threader()  # Run the port scanne

           return_to_menu()
           return
       except socket.gaierror as e:
           console.print(f"[bold red]Error resolving hostname: {e} [/bold red]")
       except Exception as e:
           console.print(f"[bold red]Unexpected error: {e} [/bold red]")


def geo_lookup(ip_address):


    try:
        # Fetch Geo Information using ipinfo.io (replace with your preferred API)
        response = requests.get(f"http://ipinfo.io/{ip_address}/json").json()

        # Extract relevant details
        city = response.get("city", "N/A")
        region = response.get("region", "N/A")
        country = response.get("country", "N/A")
        location = response.get("loc", "N/A")  # Latitude and Longitude
        org = response.get("org", "N/A")
        postal = response.get("postal", "N/A")

        # Create a Rich table for GeoLookup
        table = Table(title="GeoLookup Information", style="bold blue", header_style="bold white")
        table.add_column("Field", justify="left", style="bold blue")
        table.add_column("Value", justify="center", style="bold green")

        # Add rows to the table
        table.add_row("City", city)
        table.add_row("Region", region)
        table.add_row("Country", country)
        table.add_row("Location (Lat, Lon)", location)
        table.add_row("Organization", org)
        table.add_row("Postal Code", postal)

        # Display the table
        console.print(table)

    except requests.RequestException as e:
        console.print(f"[bold red]Error fetching GeoLookup data: {e}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Unexpected error: {e}[/bold red]")
           

def subdomain_lookup(domain):
    try:
        # VirusTotal API Key
        api_key = "afb3468ce46751169b2bbf933004c0ca6b8b6c41d270eef9646fd07aa74dfedc"
        headers = {"x-apikey": api_key}
        url = f"https://www.virustotal.com/api/v3/domains/{domain}/subdomains"

        # API Request
        response = requests.get(url, headers=headers)

        # Check HTTP status code
        if response.status_code != 200:
            console.print(f"[bold red]Error: Received status code {response.status_code} from VirusTotal API.[/bold red]")
            return

        # Parse JSON response
        data = response.json()
        subdomains = data.get("data", [])
        if not subdomains:
            console.print("[bold yellow]No subdomains found for this domain.[/bold yellow]")
            return

        # Create table for subdomains and their IPs
        table = Table(title=f"Subdomains and IPs for {domain}", style="bold blue", header_style="bold yellow")
        table.add_column("Subdomain", justify="center", style="bold white")
        table.add_column("IP Address", justify="center", style="bold green")

        # Add subdomains and their IPs to the table
        for subdomain in subdomains:
            subdomain_name = subdomain["id"]
            try:
                # Resolve IP address for the subdomain
                ip_address = socket.gethostbyname(subdomain_name)
            except socket.gaierror:
                ip_address = "[Error Resolving IP]"
            table.add_row(subdomain_name, ip_address)

        # Print the table
        console.print(table)

    except requests.RequestException as e:
        console.print(f"[bold red]Error connecting to VirusTotal API: {e}[/bold red]")
    except KeyError as e:
        console.print(f"[bold red]Unexpected data structure in API response: {e}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")


def port_scan(table, port):
    try:
        # Create a socket and attempt to connect to the target
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.5)  # Timeout for each connection attempt
            result = s.connect_ex((target, port))  # Check the port status
            if result == 0:  # Port is open
                table.add_row(f"{port}", "Open")  # Add only open ports to the table
    except Exception as e:
        # Log any unexpected errors (optional)
        pass  # Avoid cluttering the console with errors for closed ports


def threader():
   global target

   start_time = time.time()

   ports = range(1, 1024) #scanning only the first 1023 ports
   threads = []


   #create a rich table to display the result of the PORT and the STATUS 
   table = Table(title="Port Scan", style="bold purple", header_style="bold red")
   table.add_column("Ports", style="bold yellow")
   table.add_column("Status",style="bold green")


   #print the results live
   with Live(table, console=console, refresh_per_second=4 ):
      for port in ports:
            t = threading.Thread(target=port_scan, args=(table, port))  # Pass the correct function and args
            threads.append(t)
            t.start()
      for thread in threads:
         thread.join() #wait for all threads

   total_time = time.time() - start_time # Calculate elapsed time


   #print completion message
   console.print(f"Scan Completed in {total_time:.2f} seconds ")
   panel = Panel("Port Scan Completed", style="bold green", border_style="bold green", width=console_width)
   console.print(panel)

   return_to_menu()

def ping_target():

    name = pyfiglet.figlet_format("Ping Target")
    panel_head = Panel(name, style="bold blue", border_style="bold blue", width=console_width)
    console.print(panel_head)   
    
    try:
        #prompt for target Ip or hostname
        target = console.input("[bold yellow] Enter the IP to Ping (IP/Domain): [/bold yellow] ")
        response = os.system(f"ping -c 12 {target}" if os.name == "posix" else f"ping -n 12 {target}")

        if response == 0:
            console.print(f"[bold green]Target{target} is reachable![/bold green]")
        else:
            console.print(f"[bold red]Target{target} is not reachable![/bold red]")

    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
    return_to_menu()



def safe_password():

    name = pyfiglet.figlet_format("Safe Password")
    panel_head = Panel(name, style="bold yellow", border_style="bold yellow", width=console_width)
    console.print(panel_head)

    table = Table(title="Generated Password", style="bold purple", header_style="bold red")
    table.add_column("Password", style="bold yellow")


    while True:
        try:
            #solicitar comprimento da senha
            lenght = int(console.input("[bold yellow]Enter the desired password lenght: [/bold yellow]"))
            if lenght < 6:
                console.print("[bold red] The password needs to have at least 6 characters [/bold red]")
                continue
            
            #password generator
            characters = string.ascii_letters + string.digits + string.punctuation
            password = "".join(random.choice(characters) for _ in range (lenght))

            table.add_row(password)
            console.print(table)

            # show the password
            console.print(f"[bold green] Generated Password: {password} [/bold green]")
            return_to_menu()

            return

        except ValueError:
            console.print("[bold red]Invalid input. Please enter a valid number![/bold red]")
        except Exception as e:
            console.print(f"[bold red]Unexpected error: {e}[/bold red]")
        

user()
