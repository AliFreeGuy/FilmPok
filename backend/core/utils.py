
import paramiko
import logging






class ServerStreamManager:
    def __init__(
                    self
                    , hostname,
                    ssh_port,
                    username,
                    password,
                    local_zip_path,
                    api_id,
                    api_hash,
                    bot_token,
                    multi_tokens,
                    backup_channels, 
                    bin_channel,
                    port,
                    fqdn,
                    has_ssl,
                    server,
                    ):
        
        self.hostname = hostname
        self.ssh_port = ssh_port  # SSH port
        self.username = username
        self.password = password
        self.local_zip_path = local_zip_path
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.multi_tokens = multi_tokens  # List of tokens
        self.backup_channels = backup_channels  # List of backup channels
        self.bin_channel = bin_channel
        self.port = port  # Port for Docker container
        self.fqdn = fqdn
        self.has_ssl = has_ssl
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.setup_logging()
        self.connect()
        self.server = server

    def setup_logging(self):
        self.logger = logging.getLogger('tasks')


    def connect(self):
        self.logger.info("Connecting to server...")
        try:
            self.ssh.connect(self.hostname, self.ssh_port, self.username, self.password)
            self.logger.info("Connected.")
        except Exception as e:
            self.logger.error(f"Failed to connect: {e}")
            raise

    def disconnect(self):
        self.logger.info("Disconnecting...")
        self.ssh.close()
        self.logger.info("Disconnected.")

    def exec_command(self, command):
        self.logger.info(f"Executing: {command}")
        stdin, stdout, stderr = self.ssh.exec_command(command)
        stdout_data = stdout.read().decode()
        stderr_data = stderr.read().decode()
        self.logger.info(stdout_data)
        if stderr_data:
            self.logger.error(stderr_data)
        return stdout_data, stderr_data

    def upload_file(self, local_file_path, remote_file_path):
        self.logger.info(f"Uploading {local_file_path} to {remote_file_path}...")
        sftp = self.ssh.open_sftp()
        try:
            sftp.put(local_file_path, remote_file_path)
        except FileNotFoundError as e:
            self.logger.error(f"File not found: {e}")
            raise
        finally:
            sftp.close()

    def clean_up(self):
        self.logger.info("Stopping and removing existing container (if any)...")
        self.exec_command("docker stop fsb || true")
        self.exec_command("docker rm fsb || true")

        self.logger.info("Removing existing image (if any)...")
        self.exec_command("docker rmi stream-bot || true")

    def print_env_vars(self):
        # Print environment variables to be used in Docker container
        self.logger.info("Environment Variables:")
        self.logger.info(f"API_ID: {self.api_id}")
        self.logger.info(f"API_HASH: {self.api_hash}")
        self.logger.info(f"BOT_TOKEN: {self.bot_token}")
        for i, token in enumerate(self.multi_tokens, 1):
            self.logger.info(f"MULTI_TOKEN{i}: {token}")
        for i, channel in enumerate(self.backup_channels, 1):
            self.logger.info(f"BACKUP_CHANNEL{i}: {channel}")
        self.logger.info(f"BIN_CHANNEL: {self.bin_channel}")
        self.logger.info(f"PORT: {self.port}")
        self.logger.info(f"FQDN: {self.fqdn}")
        self.logger.info(f"HAS_SSL: {self.has_ssl}")

    def build_and_run_docker(self):
        self.logger.info("Building Docker image...")
        build_command = 'cd /root/server_streamer && docker build . -t stream-bot'
        stdout, stderr = self.exec_command(build_command)
        if 'Error' in stderr:
            self.logger.error(f"Build failed: {stderr}")

        # Construct environment variables string dynamically
        env_vars = (
            f'-e API_ID="{self.api_id}" '
            f'-e API_HASH="{self.api_hash}" '
            f'-e BOT_TOKEN="{self.bot_token}" '
            + ' '.join([f'-e MULTI_TOKEN{i+1}="{token}"' for i, token in enumerate(self.multi_tokens)]) + ' '
            + ' '.join([f'-e BACKUP_CHANNEL{i+1}="{channel}"' for i, channel in enumerate(self.backup_channels)]) + ' '
            f'-e BIN_CHANNEL="{self.bin_channel}" '
            f'-e PORT="{self.port}" '
            f'-e FQDN="{self.fqdn}" '
            f'-e HAS_SSL="{self.has_ssl}" '
        )

        self.logger.info("Environment Variables for Docker:")
        self.print_env_vars()

        self.logger.info("Running Docker container...")
        run_command = (
            f'docker run --restart unless-stopped --name fsb -d '
            f'{env_vars} '
            f'-p {self.port}:{self.port} '
            f'stream-bot'
        )
        stdout, stderr = self.exec_command(run_command)
        if 'Error' in stderr:
            self.logger.error(f"Run failed: {stderr}")
        else :
            self.server.is_active = True
            self.server.save()

    def setup(self):
        remote_zip_path = '/root/server_streamer.zip'
        extract_to_path = '/root/server_streamer'

        # Clean up old containers and images
        self.clean_up()

        # Upload and extract files
        self.upload_file(self.local_zip_path, remote_zip_path)
        self.exec_command(f"unzip -o {remote_zip_path} -d {extract_to_path}")

        # Build Docker image and run container
        self.build_and_run_docker()









class ServerMonitoring:
        def __init__(
                        self, 
                        hostname, 
                        port,
                        username,
                        password, 
                        local_zip_path,
                        ip_server,
                        api_url,
                        auth_token ,
                        server
                        ):
            self.hostname = hostname
            self.port = port
            self.username = username
            self.password = password
            self.local_zip_path = local_zip_path
            self.ip_server = ip_server
            self.api_url = api_url
            self.auth_token = auth_token
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.setup_logging()
            self.connect()
            self.server = server

        def setup_logging(self):
            
            self.logger = logging.getLogger('tasks')


        def connect(self):
            self.logger.info("Connecting to server...")
            try:
                self.ssh.connect(self.hostname, self.port, self.username, self.password)
                self.logger.info("Connected.")
            except Exception as e:
                self.logger.error(f"Failed to connect: {e}")
                raise

        def disconnect(self):
            self.logger.info("Disconnecting...")
            self.ssh.close()
            self.logger.info("Disconnected.")

        def exec_command(self, command):
            self.logger.info(f"Executing: {command}")
            stdin, stdout, stderr = self.ssh.exec_command(command)
            stdout_data = stdout.read().decode()
            stderr_data = stderr.read().decode()
            self.logger.info(stdout_data)
            if stderr_data:
                self.logger.error(stderr_data)
            return stdout_data, stderr_data

        def upload_file(self, local_file_path, remote_file_path):
            self.logger.info(f"Uploading {local_file_path} to {remote_file_path}...")
            sftp = self.ssh.open_sftp()
            try:
                sftp.put(local_file_path, remote_file_path)
            except FileNotFoundError as e:
                self.logger.error(f"File not found: {e}")
                raise
            finally:
                sftp.close()

        def extract_zip(self, zip_file_path, extract_to_path):
            self.logger.info(f"Extracting {zip_file_path} to {extract_to_path}...")
            self.exec_command(f"unzip -o {zip_file_path} -d {extract_to_path}")

        def clean_up(self):
            # Stop and remove existing container if it exists
            self.logger.info("Stopping and removing existing container (if any)...")
            self.exec_command("docker stop system-monitor || true")
            self.exec_command("docker rm system-monitor || true")

            # Remove existing image if it exists
            self.logger.info("Removing existing image (if any)...")
            self.exec_command("docker rmi system-monitor-image || true")

        def build_and_run_docker(self):
            self.logger.info("Building Docker image...")
            # Ensure Dockerfile is in the correct path
            build_command = 'cd /root/server_monitor && docker build -t system-monitor-image .'
            stdout, stderr = self.exec_command(build_command)
            if 'Error' in stderr:
                self.logger.error(f"Build failed: {stderr}")

            self.logger.info("Running Docker container...")
            run_command = (
                f'docker run -d --network host  '
                f'-e IP_SERVER="{self.ip_server}" '
                f'-e API_URL="{self.api_url}" '
                f'-e AUTH_TOKEN="{self.auth_token}" '
                f'--name system-monitor '
                f'system-monitor-image'
            )
            stdout, stderr = self.exec_command(run_command)
            if 'Error' in stderr:
                self.logger.error(f"Run failed: {stderr}")
            # else :
            #     self.server.is_active = True
            #     self.server.save()

        def setup(self):
            remote_zip_path = '/root/server_monitor.zip'
            extract_to_path = '/root/server_monitor'  # Path for extraction
            
            # Clean up old containers and images
            self.clean_up()

            # Upload and extract files
            self.upload_file(self.local_zip_path, remote_zip_path)
            self.extract_zip(remote_zip_path, extract_to_path)

            # Build Docker image and run container
            self.build_and_run_docker()
