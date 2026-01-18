import brian2 as b2
import matplotlib.pyplot as plt

def run_simulation():
    b2.start_scope()

    # Parameters
    area = 20000*b2.um**2
    Cm = 1*b2.ufarad*b2.cm**-2 * area
    gl = 5e-5*b2.siemens*b2.cm**-2 * area
    El = -65*b2.mV
    EK = -90*b2.mV
    ENa = 50*b2.mV
    g_na = 100*b2.msiemens*b2.cm**-2 * area
    g_kd = 30*b2.msiemens*b2.cm**-2 * area
    VT = -63*b2.mV

    # The Hodgkin-Huxley Equations
    eqs = '''
    dv/dt = (gl*(El-v) - g_na*(m**3)*h*(v-ENa) - g_kd*(n**4)*(v-EK) + I)/Cm : volt
    dm/dt = 0.32*(mV**-1)*4*mV/exprel((13*mV-v+VT)/(4*mV))/ms*(1-m)-0.28*(mV**-1)*5*mV/exprel((v-VT-40*mV)/(5*mV))/ms*m : 1
    dn/dt = 0.032*(mV**-1)*5*mV/exprel((15*mV-v+VT)/(5*mV))/ms*(1-n)-.5*exp((10*mV-v+VT)/(40*mV))/ms*n : 1
    dh/dt = 0.128*exp((17*mV-v+VT)/(18*mV))/ms*(1-h)-4/(1+exp((40*mV-v+VT)/(5*mV)))/ms*h : 1
    I : amp
    '''

    group = b2.NeuronGroup(1, eqs, threshold='v > -40*mV', refractory='v > -40*mV', method='exponential_euler')
    group.v = El
    group.I = '0.7*nA'

    M = b2.StateMonitor(group, 'v', record=0)

    print("Running Hodgkin-Huxley Simulation...")
    b2.run(100*b2.ms)
    print("Finished.")

    plt.figure(figsize=(10, 5))
    plt.plot(M.t/b2.ms, M.v[0]/b2.mV)
    plt.xlabel('Time (ms)')
    plt.ylabel('Voltage (mV)')
    plt.title('Hodgkin-Huxley Model')
    plt.grid(True)
    
    output_file = 'hodgkin_huxley.png'
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

if __name__ == "__main__":
    run_simulation()
