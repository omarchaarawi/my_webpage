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

	create a non-root user my typing: adduser <user>

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
		$ cd ~
		$ mkdir flaskapp
		$ cd flaskapp
		$ python3.6 -m venv flaskappenv
		$ source flaskappenv/bin/activate

	within the virtual env install necessary packages using:
		(flaskappenv)$ pip install wheel
		(flaskappenv)$ pip install flask
		(flaskappenv)$ pip install uwsgi
		(flaskappenv)$ pip install requests
	configure uWSGI
		create a file called wsgi.py and fill with:

			# wsgi.py

			from flaskapp import app

			if __name__ == "__main__":
   				 app.run()
	test configuration using:
		uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
	