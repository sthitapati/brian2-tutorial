# Brian2 Tutorials

This tutorial is generated using gemini-agent for my personal learning.

A comprehensive set of tutorials for the [Brian2](https://briansimulator.org/) spiking neural network simulator.

## Getting Started

### Prerequisites
- Python 3.x
- Brian2
- Matplotlib

```bash
pip install brian2 matplotlib
```

### Running Simulations
The simulation scripts are located in the `scripts/` directory.

```bash
python scripts/02_single_neuron.py
```

## Tutorials

### Basics
1.  **[Introduction](docs/01_introduction.md)**: Unit system and basics.
2.  **[Single Neuron](docs/02_single_neuron.md)**: Leaky Integrate-and-Fire (LIF) model.
3.  **[Synapses](docs/03_synapses.md)**: Event-driven synaptic transmission.
4.  **[Networks](docs/04_networks.md)**: Populations and sparse connectivity.
5.  **[Plasticity](docs/05_plasticity.md)**: Spike-Timing Dependent Plasticity (STDP).

### Advanced
6.  **[Hodgkin-Huxley](docs/06_hodgkin_huxley.md)**: Biologically realistic ion channels.
7.  **[Multicompartment](docs/07_multicompartment.md)**: Spatial neurons (Soma + Dendrite).
8.  **[Gap Junctions](docs/08_gap_junctions.md)**: Electrical coupling.

## Organization
- `docs/`: Markdown documentation and images.
- `scripts/`: Python simulation scripts.
