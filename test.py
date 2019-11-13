from SSHClient import SSHClient

def main():
    ssh = SSHClient("192.168.1.100", 22, "root", "xxxx")
    res = ssh.exec_command("pwd")
    print(res)
    res = ssh.exec_command("cd /etc; cat hosts")
    print(res)
    res = ssh.exec_command("pwd")
    print(res)
    res = ssh.exec_command("more /etc/passwd")
    print(res)
        
if "__main__"==__name__:
    main()
    