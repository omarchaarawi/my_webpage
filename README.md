# my_webpage

## Intro
This is my personal webpage where I host some of my projects. It is built using a Flask framework. I built the site myself from scratch and host it from my own personal virtual server which I rent from DigitalOcean. I'll include a *Walkthrough* on how I got the site up and running. 

## Launching omarchaarawi.com
I primarily used two sources for this which proved to be super helpful. Thank you [Corey Schafer](https://www.youtube.com/watch?v=goToXTC96Co) and [Peter Kazarinoff](https://pythonforundergradengineers.com/flask-app-on-digital-ocean.html#set-up-a-new-digital-ocean-droplet) for making such great tutorials on launching a website in a really safe secure way.
### Here are the steps I took:
#### 1. Register an account with Digital Ocean and create a droplet (virtual server)
I went with the following specs:
* Ubuntu 18.04.1 x64
* Size: Memory 1G, SSD 25 GB, Transfer 1 TB, Price $5/mo
* Datacenter Region: San Fransisco 2
* Additional Options: None
* SSH keys: Added all of my saved SSH keys 

**To Generate SSH Keys:**
* Open the terminal and type: ssh-keygen -t rsa
* create a passphrase which will later be used to authenticate connection (optional)
* locate the folder containing the private and public keys (for me that was .ssh in my home directory)
* use: "pbcopy < ~/.ssh/id_rsa.pub" to copy the public key to clipboard
* copy the ssh public key to droplet
* give the server a name (portfolio server)

#### 2. Configure the server
Just a couple housekeeping things to get pakages up to date and get things rolling
* ssh into the server using root@IP_Address, type y when promted to connect to unknown host
* enter passphrase created when creating ssh keys in step 1 (type: "passwd" to change the password if you want)
* create a non-root user by typing: "adduser <user>"
* next we must manage the firewall and all that:
  * type: "usermod -a -G sudo <user>" to grant the newly crated non-root user sudo privileges
  * on uncomplicated firewall allow ssh by typing: "ufw allow OpenSSH" **This is important**
  * accept the changes by typing: "ufw enable"
  * copy the ssh keys from root to new user using: "rsync --archive --chown=<user>:<user> ~/.ssh /home/<user>"
  * exit the server and test by reconnecting using SSH

#### 3. Purchase a domain name and point domain name server to digital ocean (optional)
This step is optional. You always just use the IP address of your server, but having a doman name is nice and allows for https.
* i purchased [omarchaarawi.com](https://omarchaarawi.com/) from google domains for $12/year
* in the settings select "use custom name servers"
![google DNS settings](/images/google_DNS_settings.png)
* got to digital ocean and click "[create]->[Domain/DNS]"
* type newly purchased domain name in the box and click "[add domain]"
* Link the new Domain to the DigitalOcean droplet by typing in the @ symbol in the "[hostname]" box and selecting
the new droplet name in the "[will direct to]" drop down box
* click "[create record]" to link the domain name to the server
  This is what my settings looked like:
  ![digitalOcean DNS settings](/images/digitalOcean_DNS_settings.png)
  
#### 4. Build the Flask APP in a virtual environment
I already had the app all built on my personal machine so I pushed that to my repository and then cloned the
repository on my virtual machine.
* I first 

  



