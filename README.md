# In Memory Storage

## Instalation
```
ln -s /home/petr/Workspace/in-memory-storage/in-memory-storage-daemon /home/petr/bin/
```

## Usage
```
# Unknown key returns [err]
echo "test" > /tmp/in-memory-storage && cat /tmp/in-memory-storage
[err]

# Put returns [ok]
echo "test=abc" > /tmp/in-memory-storage && cat /tmp/in-memory-storage
[ok]

# Get returns value
echo "test" > /tmp/in-memory-storage && cat /tmp/in-memory-storage
abc

# [all] returns all memory
echo "[all]" > /tmp/in-memory-storage && cat /tmp/in-memory-storage
{"test": "abc"}
```
