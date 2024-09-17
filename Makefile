# bot name in telegram @info_about_books_bot
start_server:
	poetry run python aiogram_run.py &

start_pc:
	python aiogram_run.py

stop:
	pkill -9 -f aiogram_run.py


test:
	python -m unittest tests.download_from_fantlab


push:
	scp -r -P 10090 bibliosites db handlers keyboards lexicon .env aiogram_run.py create_bot.py config_reader.py \
		README.md Makefile pyproject.toml olebedev@192.168.99.99:/mnt/disk/hope/code/infobooks-bot

go_to_server:
	ssh -p 10090 olebedev@192.168.99.99
	cd /mnt/disk/hope/code/infobooks-bot

#start_bot_on_server:
#	ssh -p 10090 olebedev@192.168.99.99
#	cd /mnt/disk/hope/code/infobooks-bot

#try_bot:
#	python infobooks_bot/bot.py

#database:
#	python infobooks_bot/database.py

#fantlab:
#	python infobooks_bot/fantlab.py