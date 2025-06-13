<script>
    import { createEventDispatcher, onMount, onDestroy } from 'svelte';
    // FIX: Import the missing 'fade' and 'fly' transitions
    import { fade, fly } from 'svelte/transition';
    import ImagesCanvas from '$lib/components/ImagesCanvas.svelte';
    import ConvolutionAnimator from '$lib/components/ConvolutionAnimator.svelte';
  
    export let layerData;
    const dispatch = createEventDispatcher();
  
    let selectedInputIndex = 0;
    let selectedKernelIndex = 0;
  
    $: selectedInputMap = layerData.inputActivations[selectedInputIndex];
    $: selectedKernel = layerData.kernels[selectedKernelIndex];
    $: selectedOutputMap = layerData.activations[selectedKernelIndex];
    $: selectedBias = layerData.biases[selectedKernelIndex];
  
    const closeModal = () => dispatch('close');
    const handleKeydown = (e) => e.key === 'Escape' && closeModal();
  
    onMount(() => window.addEventListener('keydown', handleKeydown));
    onDestroy(() => window.removeEventListener('keydown', handleKeydown));
  </script>
  
  <div class="modal-backdrop" on:click={closeModal} transition:fade={{duration: 150}}></div>
  
  <div class="modal-content" role="dialog" aria-modal="true" transition:fly={{ y: 50, duration: 300 }}>
    <!-- FIX: Redesigned close button with a sleek SVG and better styling -->
    <button class="close-btn" on:click={closeModal} aria-label="Close modal">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 10.586l4.95-4.95 1.414 1.414-4.95 4.95 4.95 4.95-1.414 1.414-4.95-4.95-4.95 4.95-1.414-1.414 4.95-4.95-4.95-4.95L7.05 5.636z"/>
      </svg>
    </button>
    
    <header>
      <h1>Layer Deep Dive: <span>{layerData.name}</span></h1>
      <p>This layer takes <strong>{layerData.inputActivations.length}</strong> input channels, applies <strong>{layerData.kernels.length}</strong> unique filters, and produces <strong>{layerData.activations.length}</strong> output feature maps.</p>
    </header>
  
    <div class="interactive-core">
      <div class="panel selection-panel">
        <h3>1. Select Input Channel</h3>
        <div class="item-grid">
          {#each layerData.inputActivations as input, i}
            <button class="grid-btn" class:active={selectedInputIndex === i} on:click={() => selectedInputIndex = i}>
              <ImagesCanvas imageData={input} width={layerData.inputShape[1]} height={layerData.inputShape[2]} />
              <span>In {i}</span>
            </button>
          {/each}
        </div>
      </div>
  
      <div class="panel selection-panel">
        <h3>2. Select Filter</h3>
        <div class="item-grid">
          {#each layerData.kernels as kernel, i}
            <button class="grid-btn" class:active={selectedKernelIndex === i} on:click={() => selectedKernelIndex = i}>
              <ImagesCanvas imageData={kernel} width={3} height={3} />
              <span>Filter {i}</span>
            </button>
          {/each}
        </div>
      </div>
  
      <div class="panel animator-panel">
        <h3>3. Observe the Operation</h3>
        <div class="animator-wrapper">
          <ConvolutionAnimator 
            inputMap={selectedInputMap}
            kernel={selectedKernel}
            outputMap={selectedOutputMap}
            inputShape={{w: layerData.inputShape[1], h: layerData.inputShape[2]}}
            kernelShape={{w: 3, h: 3}}
          />
        </div>
         <div class="bias-info">
          <strong>Bias Added to Output:</strong> <span>{selectedBias.toFixed(4)}</span>
        </div>
      </div>
    </div>
  </div>
  
  <style>
    .modal-backdrop {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(18, 18, 18, 0.7);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      z-index: 99;
    }
    .modal-content {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: min(1600px, 95vw);
      height: 90vh;
      background: #1a1a2e;
      border: 1px solid #0f3460;
      border-radius: 16px;
      z-index: 100;
      box-shadow: 0 20px 60px rgba(0,0,0,0.6);
      padding: 2rem 3rem;
      display: flex;
      flex-direction: column;
      color: #e0e0e0;
      font-family: 'Montserrat', sans-serif;
    }
    .close-btn {
      position: absolute;
      top: 1rem;
      right: 1rem;
      background: rgba(255,255,255,0.1);
      border: none;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      color: #e0e0e0;
      cursor: pointer;
      transition: background-color 0.2s, transform 0.2s;
    }
    .close-btn:hover {
      background: #e94560;
      transform: scale(1.1);
    }
    .close-btn svg { width: 24px; height: 24px; }
    header {
      text-align: center;
      margin-bottom: 1.5rem;
      flex-shrink: 0;
    }
    header h1 { margin: 0; }
    header h1 span { color: #e94560; }
    header p { opacity: 0.8; margin-top: 0.5rem; }
    .interactive-core {
      display: grid;
      grid-template-columns: 240px 240px 1fr;
      gap: 2rem;
      flex-grow: 1;
      min-height: 0;
    }
    .panel {
      background: rgba(15, 52, 96, 0.2);
      padding: 1.5rem;
      border-radius: 12px;
      display: flex;
      flex-direction: column;
      border: 1px solid #0f3460;
    }
    .panel h3 {
      margin: 0 0 1rem 0;
      text-align: center;
      color: #fff;
      font-size: 1.1rem;
      font-weight: 600;
      border-bottom: 1px solid #0f3460;
      padding-bottom: 0.75rem;
    }
    .selection-panel .item-grid {
      overflow-y: auto;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(50px, 1fr));
      gap: 12px;
      padding: 0.5rem;
    }
    .grid-btn {
      background: #16213e;
      border: 2px solid #0f3460;
      border-radius: 8px;
      padding: 5px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      gap: 5px;
      align-items: center;
      color: #e0e0e0;
      font-size: 0.7rem;
    }
    .grid-btn:hover, .grid-btn.active {
      border-color: #e94560;
      transform: scale(1.05);
      background: #e9456022;
    }
    .grid-btn span { font-weight: bold; }
    .animator-panel {
      gap: 1rem;
      text-align: center;
    }
    .animator-wrapper {
      flex-grow: 1;
      display: grid;
      place-items: center;
      background: rgba(0,0,0,0.2);
      border-radius: 8px;
      padding: 1rem;
    }
    .bias-info {
      font-weight: 500;
      background: #16213e;
      padding: 0.75rem;
      border-radius: 8px;
      margin-top: 1rem;
      border: 1px solid #0f3460;
    }
    .bias-info span {
        color: #e94560;
        font-weight: 700;
    }
  </style>