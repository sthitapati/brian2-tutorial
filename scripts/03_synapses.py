import brian2 as b2
import matplotlib.pyplot as plt

def run_simulation():
    b2.start_scope()

    # Parameters
    tau = 10 * b2.ms
    u_rest = -70 * b2.mV
    threshold = -55 * b2.mV
    reset = -70 * b2.mV
    
    # Differential Equation (LIF)
    # We add a parameter 'I' which we can vary per group
    eqs = '''
    du/dt = (-(u - u_rest) + I) / tau : volt
    I : volt
    '''

    # 1. Source Neuron: Driven to spike
    # I = 20 mV (effectively shifts rest potential to -50mV if we ignore threshold, 
    # but here it's an additive drive). 
    # Actually, let's just make it simple: 
    # du/dt = ... + I
    # If I is large enough, it fires.
    Source = b2.NeuronGroup(1, eqs, threshold='u > threshold', reset='u = reset', method='exact')
    Source.I = 20 * b2.mV 
    Source.u = u_rest

    # 2. Target Neuron: Silent
    Target = b2.NeuronGroup(1, eqs, threshold='u > threshold', reset='u = reset', method='exact')
    Target.I = 0 * b2.mV # No input drive
    Target.u = u_rest

    # 3. Synapse
    # Connect Source -> Target
    # Spikes travel from Source (pre-synaptic) to Target (post-synaptic).
    #
    # on_pre='u += 2*mV'
    # This means: "When a pre-synaptic spike arrives, instantaneously increase
    # the post-synaptic neuron's variable 'u' by 2 mV."
    #
    # This simulates an Excitatory Post-Synaptic Potential (EPSP).
    S = b2.Synapses(Source, Target, on_pre='u += 2*mV')
    S.connect()

    # 4. Monitors
    M_source = b2.StateMonitor(Source, 'u', record=0)
    S_source = b2.SpikeMonitor(Source)
    
    M_target = b2.StateMonitor(Target, 'u', record=0)
    
    # 5. Run
    print("Running Synapse Simulation...")
    b2.run(100 * b2.ms)
    print("Finished.")

    # 6. Plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Source Plot
    axs[0].plot(M_source.t/b2.ms, M_source.u[0]/b2.mV, 'b', label='Source Potential')
    axs[0].plot(S_source.t/b2.ms, [threshold/b2.mV]*len(S_source.t), 'ro', label='Source Spikes')
    axs[0].set_ylabel('Voltage (mV)')
    axs[0].set_title('Source Neuron (Driven)')
    axs[0].legend()
    axs[0].grid(True)

    # Target Plot
    axs[1].plot(M_target.t/b2.ms, M_target.u[0]/b2.mV, 'g', label='Target Potential')
    axs[1].set_ylabel('Voltage (mV)')
    axs[1].set_xlabel('Time (ms)')
    axs[1].set_title('Target Neuron (Receiving EPSPs)')
    axs[1].legend()
    axs[1].grid(True)
    
    output_file = 'synapse_plot.png'
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

if __name__ == "__main__":
    run_simulation()
