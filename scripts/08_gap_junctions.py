import brian2 as b2
import matplotlib.pyplot as plt

def run_simulation():
    b2.start_scope()

    # Parameters
    tau = 10*b2.ms
    v_rest = -70*b2.mV
    
    eqs = '''
    dv/dt = (-(v-v_rest) + I_gap + I_ext)/tau : volt
    I_gap : volt
    I_ext : volt
    '''
    
    # Two neurons
    G = b2.NeuronGroup(2, eqs, method='exact')
    G.v = [-70, -60]*b2.mV # Different initial conditions
    
    # Drive neuron 0, leave neuron 1 passive
    # This will pull neuron 0 up.
    G.I_ext = [20, 0]*b2.mV 

    # Electrical Synapse (Gap Junction)
    # The current flows continuously depending on voltage difference
    # We use a summed variable in the synapse model itself.
    # 'summed' means: for each post-synaptic neuron, sum this value from all pre-synaptic partners.
    S = b2.Synapses(G, G, '''
             w : 1
             I_gap_post = w * (v_pre - v_post) : volt (summed)
             ''')
    S.connect(i=0, j=1) # 0 -> 1
    S.connect(i=1, j=0) # 1 -> 0
    S.w = 0.5

    # Monitor
    M = b2.StateMonitor(G, 'v', record=True)

    print("Running Gap Junction Simulation...")
    b2.run(100*b2.ms)
    print("Finished.")

    plt.figure(figsize=(10, 5))
    plt.plot(M.t/b2.ms, M.v[0]/b2.mV, 'b', label='Neuron 0 (Driven)')
    plt.plot(M.t/b2.ms, M.v[1]/b2.mV, 'r--', label='Neuron 1 (Coupled)')
    
    plt.xlabel('Time (ms)')
    plt.ylabel('Voltage (mV)')
    plt.title('Gap Junction Coupling')
    plt.legend()
    plt.grid(True)
    
    output_file = 'gap_junctions.png'
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

if __name__ == "__main__":
    run_simulation()
