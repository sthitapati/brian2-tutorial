# Introduction to Brian2

Brian2 is a simulator for spiking neural networks. It is designed to be easy to learn and use, highly flexible, and easily extensible.

## The Unit System

One of the most defining features of Brian2 is its built-in physical unit system. You don't just work with bare numbers; you work with quantities that have dimensions.

```python
import brian2 as b2

tau = 10 * b2.ms    # Time constant
u = -70 * b2.mV     # Potentials
```

If you try to add incompatible units (e.g., `3 * b2.mV + 5 * b2.s`), Brian2 will raise a `DimensionMismatchError`. This helps prevent many common physical modeling errors.

## Basic Workflow

1.  **Define units and constants**: Set up your physical parameters.
2.  **Define equations**: Write the differential equations as strings.
3.  **Create Groups**: Make `NeuronGroup`, `PoissonGroup`, etc.
4.  **Connect**: Use `Synapses` to connect groups.
5.  **Monitor**: Use `StateMonitor` or `SpikeMonitor` to record data.
6.  **Run**: Execute the simulation for a set duration.
7.  **Plot**: Visualize the results.
