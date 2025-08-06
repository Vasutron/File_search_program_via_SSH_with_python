import paramiko
import config  # เปลี่ยนเป็นไฟล์ ใช้สำหรับกำหนดค่าการเชื่อมต่อ SSH

def search_file():
    print("File Search Program (Template)")
    print("=========================================")
    fd = input("Enter FolderName (Ex. Folder name): ").strip() # Format ชื่อ Folder หรือกำหนดเป็นอื่น ๆ ตามต้องการค้นหาจากชื่อFolder อะไร
    yyyymmdd = input("Enter date (YYYYMMDD): ").strip() # Format YYYYMMDD หรือกำหนดเป็นอื่น ๆ ตามต้องการค้นหาจากชื่อไฟล์
    print("=========================================")

    hostname = config.hostname
    username = config.username
    password = config.password

    # กำหนด path สำหรับค้นหาไฟล์ (ให้ผู้ใช้กรอกเอง)
    remote_path = input("Enter remote path (Ex. /path/to/files): ").strip()

    def run_ssh_command(ssh, command):
        stdin, stdout, stderr = ssh.exec_command(command)
        return stdout.read().decode().strip(), stderr.read().decode().strip()
    
    command = f'find {remote_path}/{fd} -type f | grep {yyyymmdd}'
    count_command = f'find {remote_path}/{fd} -maxdepth 1 -type f | wc -l'
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password, timeout=10)

        result, error = run_ssh_command(ssh, command)
        file_count, _ = run_ssh_command(ssh, count_command)

        if result:
            print("========== ShowFile ==========")
            print(result)
            print("========== ======== ==========")
            print(f"Summary file in {remote_path}/{fd} found: {file_count}")
            print("========== ======== ==========")
            input("Press Enter to continue...")
        else:
            print("No file found matching criteria.")
        if error:
            print("Error:", error)
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_file()
