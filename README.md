# Beholder 👁️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)

Live plotting for multiprocessing data streams.

Beholder is a small Python toolkit for sending numeric values through a shared queue and visualizing them in real time with PyQtGraph. It is useful for quick experiments, debugging, simulations, and any workflow where you want to watch values change while another process keeps running.

## Installation

This project requires Python 3.12 or newer.

```bash
# Using uv (recommended)
uv sync

# Using pip
pip install git+https://github.com/mateusglucas/beholder.git
```

## Quick Start

Start the server:

```bash
uv run python examples/server.py -a 127.0.0.1 -p 5555 -k 123
```

Then, in another terminal, start a client that sends values to the plot:

```bash
uv run python examples/client.py -a 127.0.0.1 -p 5555 -k 123
```

The server opens a plotting window and updates it as values arrive.

## How it works

Beholder has two main pieces:

- `QueueManager`: exposes a shared queue via `multiprocessing.managers` that clients can connect to over TCP.
- `Beholder`: consumes `(key, value)` pairs from the queue in a separate process and plots each key as a separate curve using PyQtGraph.

Example payload:

```python
QueueManager.get_global_queue().put(("temperature", 23.5))
```

Each unique key automatically becomes its own plotted series with a distinct color.

## Examples

See the [`examples/`](examples/) directory for a complete client/server setup:

| File | Description |
|------|-------------|
| [`examples/server.py`](examples/server.py) | Starts the queue manager and launches Beholder in a separate process to plot incoming data |
| [`examples/client.py`](examples/client.py) | Connects to the server and sends random values every 100ms |

## License

[MIT](LICENSE)
