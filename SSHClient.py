#encoding:utf-8
import paramiko
import time

class SSHClient():
    def __init__(self, hostname, port=22, username=None, password=None, pkey=None, key_filename=None, timeout=None, allow_agent=True, look_for_keys=True, compress=False, sock=None, gss_auth=False, gss_kex=False, gss_deleg_creds=True, gss_host=None, banner_timeout=None, auth_timeout=None, gss_trust_dns=True, passphrase=None, disabled_algorithms=None):
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #self.ssh.connect(hostname, port, username, password, pkey, key_filename, timeout, allow_agent, look_for_keys, compress, sock, gss_auth, gss_kex, gss_deleg_creds, gss_host, banner_timeout, auth_timeout, gss_trust_dns, passphrase, disabled_algorithms)
        self.ssh.connect(hostname, port, username, password)
        
    def exec_command(self, cmd, pause_time=0.05):
        cmd+="\n"
        transport = self.ssh.get_transport()
        channel = transport.open_session()
        #channel.get_pty(width=256, height=20) #宽度、高度的设置对more有用，但对cat没用，可能需要命令自身支持
        channel.get_pty(width=10240, height=10240)
        channel.exec_command(cmd) #可以和exit_status_ready配合
        
        #channel.invoke_shell() #似乎不能和exit_status_ready配合
        #channel.send(cmd)
        
        buff_size = 1024
        stdout = b""
        stderr = b""
        
        while not channel.exit_status_ready():
            time.sleep(pause_time)
            if channel.recv_ready():
                stdout += channel.recv(buff_size)
                r = stdout.split(b'\n')
                if r and r[-1].find(b"--More--")!=-1:
                    stdout = b"\n".join(r[:-1])+b"\n"
                    channel.send(" ")
                
            if channel.recv_stderr_ready():
                stderr += channel.recv_stderr(buff_size)
            
        exit_status = channel.recv_exit_status()
        # Need to gobble up any remaining output after program terminates...
        while channel.recv_ready():
            stdout += channel.recv(buff_size)

        while channel.recv_stderr_ready():
            stderr += channel.recv_stderr(buff_size)
            
        channel.close()
        return exit_status, stdout, stderr
        
    def close(self):
        self.ssh.close()
    