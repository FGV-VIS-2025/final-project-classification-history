<script>
  import { onMount } from "svelte";
  import { loadData } from "$lib/data/loadData.js";
  import Scrolly from "svelte-scrolly";

  // Slides
  import Mnist from "$lib/Mnist.svelte";
  import History from "$lib/History.svelte";
  import CNNExplorer from "$lib/CNNExplorer.svelte";
  
  // Charts
  import AIModels from "$lib/charts/AIModels.svelte";
  import ScatterPlot from "$lib/charts/ScatterPlot.svelte";

  // Componetns
  import Section from "$lib/components/layout/Section.svelte";
  import Slide from "$lib/components/layout/Slide.svelte";
  import Step from "$lib/components/scrolly/Step.svelte";

  let data = null;
  onMount(async () => {
    data = await loadData();
  });

  let progress = null;
  let stepFixe = 20;
  let coordenatesSufixes = [
    { sufix: "random" },
    { sufix: "line" },
    { sufix: "xor" },
  ];


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
  <!-- Scrolly -->
  <Scrolly bind:progress>
    <Step>
      <h1>What is classification?</h1>
      <p>
        Classification is nothing more than giving a set of labels (or classes) and a set of data, assigning a label
        (or more than one depending on the case) to each piece of data. In a more direct way,
        <span class="highlight">
          classification is the process of identifying which category a new piece of data belongs
        </span>
        to, based on a set of already labeled data.
      </p>
      <p>
        Humans have always needed to classify objects. Whether it's to identify
        whether a food is poisonous or not, or to distinguish between a
        dangerous place or not. Going a little beyond this conscious
        classification, humans have learned to classify everything
        unconsciously, whether it's the face of a person they know,
        differentiating a fork from a knife, ou recognizes digits written on a
        check.
      </p>
      <p>
        With the emergence of computers to assist in calculations and other
        complex tasks, the question arose: "Why not teach the computer to
        classify objects too?".
      </p>
      <p>
        Today, it is possível usar algoritmos to read text, identify objects in
        an image, recognize a person's voice, etc. But how did all this come
        about? What is the history behind classification?
      </p>
    </Step>
    <Step>
      <h1>Linear classification</h1>
      <p>
        In the 1950s, psychologist Frank Rosenblatt created the Perceptron, a
        mathematical model inspired by the workings of the human brain. The
        Perceptron is a linear classifier that tries to find a line (or
        hyperplane) that separates data into different classes. The idea is that
        by adjusting the weights of the inputs, the Perceptron can learn to
        correctly classify the data.
      </p>
      <p>
        Thinking mathematically, the perceptron finds one of the lines that
        separates the data. This line is called a hyperplane, and the goal of
        the perceptron is to find the hyperplane that best separates the data
        into different classes. The perceptron tries to minimize the distance
        between the data points and the hyperplane by adjusting the weights of
        the inputs.
      </p>
    </Step>
    <Step>
      <h1>The XOR problem</h1>
      <p>
        In 1969, Marvin Minsky and Seymour Papert published a book called
        "Perceptrons" in which they showed that the Perceptron could not solve
        the XOR problem. The XOR problem is a simple problem in which the input
        consists of two binary values (0 or 1) and the output is 1 if the inputs
        are different and 0 if they are the same. The problem is that there is
        no linear hyperplane that can separate the data points in this case.
      </p>
      <p>
        The XOR problem is a classic exemplo of a problema that cannot be solved
        by a linear classifier. The Perceptron can only learn to separate
        linearly separable data, which means that it can only find a hyperplane
        that separates the data points into different classes if the data points
        are linearly separable. In the case of the XOR problem, there is no
        linear hyperplane that can separate the data points into different
        classes, so the Perceptron cannot solve the problema.
      </p>
      <p>
        In the graph on the side, for example, it is <span class="highlight">impossible</span> to have a single
        line separating the blue dots from the red dots. You can try.
      </p>
    </Step>
    <svelte:fragment slot="viz">
      <ScatterPlot {data} {coordenatesSufixes} {stepFixe} {progress} />
    </svelte:fragment>
  </Scrolly>

  <!-- MNIST -->
  <Slide>
    <div class="text">
      <h1>MNIST</h1>
      <p>
        Now, let's jump into the world of machine learning for image classification. One of the most famous datasets
        used for training and testing image classification algorithms is the MNIST dataset. It has been a benchmark
        for evaluating the performance of various machine learning models, especially in the field of computer vision.
      </p>
      <p>
        The MNIST dataset is a collection of handwritten digits that is widely
        used in the field of machine learning. It contains 60,000 training
        images and 10,000 test images, each of which is a grayscale image of a
        handwritten digit (0-9) with a size of 28x28 pixels. The dataset was
        created by Yann LeCun and his colleagues in 1998 and has since become a
        benchmark for evaluating the performance of machine learning algorithms.
      </p>
    </div>
    <div class="picture">
      <Mnist />
    </div>
  </Slide>

  <!-- Trained CNN -->
  <Slide>
    <div class="text">
      <h1>CNN</h1>
      <p>
        After Multilayer Perceptrons (MLPs) successfully tackled the XOR problem, it marked a pivotal moment
        in the history of neural networks, proving their capability to learn non-linear decision boundaries.
        This breakthrough naturally led researchers to apply these models to more complex challenges like MNIST.
      </p>
      <p>
        However, MLPs have limitations with images. They flatten images into long vectors, ignoring the important
        spatial relationships between pixels. This leads to too many parameters, making the networks slow and likely
        to overfit. A new approach was needed—one that could recognize local patterns in images, like the strokes
        and curves of a digit.
      </p>
      <p>
        This necessity paved the way for the development of Convolutional Neural Networks (CNNs), a revolutionary
        architecture inspired by the human visual cortex. Unlike MLPs, CNNs utilize convolutional layers to
        <span class="highlight">automatically and adaptively learn spatial hierarchies of features</span>,
        from simple edges and corners to more
        complex motifs. By incorporating concepts like parameter sharing and pooling layers, CNNs could efficiently
        process raw pixel data, capture the spatial dependencies, and achieve a high degree of invariance to
        transformations like translation and scaling.
      </p>
      <p>
        Here you can play with the VGGNet architecture and draw a digit to see how the CNN classifies it and what is inside the CNN.
      </p>
    </div>
    <div class="picture">
      <CNNExplorer />
    </div>
  </Slide>

  <!-- History (onde colocamos a legenda à esquerda) -->
  <Slide>
    <div class="text">
      <h1>Other Models</h1>
      <p>
        While revolutionary, Convolutional Neural Networks (CNNs) were a critical milestone, not the final word in classification.
        Other powerful approaches also excelled, with Kernel methods like SVMs finding complex decision boundaries and Ensemble
        techniques like Random Forests offering exceptional robustness by combining simpler models.
      </p>
      <p>
        The evolution within deep learning didn't stop there, leading to even deeper and more powerful architectures.
        More recently, <span class="highlight">Transformers have caused a paradigm shift</span>.
        Originally designed for language, their attention-based
        architecture has been successfully adapted to computer vision, challenging the dominance of CNNs and representing
        the current cutting edge.
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

  <!-- AIModels AI Models -->
  <Slide>
    <div class="text">
      <h1>Models complexity</h1>
      <p>
        However "with great power comes great responsibility". In deep learning, this
        phrase can be translated to "With great models comes great computational
        effort". As models have become more complex, the computational effort
        required to train them has also increased significantly.
      </p>
      <p>
        This graph shows the evolution of the computational effort (in FLOPs)
        required to train models over time. The X-axis represents the year
        each model was published, and the Y-axis (log scale) displays the number
        of FLOPs.
      </p>
      <p>
        The shaded region marks the "Deep Learning Era" (from 2010 onwards),
        when there was a significant increase in the use of computing to train
        neural networks. When you hover over each point, a tooltip appears near
        the cursor showing the model name, year and number of FLOPs.
      </p>
      <p>
        As you can see, the computational effort required to train models has
        increased exponentially over the years, more than that it increase it's growth rate.
        This is due to the increasing complexity of models, the growing amount of data available for training, and the
        increasing availability of computational resources.
      </p>
      <p>
        The question that remains is: "How far can we go?" or "How far humans want to push the limits of
        computer models for classification?".
        At least for now, the answer is: "We don't know yet". We don't even know if we have reached the limit of what is possible with
        computer models for classification. But one thing is certain: the future of classification is very promising. 
      </p>
    </div>
    <div class="picture">
      <AIModels />
    </div>
  </Slide>

  <!-- Conclusion -->
  <Slide>
    <div class="text">
      <h1>Conclusion</h1>
      <p>
        As we have seen, humans have always needed to classify. With the advent of computers, classification has become
        a research and development objective. From the first models such as the Perceptron, through more complex models
        such as Convolutional Neural Networks (CNNs), to the most recent models with transformers, year after year the
        progress has become greater and faster.
      </p>
      <p>
        The next time you come across an object detection, speech recognition or any other classification system,
        remember that behind that system lies a rich and complex history of research and development.
      </p>
      <p class="break-line">...</p>
      <p>
        This project was developed as part of the Data Visualization course at Fundacão Getúlio Vargas (FGV) in 2025.1.
        It was developed by: 
        <a href="https://github.com/wobetec" target="_blank">Esdras Cavalcanti</a>,
        <a href="https://github.com/Vilasz" target="_blank">João Felipe</a> and
        <a href="https://github.com/MasFz" target="_blank">Marcelo Angelo</a>.
      </p>
      <p>
        You can check the source code on <a href="https://github.com/FGV-VIS-2025/final-project-classification-history">GitHub</a>.
        Next you can see the project Report, Poster, Presentation and Teaser Video.
      </p>
    </div>
    <div class="picture conclusion">
      <div class="row">
        <a href="/">
          <div class="media-container">
            <h2>Report</h2>
            <img class="a4" src="" alt="">
          </div>
        </a>
        <a href="/">
          <div class="media-container">
            <h2>Poster</h2>
            <img class="a4" src="" alt="">
          </div>
        </a>
      </div>
      <div class="row">
        <div class="media-container">
          <h2>Teaser</h2>
          <iframe
            title="Teaser Video"
            src="https://drive.google.com/file/d/13omNpGAdnBc2P0SK9eytZbT_eGwVbN2J/preview"
            width="480"
            height="270"
            allow="autoplay"
          ></iframe>
        </div>
        <div class="media-container">
          <h2>Presentation</h2>
          <iframe
            title="Presentation Video"
            src="https://drive.google.com/file/d/13omNpGAdnBc2P0SK9eytZbT_eGwVbN2J/preview"
            width="480"
            height="270"
            allow="autoplay"
          ></iframe>
        </div>
      </div>
    </div>
  </Slide>
</Section>

<style>
  /* Step */
  h1 {
    font-size: 40px;
    margin-bottom: 20px;
  }

  p {
    text-indent: 30px;
    text-align: justify;
    margin-bottom: 10px;
    font-size: 20px;
  }

  span.highlight {
    background-color: var(--color-highlight);
    padding: 0 5px;
    border-radius: 20px;
  }

  p.break-line {
    margin: 20px auto;
    text-indent: 0;
    text-align: center;
  }

  .text {
    width: 30%;
    padding: 30px;
  }

  .picture {
    width: 70%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  /* ===== Legend styles on the left side ===== */
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

  /* ===== Conclusion slide ===== */
  .conclusion {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 20px;
  }

  .conclusion a {
    text-decoration: none;
    transition: transform 0.2s ease-in-out;
  }

  .conclusion a:hover {
    transform: scale(1.05);
  }

  .row {
    display: flex;
    gap: 20px;
  }

  .media-container {
    padding: 10px;
    border-radius: 10px;
    background-color: var(--color-bg-lv2);
  }

  .a4 {
    width: 210px;
    height: 297px;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  h2 {
    font-size: 24px;
    margin-bottom: 10px;
    text-align: center;
    color: var(--color-font-dark-grain);
  }
  /* ============================================ */
</style>
