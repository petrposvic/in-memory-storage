# In Memory Storage

## Instalation
```
cp in-memory-storage.service ~/.config/systemd/user/
# systemctl --user status in-memory-storage.service
# systemctl --user start in-memory-storage.service
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
