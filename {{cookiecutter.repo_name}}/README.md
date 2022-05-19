# We use dot env file + pydantic settings class as project settings
# Loguru usage example
```python
from loguru import logger
logger.info("Hello {}", "World")
```
# Make develop env
```shell
make env
```
# Also, you can develop with docker
```shell
make docker
```
# Make migration
```shell
make migration
```
# Make migrate
```shell
make migrate
```
# Make testing
```shell
tox
```
# If build orjson, ujson failed
```shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup default nightly
```
# If build Pillow failed, pls install zlib, libjpeg first
