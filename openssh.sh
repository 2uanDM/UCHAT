#Install OpenSSH Server and Client
sudo yum install openssh-server openssh-clients -y

# Then start the OpenSSH service
echo -e "\033[32mStarting OpenSSH...\033[0m"
sudo systemctl start sshd

# Change the default SSH port from 22 to 20231
echo -e "\033[32mChanging the default SSH port...\033[0m"
sudo sed -i 's/#Port 22/Port 20231/g' /etc/ssh/sshd_config

# Allow root login
echo -e "\033[32mAllowing root login...\033[0m"
sudo sed -i 's/PermitRootLogin no/PermitRootLogin yes/g' /etc/ssh/sshd_config

# Tell SELinux that we want to use a non-standard port
echo -e "\033[32mTelling SELinux that we want to use a non-standard port...\033[0m"
sudo semanage port -a -t ssh_port_t -p tcp 20231

# Add firewall rules to allow SSH
echo -e "\033[32mAdding firewall rules to allow SSH...\033[0m"
sudo firewall-cmd --permanent --add-port=20231/tcp

# Reload firewall rules
echo -e "\033[32mReloading firewall rules...\033[0m"
sudo firewall-cmd --reload

# Enable the OpenSSH service to start automatically on boot
echo -e "\033[32mEnabling OpenSSH...\033[0m"
sudo systemctl enable sshd

# Restart the OpenSSH service
echo -e "\033[32mRestarting OpenSSH...\033[0m"
sudo systemctl restart sshd
