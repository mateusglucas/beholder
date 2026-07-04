# Beholder

Live plotting for multiprocessing data streams.

Beholder is a small Python toolkit for sending numeric values through a shared queue and visualizing them in real time with PyQtGraph. It is useful for quick experiments, debugging, simulations, and any workflow where you want to watch values change while another process keeps running.

## Installation

This project requires Python 3.12 or newer.

```bash
uv sync
```

## Usage

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

- `QueueManager`: exposes a shared queue that clients can connect to.
- `Beholder`: consumes `(key, value)` pairs from the queue and plots each key as a separate curve.

Example payload:

```python
QueueManager.get_global_queue().put(("temperature", 23.5))
```

Each unique key becomes its own plotted series.

## Examples

The `examples/` directory contains a minimal client/server setup:

- `examples/server.py`: starts the queue manager and plotting window.
- `examples/client.py`: connects to the queue manager and sends random values.

## License

No license has been specified yet.
