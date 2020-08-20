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
* copy the ssh public key 



