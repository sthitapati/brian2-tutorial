import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np

def run_simulation():
    b2.start_scope()

    # Parameters
    N = 100 # Number of pairs
    tau_pre = tau_post = 20 * b2.ms
    A_pre = 0.01
    A_post = -A_pre * 1.05
    xmax = 100 * b2.ms # range of time differences

    # 1. Spike Times
    # We want time differences delta_t = t_post - t_pre
    # varying from -xmax to +xmax
    delta_t = np.linspace(-xmax, xmax, N)
    
    # We set t_pre constant for all, and vary t_post
    t_pre_spikes = np.ones(N) * 150 * b2.ms
    t_post_spikes = t_pre_spikes + delta_t

    # 2. SpikeGeneratorGroups
    # Pre-synaptic neurons (indices 0 to N-1)
    Pre = b2.SpikeGeneratorGroup(N, np.arange(N), t_pre_spikes)
    # Post-synaptic neurons (indices 0 to N-1)
    Post = b2.SpikeGeneratorGroup(N, np.arange(N), t_post_spikes)

    # 3. Synapses with STDP
    # This block defines the plasticity model.
    # eq_stdp:
    #   dap/dt: "Trace" of pre-synaptic activity (decays to 0)
    #   dam/dt: "Trace" of post-synaptic activity (decays to 0)
    #
    # We essentially "remember" recent spikes to calculate delta_w.
    
    eqs_stdp = '''
    w : 1
    dap/dt = -ap / tau_pre : 1 (event-driven)
    dam/dt = -am / tau_post : 1 (event-driven)
    '''
    
    S = b2.Synapses(Pre, Post, model=eqs_stdp,
                 on_pre='''
                 w = clip(w + A_post * am, 0, inf)
                 ap += 1
                 ''',
                 on_post='''
                 w = clip(w + A_pre * ap, 0, inf)
                 am += 1
                 ''')
    
    # Connect i to i (one-to-one mapping for the pairs)
    S.connect(j='i')
    
    # Initial weights
    S.w = 0.5 

    # 4. Run
    # Run long enough for the latest spike
    # Max time is 150 + 100 = 250ms. 300ms is safe.
    print("Running STDP Simulation...")
    b2.run(300 * b2.ms)
    print("Finished.")

    # 5. Plotting
    # Change in weight
    delta_w = S.w - 0.5

    plt.figure(figsize=(8, 5))
    plt.plot(delta_t/b2.ms, delta_w, 'b-', linewidth=2)
    plt.xlabel(r'$\Delta t$ (ms) (Post - Pre)')
    plt.ylabel(r'$\Delta w$')
    plt.title('Spike-Timing Dependent Plasticity (STDP) Curve')
    plt.axhline(0, ls='-', c='k', alpha=0.5)
    plt.axvline(0, ls='-', c='k', alpha=0.5)
    plt.grid(True)
    
    output_file = 'stdp_curve.png'
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

if __name__ == "__main__":
    run_simulation()
