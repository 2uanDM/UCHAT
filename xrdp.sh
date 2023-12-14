# This script is for creating 3 user accounts for VNC remote access

# Create users (echo with colors)
echo -e "\e[1;32mCreating users 1...\e[0m"
sudo useradd kaxim_topic1
ehoc -e "\e[1;32mCreating users 2...\e[0m"
sudo useradd kaxim_topic2
echo -e "\e[1;32mCreating users 3...\e[0m"
sudo useradd kaxim_topic3

# Change password for users
echo -e "\e[1;32mChanging password for users 1...\e[0m"
sudo passwd kaxim_topic1

echo -e "\e[1;32mChanging password for users 2...\e[0m"
sudo passwd kaxim_topic2

echo -e "\e[1;32mChanging password for users 3...\e[0m"
sudo passwd kaxim_topic3

# Check visudo wheel group is uncommented
echo -e "\e[1;32mChecking visudo wheel group is uncommented...\e[0m"
sudo visudo

## Allows people in group wheel to run all commands

# %wheel        ALL=(ALL)       ALL

# Add users to wheel group
echo -e "\e[1;32mAdding users to wheel group...\e[0m"
sudo usermod -aG wheel kaxim_topic1
sudo usermod -aG wheel kaxim_topic2
sudo usermod -aG wheel kaxim_topic3

# Repel repository 
echo -e "\e[1;32mInstalling repel repository...\e[0m"
sudo yum install -y epel-release

# Install xrdp and tigervnc-server
sudo yum -y install xrdp tigervnc-server

systemctl start xrdp.service
systemctl status xrdp.service
systemctl enable xrdp.service

sudo firewall-cmd --permanent --add-port=3389/tcp 
sudo firewall-cmd --reload

# 


