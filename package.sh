# Install python in CentOS 7
sudo yum install epel-release -y
sudo yum install python3 -y

python3 --version  
sudo yum install python3-pip -y
sudo yum install python3-devel -y
sudo yum groupinstall 'development tools' -y

# Install virtualenv
pip3 install virtualenv -y