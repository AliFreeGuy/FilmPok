
import paramiko
import logging




class ServerMonitoring:
        def __init__(self, hostname, port, username, password, local_zip_path, ip_server, api_url, auth_token , server):
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
            else :
                self.server.is_active = True
                self.server.save()

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
