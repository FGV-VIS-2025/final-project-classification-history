<!-- src/lib/components/LayerVisualization.svelte -->
<script>
  import { onMount } from 'svelte';

  export let imageData = null;   // 1-D array (length 784) or null
  export let width  = 56;
  export let height = 56;

  let canvasEl;

  function draw () {
      if (!canvasEl || !imageData || imageData.length !== 784) return;

      const ctx   = canvasEl.getContext('2d');
      const side  = 28;
      const dx    = width  / side;
      const dy    = height / side;

      ctx.clearRect(0, 0, width, height);
      ctx.fillStyle = 'black';
      ctx.fillRect(0, 0, width, height);

      for (let i = 0; i < side; i++) {
          for (let j = 0; j < side; j++) {
              const v = imageData[i * side + j]; // 0-1
              const g = Math.floor(v * 255);
              ctx.fillStyle = `rgb(${g},${g},${g})`;
              ctx.fillRect(j * dx, i * dy, dx, dy);
          }
      }
  }

  onMount(draw);
  $: draw();        // run again whenever imageData changes
</script>

<canvas bind:this={canvasEl} {width} {height}
      style="border:1px solid #ccc; image-rendering:pixelated;" />
