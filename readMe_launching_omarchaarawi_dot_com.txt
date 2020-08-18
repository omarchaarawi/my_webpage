Steps for launching webpage

Steps followed from the following guide: https://pythonforundergradengineers.com/flask-app-on-digital-ocean.html#set-up-a-new-digital-ocean-droplet

1: Create a droplet on digitalOcean

Specs:
	Ubuntu 18.04.1 x64
	Size: Memory 1G, SSD 25 GB, Transfer 1 TB, Price $5/mo
	Datacenter Region: San Fransisco 2
	Additional Options: None
	SSH keys: Added all of my saved SSH keys

To generate SSH keys:
	use terminal:
		type: ssh-keygen -t rsa
		create passphrase which will later be used to authenticate connection
		locate the folder containing private and public keys
		for me that was: .ssh in my home directory

		use "pbcopy < ~/.ssh/id_rsa.pub" to copy public key to clipboard

copy ssh public key to droplet		
named the key: website_key

name the server: portfolio-server

2: configure the server
	ssh into the server using: ssh root@IPaddress

	type yes when prompted to connect to unknown host
	enter passphrase created when creating ssh keys in step 1
	if you want to change password type: passwd

	create a non-root user by typing: adduser <user>

	next we must manage the firewall and all that:
		then type: usermod -aG sudo <user>
		then type: ufw allow OpenSSH
		then type: ufw enable
	next copy the ssh keys from root to new user using:
		rsync --archive --chown=<user>:<user> ~/.ssh /home/<user>

	finally exit using "exit" and test connection using: ssh <user>@IP_address

3: purchase a domain name and point domain name server to digital ocean
	get a domain name from google domains (12/year)
	go to digitalOcean
	click "[Create] → [Domains/DNS]"
	type newly purchased domain name in the box and click [add domain]
	Link the new Domain to the Digital Ocean Droplet by typing in the @ symbol in the [HOSTNAME] box and selecting the new Droplet name in the [WILL DIRECT TO] drop down box. Click [Create Record] to link the domain name to the server. 

4: Build the Flask App

	install packages
		log in to the server and type the following:
			$ sudo apt-get update
			$ sudo apt-get upgrade
			$ sudo apt-get install python3-pip
			$ sudo apt-get install python3-dev
			$ sudo apt-get install python3-setuptools
			$ sudo apt-get install python3-venv
			$ sudo apt-get install build-essential libssl-dev libffi-dev 

	create a virtual environment using venv:
		$ git clone <git for my webpage>
		$ python3.6 -m venv my_webpage_env
	activate environment using 
		$ source my_webpage_env/bin/activate

	within the virtual env install necessary packages using:
		(my_web_page)$ pip install wheel
		(my_web_page)$ pip install flask
		(my_web_page)$ pip install uwsgi
		(my_web_page)$ pip install requests
	configure uWSGI
		create a file called wsgi.py and fill with:

			# wsgi.py

			from application import app

			if __name__ == "__main__":
   				 app.run()
	test configuration using:
		uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app

	build .ini file:
		deactivate env and 
		open application.ini

	construct a systemd file so we can run the flask app all the time:
		type: $ sudo nano /etc/systemd/system/application.service

		file should look like:

			[Unit]
			Description=uWSGI instance to serve flaskapp
			After=network.target

			[Service]
			User=omar
			Group=www-data
			WorkingDirectory=/home/omar/flaskapp
			Environment="PATH=/home/omar/flaskapp/flaskappenv/bin"
			ExecStart=/home/omar/flaskapp/flaskappenv/bin/uwsgi --ini flaskapp.ini

			[Install]
			WantedBy=multi-user.target

		now run:
			$ sudo systemctl daemon-reload
			$ sudo systemctl start application
			$ sudo systemctl status application

	install and configure NGINX
		install using: sudo apt-get install nginx

	type: sudo nano /etc/nginx/sites-available/application

	configure file as:
		server {
   			listen 80;
   		 	server_name omarchaarawi wwww.omarchaarawi.com;

   			 location / {
   		     		include uwsgi_params;
    		   		 uwsgi_pass unix:/home/omar/my_webpage/application.sock;
    			}
		}

	link NGINX:
		$ sudo ln -s /etc/nginx/sites-available/application /etc/nginx/sites-enabled
		$ sudo systemctl restart nginx
		$ sudo systemctl status nginx
		
	