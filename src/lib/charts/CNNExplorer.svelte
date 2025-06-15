<script>
  import { onMount, onDestroy } from "svelte";
  import * as tf from "@tensorflow/tfjs";
  import ImagesCanvas from "$lib/components/ImagesCanvas.svelte";
  import {
    loadModel,
  } from "$lib/data/loadMnistAssets.js";

  import HorizontalBarChart from "$lib/charts/HorizontalBarChart.svelte";

  let model = null;
  let imagesMeta = [];
  let currentIdx = 0;
  let inputTensor = null;
  let inputPixels = null; // For displaying the input image
  export let pixelMatrix = [];

  let allLayerActivations = []; // This will store { layerName, layerType, activations: [{channelIndex, pixels, displaySize, originalShape}]}
  let probs = null;

  // Helper to convert TensorFlow tensor to a flat JS array (async, non-blocking)
  const tensorToArrayAsync = async (t) => Array.from(await t.data());

  // Helper to normalize a single activation map tensor to [0,1] for grayscale display
  function normalizeActivation(tensor) {
    return tf.tidy(() => {
      const minVal = tensor.min();
      const maxVal = tensor.max();
      const range = maxVal.sub(minVal);

      // If range is very small (all values are nearly the same), return zeros or a constant.
      if (range.dataSync()[0] < 1e-7) {
        return tf.zerosLike(tensor);
      }
      return tensor.sub(minVal).div(range);
    });
  }

  async function runInferenceAndGetAllActivations() {
    if (!model || !inputTensor) return;

    // Use a single tidy for the whole inference, but only keep tensors needed for UI
    const activationsArr = [];
    let currentOutput = inputTensor;
    let lastProbs = null;

    for (let idx = 0; idx < model.layers.length; idx++) {
      const layer = model.layers[idx];
      let layerActivationData;
      try {
        currentOutput = layer.apply(currentOutput);
        const activationsForThisLayer = [];
        const layerOutputShape = currentOutput.shape;
        const layerClassName = layer.getClassName();

        // Only process Conv2D layers for visualization (skip Pool for speed)
        if (layerClassName.includes("Conv") && layerOutputShape.length === 4) {
          const [, h, w, c] = layerOutputShape;
          const displaySize = 16; // Reduce display size for speed
          // Only show up to 8 channels for speed
          const maxChannels = Math.min(8, c);
          const allChannels = tf.tidy(() => currentOutput.squeeze([0])); // [h, w, c]
          const resized = tf.tidy(() => tf.image.resizeNearestNeighbor(
            allChannels.expandDims(0),
            [displaySize, displaySize]
          ).squeeze([0])); // [displaySize, displaySize, c]
          const norm = tf.tidy(() => normalizeActivation(resized)); // [displaySize, displaySize, c]
          const normSplit = tf.split(norm, c, 2); // Array of [displaySize, displaySize, 1]
          for (let i = 0; i < c; i++) {
            activationsForThisLayer.push({
              channelIndex: i,
              pixels: await tensorToArrayAsync(normSplit[i]),
              originalShape: [h, w],
              displaySize: displaySize,
            });
          }
          normSplit.forEach((t, i) => { if (i < maxChannels) t.dispose(); });
          allChannels.dispose();
          resized.dispose();
          norm.dispose();
        } else if (layerClassName === "Dense" && layerOutputShape.length === 2) {
          // Only process last Dense layer for output
          if (idx === model.layers.length - 1) {
            const activationValues = await tensorToArrayAsync(currentOutput.squeeze());
            activationsForThisLayer.push({
              channelIndex: -1,
              pixels: activationValues,
              isDense: true,
              originalShape: [layerOutputShape[1]],
            });
          }
        } else if (layerClassName === "Flatten") {
          activationsForThisLayer.push({
            isFlatten: true,
            originalShape: layerOutputShape.slice(1),
          });
        }

        layerActivationData = {
          layerName: layer.name,
          layerType: layerClassName,
          outputShape: layer.outputShape,
          actualShape: layerOutputShape,
          params: layer.countParams(),
          activations: activationsForThisLayer,
        };
      } catch (error) {
        console.error(`Error processing layer ${layer.name}:`, error);
        layerActivationData = {
          layerName: layer.name,
          layerType: layer.getClassName(),
          error: true,
          params: layer.countParams(),
          outputShape: layer.outputShape,
          activations: [],
        };
      }
      activationsArr.push(layerActivationData);

      // Output probabilities only for last layer
      if (idx === model.layers.length - 1) {
        const logits =
          currentOutput.shape.length > 1 && currentOutput.shape[0] === 1
            ? currentOutput.flatten()
            : currentOutput;
        const soft = tf.softmax(logits);
        lastProbs = await tensorToArrayAsync(soft);
        soft.dispose();
      }
    }

    // Only update Svelte state once, outside tidy
    allLayerActivations = activationsArr.filter(
      (layer) => layer.layerType == 'Conv2D'
    );
    probs = lastProbs;
  }

  $: if (model && pixelMatrix.length > 0) {
    inputPixels = pixelMatrix.flat();
    inputTensor = tf.tensor4d(inputPixels, [1, 28, 28, 1]); // Reshape to [1, 28, 28, 1] for a single grayscale image
    runInferenceAndGetAllActivations();
  }

  onMount(async () => {
    try {
      const m = await loadModel();
      model = m;
    } catch (error) {
      console.error("Error onMount:", error);
    }
  });

  onDestroy(() => {
    if (inputTensor) inputTensor.dispose();
    if (model) model.dispose();
  });
</script>

<div class="cnn-explorer-new">
  <div class="pipeline-stage input-stage">
    {#if inputPixels}
      <div class="img">
        <ImagesCanvas
          imageData={inputPixels}
          width={28}
          height={28}
        />
      </div>
    {:else}
      <p>Loading input...</p>
    {/if}
  </div>

  {#each allLayerActivations as layerData}
    <div
      class="pipeline-stage layer-stage"
      class:error-stage={layerData.error}
    >
      {#if layerData.activations && !layerData.error}
        {#if layerData.activations.length > 0}
          <div class="activation-maps-grid-new">
            {#each layerData.activations as activation (activation.channelIndex)}
              <div class="img">
                <ImagesCanvas
                  imageData={activation.pixels}
                  width={activation.displaySize}
                  height={activation.displaySize}
                />
              </div>
            {/each}
          </div>
        {:else if !layerData.error}
          <p class="no-viz-placeholder">
            No specific visualization (e.g., {layerData.layerType})
          </p>
        {/if}
      {/if}
    </div>
  {/each}
  <div class="pipeline-stage output-stage">
    {#if probs}
      <div class="output-chart-container">
        <HorizontalBarChart data={probs} />
      </div>
    {:else}
      <p>Loading predictions...</p>
    {/if}
  </div>
</div>

<style>
  .cnn-explorer-new {
    padding: 20px;
    width: 80%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 10px;
    align-items: center;
  }

  .pipeline-stage {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 10px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    display: flex;
    flex-direction: column; /* Stack content vertically within a stage */
    gap: 12px; /* Space between elements inside a stage */
  }

  .img {
    width: 40px;
    aspect-ratio: 1 / 1;
    display: flex;
  }

  .pipeline-stage.error-stage {
    /* Style for layers that encountered an error */
    border-color: #f87171;
    background-color: #fef2f2; /* Light red background */
  }

  /* Grid for displaying multiple activation maps */
  .activation-maps-grid-new {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }

  /* Placeholder text if a layer has no specific visualization */
  .no-viz-placeholder {
    font-size: 12px;
    color: #9ca3af; /* Lighter gray text */
    text-align: center;
    padding: 15px;
    background: #f3f4f6;
    border-radius: 4px;
    flex-grow: 1; /* Allow it to take space */
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* Output stage specific styling */
  .output-stage {
    min-width: 200px; /* Slightly wider for the prediction chart */
  }
  
  .output-chart-container {
    /* Container for the PredictionChart component */
    width: 100%;
    display: flex; /* Helps in centering/sizing the chart if PredictionChart is a block */
    align-items: center;
    justify-content: center;
  }
</style>
