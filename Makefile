runserver:
	poetry run python event_loop/server.py

ping:
	poetry run python event_loop/client.py
