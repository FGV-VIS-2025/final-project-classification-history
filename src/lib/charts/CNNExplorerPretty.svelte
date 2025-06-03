    <script>
        import { onMount, onDestroy } from 'svelte';
        import * as tf from '@tensorflow/tfjs';
        import ImagesCanvas from '$lib/components/ImagesCanvas.svelte';
        import LayerVisualization from '$lib/components/LayerVisualization.svelte';
        import PredictionChart from '$lib/components/PredictionChart.svelte';
        import { loadModel, loadResume, pngToTensor } from '$lib/data/loadMnistAssets.js';

        let model = null;
        let imagesMeta = [];
        let currentIdx = 0;
        let inputTensor = null;
        let inputPixels = null;
        let layerNames = [];
        let layerIx = 0;
        let channelIx = 0;
        let actPixels = null;
        let probs = null;
        let predicted = null;
        let layerInfo = null;

        const tensorToArray = (t) => Array.from(t.dataSync());

        async function runInference() {
            if (!model || !inputTensor) return;

            if (layerNames.length === 0) {
                layerNames = model.layers.map(l => l.name);
                layerInfo = model.layers.map(l => ({
                    name: l.name,
                    type: l.getClassName(),
                    outputShape: l.outputShape,
                    params: l.countParams()
                }));
            }

            tf.tidy(() => {
                let out = inputTensor;
                let act = null;

                model.layers.forEach((layer, idx) => {
                    out = layer.apply(out);
                    if (idx === layerIx) act = out.clone();
                });

                const logits = out.flatten();
                const soft = tf.softmax(logits);

                probs = tensorToArray(soft);
                predicted = probs.indexOf(Math.max(...probs));

                soft.dispose();
                logits.dispose();

                if (act) {
                    const [, h, w, c] = act.shape;
                    channelIx = Math.min(channelIx, c - 1);

                    const single = act.slice([0, 0, 0, channelIx], [1, h, w, 1]).squeeze();
                    const resized = tf.image.resizeNearestNeighbor(single.expandDims(-1), [28, 28]);

                    actPixels = tensorToArray(resized);

                    single.dispose();
                    resized.dispose();
                    act.dispose();
                }
            });
        }

        async function pick(idx) {
            currentIdx = idx;
            const meta = imagesMeta[idx];
            if (!meta) return;

            if (inputTensor) inputTensor.dispose();
            inputTensor = await pngToTensor('/' + meta.filepath.replace(/\\/g, '/'));
            inputPixels = tensorToArray(inputTensor);

            await runInference();
        }

        onMount(async () => {
            const [m, resume] = await Promise.all([loadModel(), loadResume()]);
            model = m;
            imagesMeta = resume;
            await pick(0);
        });

        onDestroy(() => {
            if (inputTensor) inputTensor.dispose();
            if (model) model.dispose();
        });
    </script>

    <div class="cnn-explorer">
        <div class="header">
            <h2>CNN Layer Explorer</h2>
            <div class="model-info">
                <span class="badge">Model: MNIST CNN</span>
                <span class="badge">Layers: {layerNames.length}</span>
            </div>
        </div>

        <div class="main-content">
            <!-- Input Section -->
            <div class="section input-section">
                <div class="section-header">
                    <h3>Input Image</h3>
                    <div class="controls">
                        <select bind:value={currentIdx} on:change={(e) => pick(+e.target.value)}>
                            {#each imagesMeta as img, i}
                                <option value={i}>#{i} → {img.label}</option>
                            {/each}
                        </select>
                    </div>
                </div>
                <div class="visualization-container">
                    <ImagesCanvas imageData={inputPixels}/>
                </div>
            </div>

            <!-- Layer Visualization Section -->
            <div class="section layer-section">
                <div class="section-header">
                    <h3>Layer Visualization</h3>
                    <div class="layer-info">
                        {#if layerInfo && layerInfo[layerIx]}
                            <div class="info-card">
                                <div class="info-item">
                                    <span class="label">Type:</span>
                                    <span class="value">{layerInfo[layerIx].type}</span>
                                </div>
                                <div class="info-item">
                                    <span class="label">Output Shape:</span>
                                    <span class="value">{layerInfo[layerIx].outputShape.join(' × ')}</span>
                                </div>
                                <div class="info-item">
                                    <span class="label">Parameters:</span>
                                    <span class="value">{layerInfo[layerIx].params.toLocaleString()}</span>
                                </div>
                            </div>
                        {/if}
                    </div>
                </div>
                <div class="visualization-container">
                    <LayerVisualization imageData={actPixels}/>
                </div>
                <div class="layer-controls">
                    <div class="slider-container">
                        <input type="range"
                            min="0"
                            max={layerNames.length - 1}
                            bind:value={layerIx}
                            on:input={runInference}/>
                        <span class="layer-name">{layerNames[layerIx] || '–'}</span>
                    </div>
                    <div class="channel-control">
                        <label>
                            Channel:
                            <input type="number"
                                min="0"
                                step="1"
                                bind:value={channelIx}
                                on:input={runInference}/>
                        </label>
                    </div>
                </div>
            </div>

            <!-- Output Section -->
            <div class="section output-section">
                <div class="section-header">
                    <h3>Network Output</h3>
                    {#if predicted !== null}
                        <div class="prediction-badge">
                            Predicted: <strong>{predicted}</strong>
                        </div>
                    {/if}
                </div>
                <div class="visualization-container">
                    <PredictionChart probabilities={probs} predictedClass={predicted}/>
                </div>
            </div>
        </div>
    </div>

    <style>
        .cnn-explorer {
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 24px;
            font-family: system-ui, -apple-system, sans-serif;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 2px solid #f0f0f0;
        }

        .header h2 {
            margin: 0;
            color: #2d3748;
            font-size: 24px;
        }

        .model-info {
            display: flex;
            gap: 12px;
        }

        .badge {
            background: #e2e8f0;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 14px;
            color: #4a5568;
        }

        .main-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
        }

        .section {
            background: #f8fafc;
            border-radius: 8px;
            padding: 16px;
        }

        .section-header {
            margin-bottom: 16px;
        }

        .section-header h3 {
            margin: 0 0 12px 0;
            color: #2d3748;
            font-size: 18px;
        }

        .visualization-container {
            background: white;
            border-radius: 6px;
            padding: 12px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        .layer-controls {
            margin-top: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .slider-container {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .layer-name {
            font-size: 14px;
            color: #4a5568;
            min-width: 100px;
        }

        .info-card {
            background: white;
            border-radius: 6px;
            padding: 12px;
            margin-top: 8px;
        }

        .info-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 4px;
            font-size: 14px;
        }

        .info-item .label {
            color: #718096;
        }

        .info-item .value {
            color: #2d3748;
            font-weight: 500;
        }

        .prediction-badge {
            background: #ebf8ff;
            color: #2b6cb0;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 14px;
        }

        select {
            width: 100%;
            padding: 8px;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            background: white;
            color: #2d3748;
        }

        input[type="range"] {
            width: 100%;
        }

        input[type="number"] {
            width: 80px;
            padding: 4px 8px;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
        }

        .channel-control {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .channel-control label {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #4a5568;
            font-size: 14px;
        }
    </style>
    