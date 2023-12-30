import os
import paramiko
from scp import SCPClient
import sys
import time

def create_ssh_client(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(server, port, user, password)
        return client, None
    except paramiko.AuthenticationException:
        return None, "Authentication failed. Check your username/password."
    except paramiko.SSHException as e:
        return None, f"SSH connection error: {e}"

def execute_ssh_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode(), stderr.read().decode()

def select_app(app_paths):
    for idx, path in enumerate(app_paths, 1):
        print(f"{idx}. {path}")
    while True:
        try:
            choice = int(input("Select the app number you want to process: "))
            if 1 <= choice <= len(app_paths):
                return app_paths[choice - 1]
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a number.")

def print_progress_bar(step, total_steps, bar_length=50):
    percentage = (step / total_steps)
    filled_length = int(round(bar_length * percentage))
    # Define the Christmas color code (green)
    color_code = '\033[92m'  # Green for Christmas trees
    # Emoji for the slider
    slider = '🎅'  # Santa Claus emoji
    # Emoji for the filled part of the progress bar
    tree = '🎄'  # Christmas tree emoji
    bar = color_code + tree * filled_length + ' ' * (bar_length - filled_length) + "\033[0m"
    sys.stdout.write(f"\r{slider} Progress: |{bar}| {percentage:.2%}")
    sys.stdout.flush()

def main():
    server = "127.0.0.1"
    port = 2222
    user = "root"
    default_password = "alpine"

    ssh, error = create_ssh_client(server, port, user, default_password)
    if error:
        print("Default password failed. " + error)
        password = input("Enter your SSH password: ")
        ssh, error = create_ssh_client(server, port, user, password)
        if error:
            print(error)
            print("Exiting the script.")
            return
    else:
        print("Connection successful.")

    app_name = input("Enter the partial name of the app you want to test (e.g., 'Tele' for 'Telegram'): ")
    find_command = f"find /var/containers/Bundle/Application -type d -iname '{app_name}*.app'"
    app_paths, err = execute_ssh_command(ssh, find_command)
    if err:
        print(f"Error finding app: {err}")
        ssh.close()
        return

    app_paths = [path for path in app_paths.strip().split('\n') if path]
    if not app_paths:
        print("No app found with that name.")
        ssh.close()
        return

    app_path = select_app(app_paths)
    print(f"Selected app: {app_path}")
    output_ipa_name = os.path.basename(app_path).replace('.app', '.ipa')

    commands = [
        "mkdir -p Payload",
        f"cp -R {app_path} Payload",
        "zip -r Payload.zip Payload",
        "mv Payload.zip /var/containers/Bundle/",
        f"mv /var/containers/Bundle/Payload.zip /var/containers/Bundle/{output_ipa_name}"
    ]

    total_steps = len(commands) + 1  # Plus one for the SCP transfer
    current_step = 0

    for command in commands:
        current_step += 1
        print_progress_bar(current_step, total_steps)  # Print progress before executing the command
        output, err = execute_ssh_command(ssh, command)
        if err:
            print(f"\nError executing command '{command}': {err}")
            ssh.close()
            return
        time.sleep(0.5)  # Simulate a delay for the command execution

    current_step += 1
    print_progress_bar(current_step, total_steps)
    app_folder_name = output_ipa_name.replace('.ipa', '')
    local_app_folder = os.path.expanduser(f"~/IpaExtractionSuite/{app_folder_name}")
    os.makedirs(local_app_folder, exist_ok=True)
    local_ipa_path = os.path.join(local_app_folder, output_ipa_name)

    with SCPClient(ssh.get_transport()) as scp:
        scp.get(f"/var/containers/Bundle/{output_ipa_name}", local_ipa_path)
    print_progress_bar(total_steps, total_steps)  # Complete the progress bar

    print(f"\nIPA file '{output_ipa_name}' transferred successfully to {local_ipa_path}.")
    ssh.close()

if __name__ == "__main__":
    main()
