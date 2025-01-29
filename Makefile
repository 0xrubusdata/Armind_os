# Define the default target
all: start

# Target to start both client and server
start:
	@echo "Starting client and server..."
	@cd client && sudo docker compose up -d
	@cd server && sudo docker compose up -d
	@sleep 90
	@sudo ip route show | awk '/default dev veth/ {print $3}' | xargs -I {} sudo ip route del default dev {}
	@echo "Both client and server are running."

# Target to stop both client and server
stop:
	@echo "Stopping client and server..."
	@cd client && sudo docker compose down
	@cd server && sudo docker compose down
	@echo "Both client and server have been stopped."

# Target to restart both client and server
restart: stop start

# Target to view logs for both client and server
logs:
	@echo "Showing logs for client and server..."
	@cd client && sudo docker compose logs -f
	@cd server && sudo docker compose logs -f

# Target to clean up (remove containers, networks, and volumes)
clean:
	@echo "Cleaning up client and server..."
	@cd client && sudo docker compose down -v
	@cd server && sudo docker compose down -v
	@echo "Cleanup complete."

# Target to rebuild and restart both client and server
rebuild:
	@echo "Rebuilding and restarting client and server..."
	@cd client && sudo docker compose up -d --build
	@cd server && sudo docker compose up -d --build
	@echo "Rebuild and restart complete."

.PHONY: all start stop restart logs clean rebuild