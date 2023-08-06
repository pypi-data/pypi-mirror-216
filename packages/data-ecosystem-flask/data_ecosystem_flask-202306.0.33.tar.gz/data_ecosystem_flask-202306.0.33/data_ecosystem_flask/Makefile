azd-install:
	cd ~ && \
	wget https://github.com/Azure/azure-dev/releases/download/azure-dev-cli_1.0.2/azd-linux-amd64.tar.gz   && \
	tar -xvf azd-linux-amd64.tar.gz  && \
	chmod +x azd-linux-amd64  && \
	cp -r ~/azd-linux-amd64  ~/.local/bin  &&  \
	ln -s ~/azd-linux-amd64 ~/.local/bin/azd   &&  \
	azd 

cert:
	cd ~/data-ecosystem-services/pade-flask/data_ecosystem_flask && \
	openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 && \
	cp cert.pem ~/.ssl/certs/ && \
	cp key.pem ~/.ssl/private/

flask-create-OCIO-PADE-DEV:
	source ~/.local/bin/virtualenvwrapper.sh && \
	workon OCIO_PADE_DEV  && \
	curl -sSL https://install.python-poetry.org | python3 - &&  \
	cp -r ~/.local/bin $$VIRTUAL_ENV/bin/poetry  &&  \
	poetry update \
	poetry install

flask-get-external-ip:
	ip addr show eth0 | grep inet | awk '{ print $2; }' | sed 's/\/.*$//'
	# from powershell admin run 
	# netsh advfirewall firewall add rule name="WSL" dir=in action=allow protocol=TCP localport=5000
	# test on local	
	# http://<WSL_IP_ADDRESS>:5000
	# EXAMPLE: http://172.18.98.159:5000

flask-kill:
	kill $(lsof -t -i:443)

flask-run-wsl-dev:
	cd ~/.virtualenvs/OCIO_PADE_DEV/bin && \
	. activate && \
	.  ~/.bashrc && \
	cd ~/data-ecosystem-services/pade-flask/data_ecosystem_flask && \
	openssl s_client -connect www.google.com:443 -showcerts </dev/null | awk '/BEGIN/,/END/{print}' | openssl x509 -outform PEM > www-google-com-fullchain.pem && \
	openssl s_client -connect accounts.google.com:443 -showcerts </dev/null | awk '/BEGIN/,/END/{print}' | openssl x509 -outform PEM > accounts-google-com-fullchain.pem   && \
	openssl s_client -connect dev.alation.edav.cdc.gov:443 -showcerts </dev/null | awk '/BEGIN/,/END/{print}'  > dev-alation-edav-cdc-gov-fullchain.pem    && \
	poetry update && \
	poetry install	 && \
	export FLASK_APP=app.py && \
	export FLASK_ENV=development && \
	export FLASK_DEBUG=1 && \
	export FLASK_PORT=5000 && \
	flask run --host=0.0.0.0

 
flask-run-posit-dev:
	poetry update && \
	poetry install	 && \
	export FLASK_APP=app.py  && \
	export FLASK_ENV=development && \
	export FLASK_DEBUG=1 && \
	flask run  --debug   

flask-run-posit-prod:
	poetry update && \
	poetry install	 && \
	export FLASK_APP=app.py  && \
	export FLASK_DEBUG=1 && \
	flask run --debug  

chrome-libva-install:
	# Logout of ZScaler first
	cd ~   && \
	sudo apt update  && \
	sudo apt upgrade  && \
	sudo apt install i965-va-driver libva-drm2 libva-x11-2 vainfo && \
	sudo apt-get update && \
	sudo apt-get install intel-media-va-driver:amd64 && \
	sudo apt-get update

chrome-libva-reboot:
	sudo reboot 

chrome-libva-test:
	vainfo

github-setup-secrets:
	npm install -g gh
	
github-config:
	git config --global user.name "John Bowyer"
	git config --global user.email "jcbowyer@hotmail.com"

node-create:
	pip3 uninstall nodeenv
	pip3 install --user nodeenv

pip-check:
	pip --version

pip-create-wsl:
	sudo apt update
	sudo apt-get install python3-pip

posit-config-prod:
	rsconnect add --api-key $$OCIO_PADE_PROD_POSIT_SECRET --server https://rconnect.edav.cdc.gov --name data_ecosystem_flask

posit-config-dev:
	rsconnect add --api-key $$OCIO_PADE_DEV_POSIT_SECRET --server https://dev.rconnect.edav.cdc.gov:8080 --name data_ecosystem_flask_named_config

posit-test-secret-dev:
	rsconnect test-secret <test_secret> $$OCIO_PADE_DEV_POSIT_SECRET 

posit-write-manifest:
	cd ~/data-ecosystem-services/pade-flask/data_ecosystem_flask && \
	rsconnect write-manifest api  --overwrite    --verbose .

posit-deploy-manifest:
	cd ~/data-ecosystem-services/pade-flask/data_ecosystem_flask && \
	rsconnect deploy manifest  manifest.json  --server  https://dev.rconnect.edav.cdc.gov:8080 --api-key $$OCIO_PADE_DEV_POSIT_SECRET --new --title "data_ecosystem_flask_manifest"  --verbose    
 
posit-deploy-wsl:
	cd ~/data-ecosystem-services/pade-flask/ && \
	openssl s_client -connect dev.alation.edav.cdc.gov:8080 -showcerts </dev/null | awk '/BEGIN/,/END/{print}'  > dev-alation-edav-cdc-gov-fullchain.pem    && \



# rsconnect deploy api --server  https://dev.rconnect.edav.cdc.gov:8080  --api-key $OCIO_PADE_DEV_POSIT_CONNECT_SECRET   --verbose  --entrypoint data_ecosystem_flask.app:app ./data_ecosystem_flask

posit-deploy-named-config-dev:
	cd ~/data-ecosystem-services/pade-flask/data_ecosystem_flask  && \
	rsconnect deploy api --name data_ecosystem_flask_named_config  --force-generate --verbose --new  --title data_ecosystem_flask_named_config  .


posit-deploy-config-dev:
	cd ~/data-ecosystem-services/pade-flask  && \
	poetry export -f requirements.txt --output requirements.txt --without-hashes  && \
	mv  requirements.txt data_ecosystem_flask/ && \
	cd ~/data-ecosystem-services/pade-flask/data_ecosystem_flask  && \
	rsconnect deploy api   --name data_ecosystem_flask3    --verbose . 

posit-deploy-dev:
	cd ~/data-ecosystem-services/pade-flask  && \
	poetry export -f requirements.txt --output requirements.txt --without-hashes   && \
	mv  requirements.txt data_ecosystem_flask/ && \
	cd ~/data-ecosystem-services/pade-flask/data_ecosystem_flask  && \
	rsconnect deploy api --title data_ecosystem_flask_2 --force-generate --new --server   https://dev.rconnect.edav.cdc.gov:8080 --api-key $$OCIO_PADE_DEV_POSIT_CONNECT_SECRET  --verbose --entrypoint app:app .

posit-update-requirements:
	cd ~/data-ecosystem-services/pade-flask  && \
	poetry export -f requirements.txt --output requirements.txt --without-hashes   && \
	mv  requirements.txt data_ecosystem_flask/

posit-deploy-prod:
	cd ~/data-ecosystem-services/pade-flask  && \
	poetry export -f requirements.txt  && \rsconnect deploy api  --force-generate   --server  https://rconnect.edav.cdc.gov --api-key $$OCIO_PADE_DEV_POSIT_CONNECT_SECRET    --verbose --entrypoint app:app .
	


# PREREQUISITE: workon OCIO_PADE_DEV
# pip freeze > requirements.txt
# poetry export -f requirements.txt  
posit-deploy-old:
	rm -f requirements.txt \
	rm -f manifest.json \
	pip install data_ecosystem_services
	pip freeze > requirements.txt
	args="" &&  \
	new_args="" &&  \
	while IFS= read -r line; do \
		var=`echo "$$line" | cut -d '=' -f 1`; \
		val=`echo "$$line" | cut -d '=' -f 2`; \
		echo "var: $$var, val: $$val"; \
		args="$$args$$var=$$val,"; \
		echo "$$args"; \
	done < .env; \
	new_args=`echo $$args | sed 's/,$$//'`; \
	echo "$$new_args";  \
	rsconnect deploy api --name data-ecosystem-flask --title "Data Ecosystem Flask" --new  --force-generate  --verbose  --environment $$new_args .

python-create-posit:
	cd ~  && \
	INSTALL_DIR="$$HOME/.local"  && \
	wget https://www.sqlite.org/2023/sqlite-autoconf-3420000.tar.gz && \
	tar -xf sqlite-autoconf-3420000.tar.gz && \
	cd sqlite-autoconf-3420000 && \
	gcc  -c -fPIC sqlite3.c -o sqlite3.o  && \
	ar rcs libsqlite3.a sqlite3.o && \
	gcc -shared -o libsqlite3.so sqlite3.o && \
	mkdir -p $$HOME/.local/bin/sqlite-autoconf-3420000 && \
	mv ~/sqlite-autoconf-3420000/libsqlite3.so $$HOME/.local/bin/sqlite-autoconf-3420000/libsqlite3.so && \
	mv ~/sqlite-autoconf-3420000/sqlite3.o $$HOME/.local/bin/sqlite-autoconf-3420000/sqlite3.o && \
	export LD_LIBRARY_PATH=$$HOME/.local/bin/sqlite-autoconf-3420000:$$LD_LIBRARY_PATH   && \
	wget https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tar.xz  && \
	tar -xvf Python-3.9.9.tar.xz  && \
	cd Python-3.9.9 && \
	./configure --prefix=$$INSTALL_DIR && \
	make  && \
	make altinstall  && \
	echo "export PATH=\"$$INSTALL_DIR/bin:\$$PATH\"" >> ~/.bashrc  && \
	source ~/.bashrc  && \
	python3.9 --version

python-create-wsl:
	sudo apt update
	sudo apt install python3.9
	echo PATH=/usr/bin/python3.9:$$PATH | sudo tee -a ~/.bashrc
	source ~/.bashrc

python-check:
	python3 --version

rmbashrc:
	rm ~/.bashrc

venv-check:
	which virtualenv

venv-create-wsl:
	sudo apt install python3.9-venv

venv-create-root:
	mkdir ~/.virtualenvs
	pip3 install --upgrade pip
	pip3 --version
	pip3 install --user virtualenv
	pip3 install --user virtualenvwrapper
	echo 'export PATH=~/.local/bin:$$PATH' |  tee -a ~/.bashrc
	echo 'export PATH=/usr/bin:$$PATH' |  tee -a ~/.bashrc
	echo 'export WORKON_HOME=~/.virtualenvs' |  tee -a ~/.bashrc
	echo 'export VIRTUALENVWRAPPER_VIRTUALENV=~/.local/bin/virtualenv' | tee -a ~/.bashrc
	echo 'export VIRTUALENVWRAPPER_SCRIPT=~/.local/bin/virtualenvwrapper.sh' | tee -a ~/.bashrc
	echo 'export VIRTUALENVWRAPPER_PYTHON=~/.local/bin/python3' |  tee -a ~/.bashrc
	echo 'source ~/.local/bin/virtualenvwrapper.sh' | tee -a ~/.bashrc
	source ~/.bashrc

venv-create-OCIO-PADE-PROD:
	source ~/.local/bin/virtualenvwrapper.sh && \
	mkvirtualenv OCIO_PADE_PROD && \
	workon OCIO_PADE_PROD  && \
	cd $$VIRTUAL_ENV  && \
	wget https://nodejs.org/dist/v18.12.1/node-v18.12.1-linux-x64.tar.xz  && \
	tar -xf node-v18.12.1-linux-x64.tar.xz  && \
	mv node-v18.12.1-linux-x64/bin/* ./bin/  && \
	mv node-v18.12.1-linux-x64/lib/node_modules/ ./lib/node_modules/

venv-create-OCIO-PADE-DEV:
	source ~/.local/bin/virtualenvwrapper.sh && \
	mkvirtualenv OCIO_PADE_DEV && \
	workon OCIO_PADE_DEV  && \
	cd $$VIRTUAL_ENV  && \
	wget https://nodejs.org/dist/v18.12.1/node-v18.12.1-linux-x64.tar.xz  && \
	tar -xf node-v18.12.1-linux-x64.tar.xz  && \
	mv node-v18.12.1-linux-x64/bin/* ./bin/  && \
	mv node-v18.12.1-linux-x64/lib/node_modules/ ./lib/node_modules/

venv-remove-wsl-OCIO-PADE-DEV:
	# NOTE: LOGOUT OF ZSCALER FIRST
	deactivate
	cd $HOME
	# cleanup any existing node
	sudo rm -rf node-v18.12.1-linux-x64.tar.xz
	# sudo rm -rf /usr/local/bin/npm /usr/local/share/man/man1/node* ~/.npm
	# sudo rm -rf /usr/local/lib/node*
	# sudo rm -rf /usr/local/bin/node*
	# sudo rm -rf /usr/local/include/node*
	sudo apt-get purge nodejs npm
	sudo apt autoremove
	sudo pip uninstall nodeenv
	# EXAMPLE:
	workon OCIO_PADE_DEV
	cd $VIRTUAL_ENV
	# install node
	wget https://nodejs.org/dist/v18.12.1/node-v18.12.1-linux-x64.tar.xz
	tar -xf node-v18.12.1-linux-x64.tar.xz
	sudo mv node-v18.12.1-linux-x64/bin/* ./bin/
	sudo mv node-v18.12.1-linux-x64/lib/node_modules/ ./lib/node_modules/
	# Verify installation using
	node -v
	npm -v
	npm install npm@9.1.1
	pip install --upgrade pip
	pip install nodeenv
	cd $VIRTUAL_ENV/lib/node_modules/npm
	nodeenv -p
	cd $VIRTUAL_ENV/lib
	npm install  @mermaid-js/mermaid-cli --registry=https://registry.npmjs.org
	cdvirtualenv bin
	echo "export PATH='$PATH:$VIRTUAL_ENV/lib/node_modules/.bin'" | sudo tee -a activate
	source activate
	# Test client
	mmdc -h
