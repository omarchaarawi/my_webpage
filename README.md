# my_webpage

## Intro
This is my personal webpage where I host some of my projects. It is built using a Flask framework. I built the site myself from scratch and host it from my own personal virtual server which I rent from DigitalOcean. I'll include a *Walkthrough* on how I got the site up and running. 

# Launching omarchaarawi.com
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
* install the necessary packages
  * sudo apt-get update
  * sudo apt-get upgrade
  * sudo apt-get install python3-pip
  * sudo apt-get install python3-dev
  * sudo apt-get install python3-setuptools
  * sudo apt-get install python3-venv
  * sudo apt-get install build-essential libssl-dev libffi-dev
* Create a virtual environment using venv:
  * python3.6 -m venv <name_of_env> (my_webpage_env)
  * activate the environment using: "source <name_of_env/bin/activate"
  * within the virtual env install necessary packages using the requirements folder:
    * type: pip install -r <requirements.txt> 
* After creating the virtual env test the application
  * export the project using: export FLASK_APP=applicaiton.py
  * then type: flask run --host=0.0.0.0
  * now when you open the browser and go to myIPADDRESS:5000 you should see the page
* Now that things are running fine in the development server let's take er live using NGINX and Gunicorn
* install NGINX
  * sudo apt install nginx
  * pip install gunicorn  (make sure you're in your virtual env)
* update the config file for nginx
  * remove the default NGINX config file using: sudo rm /etc/nginx/sites-enabled/default
  * create new config file using: sudo nano /etc/nginx/sites-enabled/<file_name>
  * this is how i configured my file:
  
  server {
        server_name omarchaarawi.com www.omarchaarawi.com;

        location /static {
                alias /home/omar/my_webpage/static;
        }
        location / {
                proxy_pass http://localhost:8000;
                include /etc/nginx/proxy_params;
                proxy_redirect off;
        }

* next open up port 80 and close 5000
  * sudo ufw allow http/tcp
  * sudo ufw delete allow 5000
  * sudp ufw enable
* restart the nginx server
  * sudo systemctl restart nginx
Now NGINX is running but guincorn is not so NGINX doesn't know what to do with the python application
* run gunicorn
  * gunicorn -w 3 <file_that_has_application>
  
  When determing how many workers to run we use the following formula from the gunicorn documentation: (2 x num_of_cores) + 1. I am running
  this on a machine with 1 core so i used 3 workers.
  
  * run gunicorn using: gunicorn -w 3 run:app
* now gunicorn is running, but not in the background
* using Supervisor we can configure this to run in the background
  * install supervisor using: sudo apt install supervisor
  * setup config file for supervisor
    * sudo nano /etc/supervisor/conf.d/<name_of_file>
    * this is how i configured my file:
    
      [program:application]
      
      directory=/home/omar/my_webpage
      
      command=/home/omar/my_webpage/my_webpage_env/bin/gunicorn -w 3 application:app
      
      user=omar
      
      autostart=true
      
      autorestart=true
      
      stopasgroup=true
      
      killasgroup=true
      
      stderr_logfile=/var/log/my_webpage/my_webpage.err.log
      
      stdout_logfile=/var/log/my_webpage/my_webpage.out.log

  * create a directory to save stderr file and stdout file using run: sudo mkdir -p /var/log/<name_of_file_containing_app>
  * then run: sudo touch /var/log/<name_of_file_containing_app>/<name_of_stderr_file.err.log>
  * then run: sudo touch /var/log/<name_of_file_containing_app>/<name_of_stderr_file.out.log>
* restart supervisor using: sudo supervisorctl reload 

Now that guicorn is running in the background all should be running fine. To add SSL security follow the following steps.

#### 5. Adding SSL security so site can be run https

We can use certbot to generate SSL certificates

* sudo add-apt-repository ppa:certbot/certbot
* sudo apt install python-certbot-nginx
* sudo certbot --nginx -d mydomain.com -d www.mydomain.com

I selected option 2 to redirect

If this step is done correctly a little message will pop up letting you know. 

run: sudo ufw delete allow 'Nginx Full'
run: sudo ufw allow Nginx HTTPS'

Finally restart nginx and supervisor for all changes to take place.


  
    

 

 
 

  



