import brian2 as b2
import matplotlib.pyplot as plt

def run_simulation():
    # 1. Cloud-based configuration (preferences) can be set here if needed
    b2.start_scope()

    # 2. Define physical constants and parameters
    tau = 10 * b2.ms
    u_rest = -70 * b2.mV
    u_reset = -65 * b2.mV
    threshold = -50 * b2.mV
    
    # Input current (step current) to make it fire
    # We'll add a term 'I' to the equation later, for now let's just observe decay 
    # or simple drift if we set initial value high.
    # Let's add a constant current I so we can see charging up.
    R = 10 * b2.Mohm
    I_ext = 2.5 * b2.nA # Sufficient to cross threshold if we had spikes
    
    # 3. Define Differential Equations
    # The Leaky Integrate-and-Fire Mechanism
    # du/dt : Change in voltage over time
    # -(u - u_rest) : Decay term (pulls u back to u_rest)
    # R * I_ext : Input drive (pushes u up)
    # Divided by tau : Controls the speed of dynamics
    eqs = '''
    du/dt = (-(u - u_rest) + R * I_ext) / tau : volt
    '''

    # 4. Create Neuron Group
    # Added threshold and reset for spiking behavior
    G = b2.NeuronGroup(1, eqs, threshold='u > threshold', reset='u = u_reset', method='exact')

    # 5. Set Initial Conditions
    G.u = u_rest

    # 6. Record State
    M = b2.StateMonitor(G, 'u', record=True)
    S = b2.SpikeMonitor(G)

    # 7. Run Simulation
    print("Running simulation...")
    b2.run(100 * b2.ms)
    print("Simulation finished.")

    # 8. Plot results
    plt.figure(figsize=(10, 4))
    plt.plot(M.t/b2.ms, M.u[0]/b2.mV, label='Membrane Potential')
    # Plot spikes
    plt.plot(S.t/b2.ms, [threshold/b2.mV]*len(S.t), 'ro', label='Spikes')
    
    plt.xlabel('Time (ms)')
    plt.ylabel('Voltage (mV)')
    plt.title('Single Neuron - Leaky Integrate-and-Fire with Spikes')
    plt.axhline(threshold/b2.mV, ls='--', c='r', label='Threshold')
    plt.legend()
    plt.grid(True)
    
    output_file = 'single_neuron_spikes.png'
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

if __name__ == "__main__":
    run_simulation()
