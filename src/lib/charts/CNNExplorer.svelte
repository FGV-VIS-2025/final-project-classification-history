<script>
  import { onMount, onDestroy } from "svelte";
  import * as tf from "@tensorflow/tfjs";
  // Make sure these paths are correct for your project structure
  import ImagesCanvas from "$lib/components/ImagesCanvas.svelte";
  import PredictionChart from "$lib/components/PredictionChart.svelte";
  import {
    loadModel,
    loadResume,
    pngToTensor,
  } from "$lib/data/loadMnistAssets.js";
  import { base } from "$app/paths";

  let model = null;
  let imagesMeta = [];
  let currentIdx = 0;
  let inputTensor = null;
  let inputPixels = null; // For displaying the input image

  let allLayerActivations = []; // This will store { layerName, layerType, activations: [{channelIndex, pixels, displaySize, originalShape}]}
  let probs = null;
  let predicted = null;
  let layerInfoForHeader = { count: 0 }; // For the header badge

  // Helper to convert TensorFlow tensor to a flat JS array
  const tensorToArray = (t) => Array.from(t.dataSync());

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

    if (layerInfoForHeader.count === 0 && model.layers) {
      layerInfoForHeader.count = model.layers.length;
    }

    const newAllLayerActivations = [];
    // console.log("Starting inference and activation extraction...");

    tf.tidy(() => {
      // Outer tidy scope for the entire inference and activation extraction process
      let currentOutput = inputTensor;

      model.layers.forEach((layer, idx) => {
        let layerActivationData;
        try {
          currentOutput = layer.apply(currentOutput); // Get output of the current layer

          const activationsForThisLayer = [];
          const layerOutputShape = currentOutput.shape; // Actual shape from tensor
          const layerClassName = layer.getClassName();

          // Process layers that produce image-like activations (Conv2D, Pooling)
          if (
            (layerClassName.includes("Conv") ||
              layerClassName.includes("Pool")) &&
            layerOutputShape.length === 4
          ) {
            const [, h, w, c] = layerOutputShape; // Batch, Height, Width, Channels
            const numChannelsToDisplay = Math.min(c, 6); // Show up to 6 channels
            const displaySize = 32; // Render each activation map at 32x32 pixels

            for (let i = 0; i < numChannelsToDisplay; i++) {
              // Inner tidy scope for processing each channel to manage memory
              tf.tidy(() => {
                const singleChannelTensor = currentOutput
                  .slice([0, 0, 0, i], [1, h, w, 1])
                  .squeeze();
                const resizedTensor = tf.image.resizeNearestNeighbor(
                  singleChannelTensor.expandDims(-1),
                  [displaySize, displaySize],
                );
                const normalizedTensor = normalizeActivation(resizedTensor); // Normalize values to [0,1] for display

                activationsForThisLayer.push({
                  channelIndex: i,
                  pixels: tensorToArray(normalizedTensor),
                  originalShape: [h, w], // Store original H, W before resize
                  displaySize: displaySize,
                });
              }); // End inner tidy scope for channel
            }
          } else if (
            layerClassName === "Dense" &&
            layerOutputShape.length === 2
          ) {
            // Handle Dense layers
            tf.tidy(() => {
              const activationValues = tensorToArray(currentOutput.squeeze()); // Get neuron activations
              activationsForThisLayer.push({
                channelIndex: -1, // Special marker for dense layer
                pixels: activationValues,
                isDense: true,
                originalShape: [layerOutputShape[1]], // Number of neurons
              });
            });
          } else if (layerClassName === "Flatten") {
            // Handle Flatten layers
            activationsForThisLayer.push({
              isFlatten: true,
              originalShape: layerOutputShape.slice(1), // Shape after flattening
            });
          }
          // Other layer types (e.g., Dropout, pure Activation layers) might not produce new visualizable maps
          // and will be passed through. Add more conditions if needed.

          layerActivationData = {
            layerName: layer.name,
            layerType: layerClassName,
            outputShape: layer.outputShape, // Output shape from Keras model config
            actualShape: layerOutputShape, // Actual runtime tensor shape
            params: layer.countParams(),
            activations: activationsForThisLayer,
          };
        } catch (error) {
          console.error(`Error processing layer ${layer.name}:`, error);
          // Create a placeholder if a layer fails, so the pipeline doesn't break
          layerActivationData = {
            layerName: layer.name,
            layerType: layer.getClassName(),
            error: true,
            params: layer.countParams(),
            outputShape: layer.outputShape,
            activations: [],
          };
        }
        newAllLayerActivations.push(layerActivationData);

        // If this is the last layer, calculate probabilities for the output chart
        if (idx === model.layers.length - 1) {
          tf.tidy(() => {
            // Ensure logits is a 1D tensor for softmax
            const logits =
              currentOutput.shape.length > 1 && currentOutput.shape[0] === 1
                ? currentOutput.flatten()
                : currentOutput;
            const soft = tf.softmax(logits);
            probs = tensorToArray(soft);
            predicted = probs.indexOf(Math.max(...probs)); // Find the predicted class index
          });
        }
      }); // End model.layers.forEach
    }); // End outer tf.tidy()

    allLayerActivations = newAllLayerActivations; // Update the reactive variable
    // console.log("Finished activation extraction:", allLayerActivations);
  }

  async function pick(idx) {
    currentIdx = idx;
    const meta = imagesMeta[idx];
    if (!meta) return;

    if (inputTensor) inputTensor.dispose(); // Dispose previous tensor
    // Load new image as tensor
    inputTensor = await pngToTensor(`${base}/${meta.filepath}`);

    // Get pixel data for the input image display
    // Assuming pngToTensor normalizes to [0,1] and inputTensor is [1,H,W,1] or similar
    // tensorToArray will flatten it, ImagesCanvas needs to know H, W.
    inputPixels = tensorToArray(inputTensor);

    await runInferenceAndGetAllActivations(); // Run inference and get all activations
  }

  onMount(async () => {
    try {
      const [m, resume] = await Promise.all([loadModel(), loadResume()]);
      model = m;
      imagesMeta = resume;
      if (imagesMeta.length > 0) {
        await pick(0); // Load the first image and run inference
      } else {
        console.error("No images loaded from resume.");
      }
    } catch (error) {
      console.error("Error onMount:", error);
    }
  });

  onDestroy(() => {
    if (inputTensor) inputTensor.dispose();
    if (model) model.dispose();
    // console.log("CNN Visualizer destroyed, tensors disposed.");
  });
</script>

<div class="cnn-explorer-new">
  <div class="header-new">
    <h2>CNN Visualizer</h2>
    <div class="model-info-new">
      <span class="badge-new">Model: MNIST CNN</span>
      <span class="badge-new">Layers: {layerInfoForHeader.count}</span>
      <select
        bind:value={currentIdx}
        on:change={(e) => pick(+e.target.value)}
        title="Select Input Image"
      >
        {#each imagesMeta as img, i}
          <option value={i}>Image #{i} (Label: {img.label})</option>
        {/each}
      </select>
    </div>
  </div>

  <div class="cnn-visualization-pipeline-container">
    <div class="cnn-visualization-pipeline">
      <div class="pipeline-stage input-stage">
        <h3>Input</h3>
        {#if inputPixels}
          <div class="input-image-container">
            <ImagesCanvas
              imageData={inputPixels}
              width={28}
              height={28}
              scale={4}
            />
          </div>
        {:else}
          <p>Loading input...</p>
        {/if}
      </div>

      {#each allLayerActivations as layerData, layerIndex (layerData.layerName)}
        <div class="pipeline-connector">
          <svg
            width="40"
            height="100%"
            viewBox="0 0 20 100"
            preserveAspectRatio="xMidYMid meet"
          >
            <line
              x1="10"
              y1="0"
              x2="10"
              y2="100"
              stroke="#d1d5db"
              stroke-width="2"
              stroke-dasharray="4 2"
            />
            <polyline
              points="6,46 14,50 6,54"
              fill="none"
              stroke="#d1d5db"
              stroke-width="2"
            />
          </svg>
        </div>
        <div
          class="pipeline-stage layer-stage"
          class:error-stage={layerData.error}
        >
          <div class="layer-header">
            <span class="layer-name-new" title={layerData.layerName}
              >{layerData.layerName}</span
            >
            <span class="layer-type-badge">{layerData.layerType}</span>
          </div>
          <div class="layer-meta">
            {#if layerData.error}
              <p class="error-message">Error processing this layer.</p>
            {:else}
              <span
                >Output: {layerData.actualShape
                  ? layerData.actualShape.slice(1).join(" × ")
                  : "N/A"}</span
              >
              <span>Params: {layerData.params?.toLocaleString() ?? "N/A"}</span>
            {/if}
          </div>
          {#if layerData.activations && !layerData.error}
            {#if layerData.activations.length > 0 && layerData.activations[0].isDense}
              <div class="dense-activations-container">
                <p class="dense-info">
                  Dense Activations ({layerData.activations[0].originalShape[0]}
                  neurons)
                </p>
                <div class="dense-values">
                  {#each layerData.activations[0].pixels.slice(0, 10) as val, i (i)}
                    <span
                      class="dense-value"
                      title={`Neuron ${i}: ${val.toFixed(3)}`}
                      >{val.toFixed(2)}</span
                    >
                  {/each}
                  {#if layerData.activations[0].pixels.length > 10}...{/if}
                </div>
              </div>
            {:else if layerData.activations.length > 0 && layerData.activations[0].isFlatten}
              <div class="flatten-layer-info">
                <p>Flatten Layer</p>
                <span
                  >Output Dim: {layerData.activations[0].originalShape.join(
                    " × ",
                  )}</span
                >
              </div>
            {:else if layerData.activations.length > 0}
              <div class="activation-maps-grid-new">
                {#each layerData.activations as activation (activation.channelIndex)}
                  <div
                    class="activation-map-item"
                    title={`Channel ${activation.channelIndex} (Original: ${activation.originalShape.join("×")})`}
                  >
                    <ImagesCanvas
                      imageData={activation.pixels}
                      width={activation.displaySize}
                      height={activation.displaySize}
                      scale={1.5}
                    />
                    <span class="map-channel-label"
                      >Ch {activation.channelIndex}</span
                    >
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
      <div class="pipeline-connector">
        <svg
          width="40"
          height="100%"
          viewBox="0 0 20 100"
          preserveAspectRatio="xMidYMid meet"
        >
          <line
            x1="10"
            y1="0"
            x2="10"
            y2="100"
            stroke="#d1d5db"
            stroke-width="2"
            stroke-dasharray="4 2"
          />
          <polyline
            points="6,46 14,50 6,54"
            fill="none"
            stroke="#d1d5db"
            stroke-width="2"
          />
        </svg>
      </div>
      <div class="pipeline-stage output-stage">
        <h3>Output</h3>
        {#if predicted !== null && imagesMeta[currentIdx]}
          <div class="prediction-badge-new">
            Predicted: <strong>{predicted}</strong> (Actual: {imagesMeta[
              currentIdx
            ]?.label})
          </div>
        {/if}
        {#if probs}
          <div class="output-chart-container">
            <PredictionChart probabilities={probs} predictedClass={predicted} />
          </div>
        {:else}
          <p>Loading predictions...</p>
        {/if}
      </div>
    </div>
  </div>
</div>

<style>
  /* General container for the whole visualizer */
  .cnn-explorer-new {
    background: #f9fafb; /* Light gray page background */
    border-radius: 8px;
    padding: 20px;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    color: #374151; /* Default text color */
    max-width: 100%;
    overflow: hidden; /* Prevent page scrollbars if pipeline is too wide for viewport initially */
  }

  /* Header styles */
  .header-new {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 1px solid #e5e7eb; /* Light border */
  }

  .header-new h2 {
    margin: 0;
    color: #1f2937; /* Darker title color */
    font-size: 22px;
    font-weight: 600;
  }

  .model-info-new {
    display: flex;
    align-items: center;
    gap: 15px; /* Space between items in model info */
  }

  .model-info-new select {
    padding: 8px 12px;
    border-radius: 6px;
    border: 1px solid #d1d5db;
    background-color: #fff;
    font-size: 14px;
    cursor: pointer;
    outline: none;
  }
  .model-info-new select:hover {
    border-color: #9ca3af;
  }
  .model-info-new select:focus {
    border-color: #3b82f6; /* Highlight on focus */
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
  }

  .badge-new {
    background: #e5e7eb; /* Badge background */
    padding: 6px 12px;
    border-radius: 16px; /* Pill shape */
    font-size: 13px;
    color: #4b5563; /* Badge text color */
    font-weight: 500;
  }

  /* Container for the scrollable pipeline */
  .cnn-visualization-pipeline-container {
    overflow-x: auto; /* Enable horizontal scrolling */
    padding: 10px 0;
    background-color: #ffffff; /* White background for the scrolling area */
    border-radius: 6px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05); /* Subtle shadow */
  }

  /* The pipeline itself (flex container) */
  .cnn-visualization-pipeline {
    display: flex;
    align-items: stretch; /* Make stages of same height if possible */
    gap: 5px;
    min-width: fit-content; /* Ensure flex container is wide enough for all stages */
    padding: 10px; /* Padding inside the scrollable area */
  }

  /* Individual stage in the pipeline (input, layer, output) */
  .pipeline-stage {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 15px;
    min-width: 220px; /* Minimum width for a stage */
    max-width: 380px; /* Maximum width */
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    display: flex;
    flex-direction: column; /* Stack content vertically within a stage */
    gap: 12px; /* Space between elements inside a stage */
  }
  .pipeline-stage.error-stage {
    /* Style for layers that encountered an error */
    border-color: #f87171;
    background-color: #fef2f2; /* Light red background */
  }
  .error-message {
    color: #ef4444; /* Red text for errors */
    font-weight: 500;
    font-size: 13px;
  }

  /* Headers for stages (Input, Output) and layers */
  .pipeline-stage h3,
  .layer-header {
    margin: 0 0 5px 0;
    color: #1f2937;
    font-size: 16px;
    font-weight: 600;
    padding-bottom: 5px;
    border-bottom: 1px solid #f3f4f6; /* Separator line */
  }
  .layer-header {
    /* Specific styling for layer headers */
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .layer-header .layer-name-new {
    /* Layer name might be long */
    font-size: 15px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex-grow: 1; /* Allow name to take available space */
    margin-right: 8px;
  }
  .layer-type-badge {
    /* Small badge for layer type (Conv2D, Dense, etc.) */
    background-color: #dbeafe; /* Light blue */
    color: #3b82f6; /* Blue text */
    font-size: 11px;
    padding: 3px 8px;
    border-radius: 10px;
    font-weight: 500;
    white-space: nowrap;
  }

  /* Container for the input image */
  .input-image-container {
    display: flex;
    justify-content: center;
    align-items: center;
    background: #f3f4f6;
    border-radius: 4px;
    padding: 10px;
    min-height: 130px; /* Fixed height for consistency */
  }
  .input-image-container canvas {
    /* Style the canvas within */
    border: 1px solid #d1d5db;
    background-color: #fff; /* White background for the canvas itself if transparent parts */
  }

  /* Meta information for layers (output shape, params) */
  .layer-meta {
    font-size: 12px;
    color: #6b7280; /* Gray text */
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .layer-meta span {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Grid for displaying multiple activation maps */
  .activation-maps-grid-new {
    display: grid;
    /* Auto-fill columns, each map item at least 52px wide */
    grid-template-columns: repeat(auto-fill, minmax(52px, 1fr));
    gap: 8px;
    margin-top: 10px;
  }

  .activation-map-item {
    /* Container for one activation map + its label */
    display: flex;
    flex-direction: column;
    align-items: center;
    background: #f3f4f6; /* Light background for the map item */
    border-radius: 4px;
    padding: 5px;
  }
  .activation-map-item canvas {
    border: 1px solid #e5e7eb;
    background-color: #fff; /* Ensure canvas background is white if activations are sparse */
  }
  .map-channel-label {
    /* Label for the channel (e.g., "Ch 0") */
    font-size: 10px;
    color: #4b5563;
    margin-top: 4px;
  }

  /* Styling for Dense layer activation display */
  .dense-activations-container {
    font-size: 13px;
  }
  .dense-info {
    margin-bottom: 8px;
    font-weight: 500;
    color: #374151;
  }
  .dense-values {
    /* Container for neuron values */
    display: flex;
    flex-wrap: wrap; /* Allow values to wrap to next line */
    gap: 5px;
  }
  .dense-value {
    /* Individual neuron value badge */
    background-color: #e0e7ff; /* Light purple/blue */
    color: #4338ca; /* Purple/blue text */
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 11px;
    font-family: "Consolas", "Menlo", monospace;
  }

  /* Styling for Flatten layer information */
  .flatten-layer-info {
    font-size: 13px;
    color: #4b5563;
    background-color: #f0f9ff; /* Very light blue */
    padding: 10px;
    border-radius: 4px;
    text-align: center;
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

  /* Connectors between pipeline stages (the SVG arrows) */
  .pipeline-connector {
    display: flex;
    align-items: center;
    justify-content: center;
    align-self: stretch; /* Make connector take full height of the flex row */
    padding: 0 5px;
    min-width: 40px;
  }
  .pipeline-connector svg line,
  .pipeline-connector svg polyline {
    stroke: #9ca3af; /* Connector line color */
  }

  /* Output stage specific styling */
  .output-stage {
    min-width: 280px; /* Slightly wider for the prediction chart */
  }
  .prediction-badge-new {
    /* Badge for the predicted class */
    background: #cffafe; /* Light cyan */
    color: #0e7490; /* Dark cyan text */
    padding: 10px 15px;
    border-radius: 6px;
    font-size: 14px;
    text-align: center;
    font-weight: 500;
  }
  .output-chart-container {
    /* Container for the PredictionChart component */
    margin-top: 10px;
    width: 100%;
    min-height: 150px; /* Ensure some height for the chart */
    display: flex; /* Helps in centering/sizing the chart if PredictionChart is a block */
    align-items: center;
    justify-content: center;
  }
</style>
