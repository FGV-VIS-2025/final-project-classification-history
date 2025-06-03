<script>
    import MnistImages from "$lib/charts/MnistImages.svelte";
    import { loadData } from "$lib/data/loadData.js";
    import Drawer from "$lib/Drawer.svelte";
    import Section from "$lib/layout/Section.svelte";
    import Slide from "$lib/layout/Slide.svelte";
    import Step from "$lib/scrolly/Step.svelte";
    import { onMount } from "svelte";
    import Scrolly from "svelte-scrolly";
    import ScatterPlot from "$lib/charts/ScatterPlot.svelte";
    import History from "$lib/slides/History.svelte";
    import Notable from "$lib/slides/Notable.svelte";
    import CNNExplorer   from "$lib/charts/CNNExplorer.svelte";

    let data = null;
    onMount(async () => {
        data = await loadData();
    });

    let progress = null;
    let stepFixe = 20;
    let coordenatesSufixes = [
        { "sufix": "random" },
        { "sufix": "line" },
        { "sufix": "xor" },
    ];

    let pixelMatrix;

    // ====== Variáveis para empacotar a legenda do Timeline ======
    let legendCategories = [];
    let legendColorScale;

    function handleLegend(event) {
        legendCategories = event.detail.categories;
        legendColorScale = event.detail.colorScale;
    }
    // ==============================================================
</script>

<Section>
    <div class="progress">
        {progress}
    </div>

    <Scrolly bind:progress={progress}>
        <Step>
            <h1>What is classification?</h1>
            <p>Classification is nothing more than giving a set of labels (or classes) and a set of data, assigning a label (or more than one depending on the case) to each piece of data. In a more direct way, classification is the process of identifying which category a new piece of data belongs to, based on a set of already labeled data.</p>
            <p>Humans have always needed to classify objects. Whether it's to identify whether a food is poisonous or not, or to distinguish between a dangerous place or not. Going a little beyond this conscious classification, humans have learned to classify everything unconsciously, whether it's the face of a person they know, differentiating a fork from a knife, ou recognizes digits written on a check.</p>
            <p>With the emergence of computers to assist in calculations and other complex tasks, the question arose: "Why not teach the computer to classify objects too?".</p>
            <p>Today, it is possível usar algoritmos to read text, identify objects in an image, recognize a person's voice, etc. But how did all this come about? What is the history behind classification?</p>
        </Step>
        <Step>
            <h1>Linear classification</h1>
            <p>In the 1950s, psychologist Frank Rosenblatt created the Perceptron, a mathematical model inspired by the workings of the human brain. The Perceptron is a linear classifier that tries to find a line (or hyperplane) that separates data into different classes. The idea is that by adjusting the weights of the inputs, the Perceptron can learn to correctly classify the data.</p>
            <p>Thinking mathematically, the perceptron finds one of the lines that separates the data. This line is called a hyperplane, and the goal of the perceptron is to find the hyperplane that best separates the data into different classes. The perceptron tries to minimize the distance between the data points and the hyperplane by adjusting the weights of the inputs.</p>
        </Step>
        <Step>
            <h1>The XOR problem</h1>
            <p>In 1969, Marvin Minsky and Seymour Papert published a book called "Perceptrons" in which they showed that the Perceptron could not solve the XOR problem. The XOR problem is a simple problem in which the input consists of two binary values (0 or 1) and the output is 1 if the inputs are different and 0 if they are the same. The problem is that there is no linear hyperplane that can separate the data points in this case.</p>
            <p>The XOR problem is a classic exemplo of a problema that cannot be solved by a linear classifier. The Perceptron can only learn to separate linearly separable data, which means that it can only find a hyperplane that separates the data points into different classes if the data points are linearly separable. In the case of the XOR problem, there is no linear hyperplane that can separate the data points into different classes, so the Perceptron cannot solve the problema.</p>
            <p>In the graph on the side, for example, it is impossible to have a single line separating the blue dots from the red dots. You can try.</p>
        </Step>
        <svelte:fragment slot="viz">
            <ScatterPlot
                data={data}
                coordenatesSufixes={coordenatesSufixes}
                stepFixe={stepFixe}
                progress={progress}
            />
        </svelte:fragment>
    </Scrolly>

    <!-- MNIST -->
    <Slide>
        <div class="text">
            <h1>MNIST</h1>
            <p>
                The MNIST dataset is a collection of handwritten digits that is widely used in the field of machine learning. It contains 60,000 training images and 10,000 test images, each of which is a grayscale image of a handwritten digit (0-9) with a size of 28x28 pixels. The dataset was created by Yann LeCun and his colleagues in 1998 and has since become a benchmark for evaluating the performance of machine learning algorithms.
            </p>
        </div>
        <div class="picture">
            <MnistImages/>
        </div>
    </Slide>

    <!-- Trained CNN -->
    <Slide>
        <Drawer bind:pixelMatrix/>
        <CNNExplorer />   
    </Slide>

    <!-- History (onde colocamos a legenda à esquerda) -->
    <Slide>
        <div class="text">
            <h1>History</h1>
            <p>
                Lorem ipsum dolor sit amet, consectetur adipisicing elit. Impedit tempora rem necessitatibus deleniti quibusdam omnis, magni minima natus debitis consectetur voluptatum. Blanditiis, odio maxime laudantium in doloremque eius ipsa inventore?
            </p>

            {#if legendCategories.length}
                <div class="legend-in-text">
                    {#each legendCategories as cat}
                        <div class="legend-item">
                            <span
                                class="legend-color"
                                style="background-color: {legendColorScale(cat)}"
                            ></span>
                            <span>{cat}</span>
                        </div>
                    {/each}
                </div>
            {/if}
        </div>
        <div class="picture">
            <History on:readyLegend={handleLegend} />
        </div>
    </Slide>

    <!-- Notable AI Models -->
    <Slide>
        <div class="text">
            <h1>Notable AI Models</h1>
            <p>
                Este gráfico mostra a evolução do esforço computacional (em FLOPs) necessário para treinar modelos de IA ao longo do tempo. 
                O eixo X representa o ano de publicação de cada modelo e o eixo Y (escala logarítmica) exibe o número de FLOPs.
            </p>
            <p>
                A região sombreada marca a “Deep Learning Era” (a partir de 2010), quando houve um aumento expressivo no uso de computação para treinar redes neurais. 
                Ao passar o mouse sobre cada ponto, aparece um tooltip próximo ao cursor mostrando o nome do modelo, o ano e a quantidade de FLOPs.
            </p>
        </div>
        <div class="picture">
            <Notable/>
        </div>
    </Slide>
    
</Section>

<style>
    .progress {
        position: fixed;
        right: 0;
        top: 0;
    }

    /* Step */
    h1 {
        font-size: 40px;
        margin-bottom: 20px;
    }

    p {
        text-indent: 20px;
        text-align: justify;
        margin-bottom: 10px;
        font-size: 20px;
    }

    .text {
        width: 25%;
    }

    .picture {
        width: 75%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .cnn-wrapper {
        display: flex;
        flex: 1 1 100%;
        gap: 24px;            /* space between Drawer and CNNExplorer */
        align-items: flex-start;
        height: 100%;         /* keeps both widgets full-height inside Slide */
    }

    /* ===== Estilos da legenda no lado esquerdo ===== */
    .legend-in-text {
        margin-top: 1rem;
        padding: 0.5rem;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 4px;
        border: 1px solid #ddd;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .legend-item {
        display: flex;
        align-items: center;
        font-size: 0.9rem;
        margin-bottom: 6px;
    }
    .legend-item:last-child {
        margin-bottom: 0;
    }
    .legend-color {
        width: 12px;
        height: 12px;
        border: 1px solid #999;
        margin-right: 8px;
    }
    /* ============================================ */
</style>
