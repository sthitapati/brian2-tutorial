import brian2 as b2
import matplotlib.pyplot as plt

def run_simulation():
    b2.start_scope()

    # Parameters
    N = 100 # Number of neurons
    tau = 10 * b2.ms
    u_rest = -70 * b2.mV
    threshold = -55 * b2.mV
    reset = -70 * b2.mV
    
    # 1. Poisson Input Group
    # This group simulates an external population (e.g., retina) firing randomly.
    # '10*b2.Hz' is the average firing rate for each of the 100 neurons.
    P = b2.PoissonGroup(N, rates=10*b2.Hz)

    # 2. Target Population (LIF Neurons)
    eqs = '''
    du/dt = -(u - u_rest) / tau : volt
    '''
    G = b2.NeuronGroup(N, eqs, threshold='u > threshold', reset='u = reset', method='exact')
    G.u = u_rest

    # 3. Connections
    # Connect Poisson inputs to Neurons
    # p=0.1 means each pair has a 10% chance of being connected (Sparse connectivity).
    #
    # When a Poisson neuron fires, it increases the target's voltage by 5 mV.
    S = b2.Synapses(P, G, on_pre='u += 5*mV')
    S.connect(p=0.1)

    # 4. Monitors
    spikes_P = b2.SpikeMonitor(P)
    spikes_G = b2.SpikeMonitor(G)

    # 5. Run
    print("Running Network Simulation...")
    b2.run(500 * b2.ms)
    print("Finished.")

    # 6. Plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Poisson Input Raster
    axs[0].plot(spikes_P.t/b2.ms, spikes_P.i, '.k', ms=3)
    axs[0].set_ylabel('Neuron Index')
    axs[0].set_title('Poisson Input Spikes')
    axs[0].grid(True, alpha=0.3)

    # Population Response Raster
    axs[1].plot(spikes_G.t/b2.ms, spikes_G.i, '.b', ms=3)
    axs[1].set_ylabel('Neuron Index')
    axs[1].set_xlabel('Time (ms)')
    axs[1].set_title('Target Population Response')
    axs[1].grid(True, alpha=0.3)
    
    output_file = 'network_raster.png'
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

if __name__ == "__main__":
    run_simulation()
