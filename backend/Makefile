.PHONY: lock lock-linux lock-macos lock-windows

# Default target
all: lock

# Lock dependencies for all platforms
lock:
	uv pip compile -o requirements.txt pyproject.toml

# Clean generated requirements files
clean:
	rm -f requirements.linux.txt requirements.macos.txt requirements.windows.txt *.db
