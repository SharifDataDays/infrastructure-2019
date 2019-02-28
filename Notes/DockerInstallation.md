# Docker Installation Guid

## Resources
The Following is from here:
1. [Digital Ocean's Tutorials](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04)


# Ubuntu Bash
0. (*optional*) using the GPG key of the official Docker Repository it's possible to validate the downloads:
  1. Add *GPG key* to the system:
  ```bash
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  ```

  2. Add the Docker repository to *APT* sources: 
  ```bash
  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"  
  ```
    
  3. Update the package database with the Docker packages from the newly added repo:
  ```bash
  sudo apt-get update
  ```

  4. Validate you're installing the Docker repo instead of the default Ubuntu 16.04 repo:
  ```bash
  apt-cache policy docker-ce
  ```

1. Install Docker and check if the deamon service is Correctly and the process is enabled to start on boot:
  1. Install Docker:
  ```bash
  sudo apt-get install -y docker-ce
  ```

  2. Check the daemon service status:
  ```bash
  sudo systemctl status docker
  ```
