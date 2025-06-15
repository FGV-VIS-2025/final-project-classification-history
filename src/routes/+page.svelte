<script>
  import { onMount } from "svelte";
  import { loadData } from "$lib/data/loadData.js";
  import Scrolly from "svelte-scrolly";
  import { base } from "$app/paths";

  // Slides
  import Mnist from "$lib/Mnist.svelte";
  import History from "$lib/History.svelte";
  import CNNExplorer from "$lib/CNNExplorer.svelte";

  // Charts
  import AIModels from "$lib/charts/AIModels.svelte";
  import ScatterPlot from "$lib/charts/ScatterPlot.svelte";

  // Components
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

  // ====== Timeline Legend Variables ======
  let legendCategories = [];
  let legendColorScale;

  function handleLegend(event) {
    legendCategories = event.detail.categories;
    legendColorScale = event.detail.colorScale;
  }

  // ====== Extraordinary Cover Page Animation ======
  onMount(() => {
    const canvas = document.getElementById("constellation-canvas");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    let particles = [];
    let mouse = { x: null, y: null, radius: 150 };

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resizeCanvas();
    window.addEventListener("resize", resizeCanvas);

    window.addEventListener("mousemove", (event) => {
        mouse.x = event.x;
        mouse.y = event.y;
    });
    window.addEventListener("mouseout", () => {
        mouse.x = null;
        mouse.y = null;
    });

    class Particle {
        constructor(x, y, directionX, directionY, size, color) {
            this.x = x;
            this.y = y;
            this.directionX = directionX;
            this.directionY = directionY;
            this.size = size;
            this.color = color;
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
            ctx.fillStyle = this.color;
            ctx.fill();
        }
        update() {
            if (this.x > canvas.width || this.x < 0) this.directionX = -this.directionX;
            if (this.y > canvas.height || this.y < 0) this.directionY = -this.directionY;
            this.x += this.directionX;
            this.y += this.directionY;
            this.draw();
        }
    }

    function init() {
        particles = [];
        let numberOfParticles = (canvas.height * canvas.width) / 9000;
        for (let i = 0; i < numberOfParticles; i++) {
            let size = Math.random() * 2 + 1;
            let x = Math.random() * (innerWidth - size * 2 - size * 2) + size * 2;
            let y = Math.random() * (innerHeight - size * 2 - size * 2) + size * 2;
            let directionX = Math.random() * 0.4 - 0.2;
            let directionY = Math.random() * 0.4 - 0.2;
            let color = "rgba(0, 170, 255, 0.8)";
            particles.push(new Particle(x, y, directionX, directionY, size, color));
        }
    }

    function connect() {
        let opacityValue = 1;
        for (let a = 0; a < particles.length; a++) {
            for (let b = a; b < particles.length; b++) {
                let distance = ((particles[a].x - particles[b].x) ** 2) + ((particles[a].y - particles[b].y) ** 2);
                if (distance < (canvas.width / 7) * (canvas.height / 7)) {
                    opacityValue = 1 - (distance / 20000);
                    ctx.strokeStyle = `rgba(0, 255, 204, ${opacityValue})`;
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.moveTo(particles[a].x, particles[b].y);
                    ctx.lineTo(particles[b].x, particles[a].y);
                    ctx.stroke();
                }
            }
        }
        // Connect to mouse
        if (mouse.x !== null && mouse.y !== null) {
            for(let i = 0; i < particles.length; i++){
                let distance = ((particles[i].x - mouse.x) ** 2) + ((particles[i].y - mouse.y) ** 2);
                if(distance < mouse.radius * mouse.radius){
                    opacityValue = 1 - (distance / (mouse.radius*mouse.radius));
                    ctx.strokeStyle = `rgba(0, 170, 255, ${opacityValue * 0.8})`;
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(mouse.x, mouse.y);
                    ctx.lineTo(particles[i].x, particles[i].y);
                    ctx.stroke();
                }
            }
        }
    }

    function animate() {
        requestAnimationFrame(animate);
        ctx.clearRect(0, 0, innerWidth, innerHeight);
        for (let i = 0; i < particles.length; i++) {
            particles[i].update();
        }
        connect();
    }

    init();
    animate();

    return () => {
      window.removeEventListener("resize", resizeCanvas);
    };
  });
</script>

<Section>
  <Slide id="cover-page">
    <canvas id="constellation-canvas"></canvas>
    <div class="cover-content">
      <h1 class="cover-title">Classification History</h1>
      <p class="cover-subtitle">From logic to convolution networks and beyond</p>
    </div>
    <div class="scroll-indicator">
      <span>Scroll to Begin</span>
      <div class="celestial-cascade">
        <div class="chevron"></div>
        <div class="chevron"></div>
        <div class="chevron"></div>
      </div>
    </div>
  </Slide>

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
        hyperplane) that separates the data into different classes. The idea is that
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
        This project was developed by: 
        <a href="https://github.com/wobetec" target="_blank">Esdras Cavalcanti</a>,
        <a href="https://github.com/Vilasz" target="_blank">João Felipe</a> &
        <a href="https://github.com/MasFz" target="_blank">Marcelo Angelo</a>.
      </p>
      <p>
        Check the source code on <a href="https://github.com/FGV-VIS-2025/final-project-classification-history">GitHub</a>.
      </p>
      <p>
        References:
          <a href="https://epoch.ai/data/notable-ai-models">Notable Models</a>,
          <a href="https://poloclub.github.io/cnn-explainer">CNN Explaner - Polo Club</a>
      </p>
    </div>
    <div class="picture conclusion">
      <a href="/" class="media-link">
        <div class="media-container">
          <h2>Report</h2>
          <img src={`${base}/images/report.png`} alt="report" class="a4">
        </div>
      </a>
      <a href="/" class="media-link">
        <div class="media-container">
          <h2>Poster</h2>
          <img src={`${base}/images/poster.png`} alt="poster" class="a4">
        </div>
      </a>
      <a href="/" class="media-link teaser-link">
        <div class="media-container">
          <h2>Teaser</h2>
          <iframe
            title="Teaser Video"
            src="https://drive.google.com/file/d/13omNpGAdnBc2P0SK9eytZbT_eGwVbN2J/preview"
            allow="autoplay"
          ></iframe>
        </div>
      </a>
       <a href="/" class="media-link presentation-link">
        <div class="media-container">
          <h2>Presentation</h2>
          <iframe
            title="Presentation Video"
            src="https://drive.google.com/file/d/13omNpGAdnBc2P0SK9eytZbT_eGwVbN2J/preview"
            allow="autoplay"
          ></iframe>
        </div>
      </a>
    </div>
  </Slide>
</Section>

<style>
  :root {
    --color-bg-dark: #121212;
    --color-bg-light: #1e1e1e;
    --color-primary: #00aaff;
    --color-accent: #00ffcc;
    --color-secondary-accent: #ff00ff; /* Added a magenta for the title gradient */
    --color-text: #e0e0e0;
    --color-text-dark: #333333;
    --font-family-main: "Roboto", sans-serif;
    --font-family-headings: "Montserrat", sans-serif;
  }

  /* === STYLES FOR SCROLLY (LIGHT THEME) === */
  h1 {
    font-family: var(--font-family-headings);
    font-size: 3rem;
    color: var(--color-text-dark);
    margin-bottom: 1.5rem;
  }

  p {
    font-family: var(--font-family-main);
    font-size: 1.1rem;
    line-height: 1.6;
    text-indent: 1.5rem;
    text-align: justify;
    margin-bottom: 1rem;
    color: var(--color-text-dark);
  }

  span.highlight {
    background-color: rgba(0, 170, 255, 0.15);
    color: #005bb5;
    padding: 0.2rem 0.5rem;
    border-radius: 5px;
    font-weight: bold;
  }

  /* === STYLES FOR DARK THEME SLIDES === */
  .text {
    width: 40%;
    padding: 2rem;
    background: linear-gradient(145deg, var(--color-bg-light), var(--color-bg-dark));
    border-radius: 15px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
  }

  .text h1 {
    color: var(--color-primary);
    text-shadow: 0 0 10px var(--color-primary);
  }

  .text p {
    color: var(--color-text);
  }
  
  .text a {
    color: var(--color-accent);
    text-decoration: none;
    transition: text-shadow 0.3s;
  }
  
  .text a:hover {
	text-shadow: 0 0 8px var(--color-accent);
  }

  .text span.highlight {
    background-color: rgba(0, 170, 255, 0.2);
    color: var(--color-accent);
  }
  
  .picture {
    width: 60%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
  }
  
  .legend-in-text {
    margin-top: 1.5rem;
    padding: 1rem;
    background: var(--color-bg-dark);
    border: 1px solid var(--color-primary);
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(0, 170, 255, 0.2);
  }

  .legend-item {
    display: flex;
    align-items: center;
    font-size: 1rem;
    margin-bottom: 0.5rem;
  }
  
  .legend-item span {
	  color: var(--color-text);
  }

  .legend-color {
    width: 15px;
    height: 15px;
    margin-right: 10px;
    border: 1px solid var(--color-accent);
    border-radius: 3px;
  }

  p.break-line {
    text-align: center;
    font-size: 2rem;
    color: var(--color-primary);
    margin: 2rem 0;
  }
  
  /* === UPGRADED EXTRAORDINARY COVER PAGE === */
  #constellation-canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
  }
  
  .cover-content {
  /* place dead-centre on the slide */
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;

  /* ► veil gone  */
  background: transparent;
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
  border: none;
  padding: 0;
}

/* === HERO TITLE (update) === */
.cover-title {
  font-size: 6rem;          /* a bit larger */
  font-weight: 800;
  margin: 0;
  text-align: center;

  /* animated “data-stream” gradient in deep-blue tones */
  background: linear-gradient(
      90deg,
      #002bff 0%,
      #0080ff 25%,
      #00e0ff 50%,
      #0080ff 75%,
      #002bff 100%
  );
  background-size: 400% 100%;
  color: transparent;
  -webkit-background-clip: text;
          background-clip: text;
  animation: ml-stream 8s linear infinite;

  text-shadow: 0 0 18px rgba(0, 64, 255, 0.7);
}

  /* keyframes for the new effect */
  @keyframes ml-stream {
    0%   { background-position:   0% 0; }
    100% { background-position: -400% 0; }
  }

  
  /* @keyframes text-gradient-flow {
      to {
          background-position: -200% center;
      }
  } */
  
  .cover-subtitle {
    font-size: 1.5rem;
    color: var(--color-bg-dark);
    text-indent: 0;
    text-align: center;
    max-width: 600px;
    opacity: 0.8;
  }
  
  .scroll-indicator {
    position: absolute;
    bottom: 2rem;
    left: 50%; /* Center horizontally */
    transform: translateX(-50%); /* Fine-tune horizontal centering */
    color: var(--color-text);
    font-size: 1rem;
    z-index: 3;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }

  /* NEW "CELESTIAL CASCADE" BUTTON */
  .celestial-cascade {
    position: relative;
    width: 24px;
    height: 40px; /* Increased height for more room */
  }

  .chevron {
    position: absolute;
    width: 24px;
    height: 24px;
    opacity: 0;
    transform: scale(0.3) rotate(45deg);
    animation: cascade-scroll 3s infinite;
    box-shadow: 0 0 10px var(--color-accent), 0 0 20px var(--color-accent);
  }
  .chevron:before,
  .chevron:after {
    content: '';
    position: absolute;
    width: 100%;
    height: 4px;
    background-color: var(--color-accent);
    border-radius: 2px;
  }
  .chevron:before {
    top: 0;
    left: -50%;
  }
  .chevron:after {
    top: 50%;
    left: 0;
    transform: rotate(90deg);
    transform-origin: top left;
  }

  /* Staggered animation delays for the cascade effect */
  .chevron:nth-child(1) {
    animation-delay: 0s;
  }
  .chevron:nth-child(2) {
    animation-delay: 0.5s;
  }
  .chevron:nth-child(3) {
    animation-delay: 1s;
  }

  @keyframes cascade-scroll {
    0% {
      transform: translateY(-10px) scale(0.5) rotate(45deg);
      opacity: 0;
    }
    50% {
      opacity: 1;
    }
    100% {
      transform: translateY(20px) scale(1.2) rotate(45deg);
      opacity: 0;
    }
  }


  /* === FIXED CONCLUSION SLIDE === */
  .conclusion {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    width: 100%;
    height: 100%;
    align-items: stretch;
  }
  
  .media-link {
	  text-decoration: none;
    display: flex;
  }

  .media-container {
    padding: 1rem 1.5rem;
    border-radius: 15px;
    background: rgba(44, 44, 44, 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0, 170, 255, 0.3);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
  }

  .media-link:hover .media-container {
    transform: translateY(-10px);
    box-shadow: 0 0 25px rgba(0, 170, 255, 0.5);
    background: rgba(44, 44, 44, 0.9);
  }

  .conclusion h2 {
    font-family: var(--font-family-headings);
    font-size: 1.5rem;
    color: var(--color-accent);
    text-align: center;
    margin: 0;
    padding-bottom: 1rem;
  }

  .a4 {
    width: 100%;
    max-width: 180px;
    aspect-ratio: 210 / 297;
    border-radius: 5px;
    margin: auto 0;
  }
  
  .conclusion iframe {
	  width: 100%;
    aspect-ratio: 16 / 9;
	  border: none;
	  border-radius: 10px;
    margin: auto 0;
  }
</style>