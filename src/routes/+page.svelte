<script>
    import { loadData } from "$lib/data/loadData.js";
    import Section from "$lib/layout/Section.svelte";
    import Step from "$lib/scrolly/Step.svelte";
    import { onMount } from "svelte";
    import Scrolly from "svelte-scrolly";
    import ScatterPlot from "../lib/charts/ScatterPlot.svelte";
    import Drawer from "$lib/Drawer.svelte";

    let data = null;
    onMount(async () => {
        data = await loadData();
        });

	let progress = null;
    let stepFixe = 20;
    let coordenatesSufixes = [
        {"sufix": "random"},
        {"sufix": "line"},
        {"sufix": "xor"},
    ];

    let pixelMatrix;
    $: console.log("pixelMatrix", pixelMatrix);

</script>

<Section>
    <div class="progress">
        {progress}
    </div>
	<Scrolly bind:progress={progress}>
        <Step>
            <h1>What is classification?</h1>
            <p>Classification is nothing more than giving a set of labels (or classes) and a set of data, assigning a label (or more than one depending on the case) to each piece of data. In a more direct way, classification is the process of identifying which category a new piece of data belongs to, based on a set of already labeled data.</p>
            <p>Humans have always needed to classify objects. Whether it's to identify whether a food is poisonous or not, or to distinguish between a dangerous place or not. Going a little beyond this conscious classification, humans have learned to classify everything unconsciously, whether it's the face of a person they know, differentiating a fork from a knife, or recognizing digits written on a check.</p>
            <p>With the emergence of computers to assist in calculations and other complex tasks, the question arose: "Why not teach the computer to classify objects too?".</p>
            <p>Today, it is possible to use algorithms to read text, identify objects in an image, recognize a person's voice, etc. But how did all this come about? What is the history behind classification?</p>
        </Step>
        <Step>
            <h1>Linear classification</h1>
            <p>In the 1950s, psychologist Frank Rosenblatt created the Perceptron, a mathematical model inspired by the workings of the human brain. The Perceptron is a linear classifier that tries to find a line (or hyperplane) that separates data into different classes. The idea is that by adjusting the weights of the inputs, the Perceptron can learn to correctly classify the data.</p>
            <p>Thinking mathematically, the perceptron finds one of the lines that separates the data. This line is called a hyperplane, and the goal of the perceptron is to find the hyperplane that best separates the data into different classes. The perceptron tries to minimize the distance between the data points and the hyperplane by adjusting the weights of the inputs.</p>
        </Step>
        <Step>
            <h1>The XOR problem</h1>
            <p>In 1969 , Marvin Minsky and Seymour Papert published a book called "Perceptrons" in which they showed that the Perceptron could not solve the XOR problem. The XOR problem is a simple problem in which the input consists of two binary values (0 or 1) and the output is 1 if the inputs are different and 0 if they are the same. The problem is that there is no linear hyperplane that can separate the data points in this case.</p>
            <p>The XOR problem is a classic example of a problem that cannot be solved by a linear classifier. The Perceptron can only learn to separate linearly separable data, which means that it can only find a hyperplane that separates the data points into different classes if the data points are linearly separable. In the case of the XOR problem, there is no linear hyperplane that can separate the data points into different classes, so the Perceptron cannot solve the problem.</p>
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
    <div class="slide">
        <Drawer bind:pixelMatrix/>
    </div>
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

    .slide {
        width: 100%;
        height: 100vh;
    }
</style>