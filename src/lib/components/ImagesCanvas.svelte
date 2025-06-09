<script>
    import { onMount } from 'svelte';
  
    /** @type {number[] | null} */
    export let imageData = null; // Array 1D de 784 pixels (0-1 ou 0-255)
    /** @type {number} */
    export let width = 56; // Largura do canvas
    /** @type {number} */
    export let height = 56; // Altura do canvas
  
    /** @type {HTMLCanvasElement} */
    let canvasElement;
  
    function draw() {
      if (!canvasElement || !imageData || imageData.length / width / height !== 1) return;
  
      const ctx = canvasElement.getContext('2d');
      if (!ctx) return;
  
      const imageSide = 28;
  
      ctx.clearRect(0, 0, width, height);
      ctx.fillStyle = 'black';
      ctx.fillRect(0,0, width, height);
  
      for (let i = 0; i < height; i++) {
        for (let j = 0; j < width; j++) {
          const pixelValue = imageData[i * height + j];
          let grayscale;
          if (pixelValue <= 1) {
            grayscale = Math.floor(pixelValue * 255);
          } else {
            grayscale = Math.floor(pixelValue);
          }
          ctx.fillStyle = `rgb(${grayscale}, ${grayscale}, ${grayscale})`;
          ctx.fillRect(j, i, 1, 1);
        }
      }
    }
  
    onMount(() => {
      draw();
    });
  
    $: if (imageData && canvasElement) {
      draw();
    }
  </script>
  
  <canvas bind:this={canvasElement} {width} {height} style="border: 1px solid #ccc; image-rendering: pixelated;"></canvas>