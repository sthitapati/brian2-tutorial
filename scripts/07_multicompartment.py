import brian2 as b2
import matplotlib.pyplot as plt

def run_simulation():
    b2.start_scope()

    # Parameters
    # Standard properties for a cortical neuron (usually)
    cm = 1*b2.uF/b2.cm**2 # specific membrane capacitance
    Rm = 10000*b2.ohm*b2.cm**2 # specific membrane resistance
    Ri = 100*b2.ohm*b2.cm # intracellular resistivity
    
    # Morphology: Soma connected to a long dendrite
    morpho = b2.Soma(diameter=30*b2.um)
    morpho.dendrite = b2.Cylinder(length=500*b2.um, diameter=2*b2.um, n=50)

    # Channels (Passive leak only for visualization of attenuation)
    eqs = '''
    Im = gl * (El - v) : amp/meter**2
    I : amp (point current)
    gl = 1/Rm : siemens/meter**2
    El = -70*mV : volt
    '''

    neuron = b2.SpatialNeuron(morphology=morpho, model=eqs, Cm=cm, Ri=Ri, method='exponential_euler')
    neuron.v = -70*b2.mV

    # Inject current at the tip of the dendrite
    # The last compartment of the dendrite
    neuron.dendrite.I[-1] = 0.5*b2.nA 

    # Monitors
    # Record soma
    M_soma = b2.StateMonitor(neuron, 'v', record=[0])
    # Record dendrite tip (last compartment)
    # The dendrite has 50 compartments, so the last one is index 49.
    M_dendrite = b2.StateMonitor(neuron.dendrite, 'v', record=[49])
    
    print("Running Multicompartment Simulation...")
    b2.run(100*b2.ms)
    print("Finished.")

    plt.figure(figsize=(10, 5))
    plt.plot(M_soma.t/b2.ms, M_soma.v[0]/b2.mV, label='Soma (0 um)')
    plt.plot(M_dendrite.t/b2.ms, M_dendrite.v[0]/b2.mV, label='Dendrite Tip (500 um)')
    
    plt.xlabel('Time (ms)')
    plt.ylabel('Voltage (mV)')
    plt.title('Signal Attenuation in Cable Equation')
    plt.legend()
    plt.grid(True)
    
    output_file = 'multicompartment.png'
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

if __name__ == "__main__":
    run_simulation()
