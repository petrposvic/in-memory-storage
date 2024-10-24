# In Memory Storage

## Instalation
```
# mkdir -p ~/.config/systemd/user
cp in-memory-storage.service ~/.config/systemd/user/
# sudo apt install python3-dbus # For server
# sudo apt install python3-click # For client
# systemctl --user status in-memory-storage.service
# systemctl --user start in-memory-storage.service
# systemctl --user enable in-memory-storage.service
# journalctl --user -u in-memory-storage.service -f
```

## Usage
```
# Unknown key returns [err]
./client.py test
[err]

# Put returns [ok]
./client.py test=abc
[ok]

# Get returns value
./client.py test
abc

# [all] returns all memory
./client.py [all]
{"test": "abc"}
```
