<script>
  import { onMount, onDestroy } from "svelte";
  import * as tf from "@tensorflow/tfjs";
  import { loadModel } from "$lib/data/loadMnistAssets.js";
  import ImagesCanvas from "$lib/components/ImagesCanvas.svelte";
  import HorizontalBarChart from "$lib/charts/HorizontalBarChart.svelte";
  import LayerDetailModal from '$lib/components/LayerDetailModal.svelte';
  import { fade, fly } from 'svelte/transition';

  export let pixelMatrix = [];

  // --- State ---
  let model = null;
  let modelDescription = null;
  let allLayerInfo = [];
  let probs = [];
  let isLoading = true;
  let isProcessing = false;
  let error = null;

  // This variable holds the data for the currently selected layer to show the modal
  let selectedLayerData = null; 
  
  // --- Debouncing Logic for Performance ---
  let inferenceTimer;

  $: if (pixelMatrix.length > 0 && model) {
    clearTimeout(inferenceTimer);
    isProcessing = true;
    inferenceTimer = setTimeout(() => runInference(), 400);
  }

  // --- Lifecycle ---
  onMount(async () => {
    try {
      // Load model and description in parallel for speed
      [model, modelDescription] = await Promise.all([
        loadModel(),
        fetch(`/models/mnist_model_tfjs_tiny/mnist_model_description.json`).then(res => {
           if (!res.ok) throw new Error("Network description file not found.");
           return res.json()
        })
      ]);
    } catch (e) { 
      error = e.message; 
      console.error("Initialization Error:", e);
    } finally { 
      isLoading = false; 
    }
  });

  onDestroy(() => {
    clearTimeout(inferenceTimer);
    if(model) model.dispose();
  });

  // --- Core Inference Function ---
  function runInference() {
    if (!model || !pixelMatrix || pixelMatrix.length === 0) {
      isProcessing = false;
      return;
    }
    
    // Using requestAnimationFrame ensures the UI doesn't freeze during processing
    requestAnimationFrame(() => {
      tf.tidy(() => {
        let processed = [];
        let previousActivations = [pixelMatrix.flat()]; // Start with the user's drawing as the first "activation"
        let currentOutput = tf.tensor4d(pixelMatrix.flat(), [1, 28, 28, 1]);

        for (const layer of model.layers) {
          const type = layer.getClassName();
          const inputShape = currentOutput.shape.slice(1); // Shape before applying the layer
          currentOutput = layer.apply(currentOutput);     // Shape after applying the layer

          // We only care about showing Conv2D layers in the main pipeline
          if (type === 'Conv2D') {
            const desc = modelDescription.find(d => d.name === layer.name);
            const act3D = currentOutput.squeeze(0);
            const actMaps = tf.split(act3D, act3D.shape[2], 2);
            
            processed.push({
              name: layer.name,
              type: type,
              inputShape: inputShape,
              outputShape: layer.outputShape.slice(1),
              kernels: desc?.weights.map(w => w.weights.flat()) || [],
              biases: desc?.weights.map(w => w.bias) || [],
              activations: actMaps.map(t => Array.from(t.dataSync())),
              inputActivations: previousActivations, // Pass the previous layer's output to the modal
            });
          }
          
          // The output of this layer becomes the input for the next one in the deep dive
          if (type === 'Conv2D' || type === 'MaxPooling2D') {
             const act3D = currentOutput.squeeze(0);
             const actMaps = tf.split(act3D, act3D.shape[2], 2);
             previousActivations = actMaps.map(t => Array.from(t.dataSync()));
          }
        }
        
        // Update Svelte state variables
        probs = Array.from(tf.softmax(currentOutput).dataSync());
        allLayerInfo = processed;
      });
      isProcessing = false;
    });
  }

  const handleLayerClick = (layer) => {
    selectedLayerData = layer;
  };
</script>

<div class="arch-viz-container">
    {#if error}
        <p class="error-message">{error}</p>
    {:else if isLoading}
        <div class="placeholder-text">Loading Neural Network...</div>
    {:else}
      <div class="arch-flow">
          <div class="stage input-stage">
              <div class="stage-header">Input</div>
              {#if pixelMatrix.length}
                  <div class="input-image">
                    <ImagesCanvas imageData={pixelMatrix.flat()} width={28} height={28} />
                  </div>
              {/if}
          </div>

          {#each allLayerInfo as layer (layer.name)}
              <div class="flow-arrow" transition:fade|local>→</div>
              <button class="stage conv-stage" on:click={() => handleLayerClick(layer)} transition:fly|local={{y:20, duration: 300}}>
                  <div class="stage-header">{layer.name}</div>
                  <div class="layer-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M2 2h20v20H2z" opacity=".2"/><path d="M4 4h7v7H4zM4 13h7v7H4zM13 4h7v7h-7zM13 13h7v7h-7z"/></svg>
                  </div>
                  <div class="shape-info">{layer.outputShape[2]} feature maps</div>
                  <div class="click-prompt">Deep Dive</div>
              </button>
          {/each}

          <div class="flow-arrow" transition:fade|local>→</div>
          <div class="stage output-stage">
              <div class="stage-header">Prediction</div>
              {#if probs.length}
                  <div class="chart-container"><HorizontalBarChart data={probs} /></div>
              {/if}
          </div>
      </div>
    {/if}
    
    {#if isProcessing}
      <div class="loading-overlay" transition:fade={{duration: 150}}>
        <div class="spinner"></div>
      </div>
    {/if}
</div>

{#if selectedLayerData}
    <LayerDetailModal 
        layerData={selectedLayerData} 
        on:close={() => selectedLayerData = null}
    />
{/if}

<style>
:root {
  --color-bg-dark: #1a1a2e;
  --color-bg-light: #16213e;
  --color-primary: #0f3460;
  --color-accent: #e94560;
  --color-text: #dcdcdc;
  --color-glow: rgba(233, 69, 96, 0.5);
  --border-radius: 12px;
}

.arch-viz-container {
  position: relative;
  background: var(--color-bg-dark);
  padding: 1.5rem 2rem;
  border-radius: var(--border-radius);
  color: var(--color-text);
  overflow-x: auto;
  height: 100%;
  border: 1px solid var(--color-primary);
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.arch-flow {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: fit-content;
  height: 100%;
  padding: 0 0.5rem;
}

.stage {
  flex-shrink: 0;
  background: var(--color-bg-light);
  border: 1px solid var(--color-primary);
  border-radius: var(--border-radius);
  padding: 1rem;
  height: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 130px;
  text-align: center;
}

.conv-stage {
  cursor: pointer;
  transition: all 0.2s ease-out;
  background: none;
  border-style: dashed;
}

.conv-stage:hover {
  border-color: var(--color-accent);
  background: var(--color-bg-light);
  transform: translateY(-5px) scale(1.05);
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.stage-header {
  font-weight: bold;
  font-size: 0.9rem;
  text-align: center;
  margin-bottom: 0.5rem;
  color: var(--color-text);
}

.conv-stage .stage-header {
    color: var(--color-primary);
    transition: color 0.2s ease-out;
}
.conv-stage:hover .stage-header {
    color: var(--color-accent);
}

.shape-info {
    font-size: 0.75rem;
    color: var(--color-text);
    opacity: 0.7;
    font-weight: normal;
}

.input-image {
  border: 2px solid var(--color-primary);
  border-radius: 4px;
  background: #000;
  padding: 5px;
}

.flow-arrow {
  font-size: 2rem;
  color: var(--color-primary);
  opacity: 0.6;
}

.layer-icon {
  width: 48px;
  height: 48px;
  color: var(--color-primary);
  margin: 0.5rem 0;
  transition: color 0.2s ease-out;
}
.conv-stage:hover .layer-icon {
    color: var(--color-accent);
}

.click-prompt {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 0.5rem;
  color: var(--color-accent);
  opacity: 0;
  transition: opacity 0.2s;
}

.conv-stage:hover .click-prompt {
  opacity: 1;
}

.output-stage {
    min-width: 280px;
}

.chart-container {
    width: 100%;
    height: 100%;
    min-width: 250px;
}

.placeholder-text, .error-message {
  font-size: 1.2rem;
  text-align: center;
  width: 100%;
  color: var(--color-text);
  opacity: 0.7;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.error-message { color: #ff8a8a; }

.loading-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 20;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius);
  cursor: wait;
}
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--color-primary);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>