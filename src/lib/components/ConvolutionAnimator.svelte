<script>
    import { onMount, onDestroy } from 'svelte';
  
    export let inputMap = [];
    export let kernel = [];
    export let outputMap = [];
    export let inputShape = { w: 0, h: 0 };
    export let kernelShape = { w: 0, h: 0 };
  
    let canvas;
    let animFrame;
    let step = 0;
    let isAnimating = true;
  
    const PADDING = 40;
    const CELL_SIZE = 10;
    const KERNEL_WINDOW_COLOR = 'rgba(233, 69, 96, 0.9)'; // Accent color, more opaque
  
    // --- THIS IS THE KEY FIX FOR INTERACTIVITY ---
    // This reactive block watches for any change in the input props.
    // When you select a new kernel or input, it resets the animation.
    $: if (inputMap && kernel) {
      step = 0; // Reset the animation step
      isAnimating = true; // Ensure animation is running
      draw(); // Immediately draw the first frame with the new data
    }
  
    function draw() {
      if (!canvas || !inputMap.length) return;
      const ctx = canvas.getContext('2d');
      const outputW = inputShape.w - kernelShape.w + 1;
      const outputH = inputShape.h - kernelShape.h + 1;
      
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.font = 'bold 12px "Montserrat", sans-serif';
      ctx.fillStyle = '#e0e0e0';
      
      // Draw Input Map
      ctx.fillText('Input Channel', 0, -8);
      for (let y = 0; y < inputShape.h; y++) {
        for (let x = 0; x < inputShape.w; x++) {
          const val = inputMap[y * inputShape.w + x];
          ctx.fillStyle = `rgba(220, 220, 220, ${val * 0.7 + 0.05})`;
          ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
          ctx.strokeStyle = '#0f3460';
          ctx.strokeRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
        }
      }
      
      // Draw Output Map as it's being built
      const outputStartX = inputShape.w * CELL_SIZE + PADDING;
      ctx.fillStyle = '#e0e0e0';
      ctx.fillText('Output Channel', outputStartX, -8);
      for (let y = 0; y < outputH; y++) {
        for (let x = 0; x < outputW; x++) {
          const i = y * outputW + x;
          const val = i <= step ? outputMap[i] : 0;
          ctx.fillStyle = `rgba(233, 69, 96, ${val * 0.9})`;
          ctx.fillRect(outputStartX + x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
          ctx.strokeStyle = '#e94560';
          ctx.strokeRect(outputStartX + x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
        }
      }
  
      // Draw Sliding Kernel Window on Input
      if(step < outputW * outputH) {
        const currentY = Math.floor(step / outputW);
        const currentX = step % outputW;
        ctx.strokeStyle = KERNEL_WINDOW_COLOR;
        ctx.lineWidth = 2.5;
        ctx.strokeRect(currentX * CELL_SIZE - 1, currentY * CELL_SIZE - 1, kernelShape.w * CELL_SIZE + 2, kernelShape.h * CELL_SIZE + 2);
      }
    }
  
    function animate() {
      if (!isAnimating) return;
      const outputSize = (inputShape.w - kernelShape.w + 1) * (inputShape.h - kernelShape.h + 1);
      step = (step + 1) % (outputSize);
      draw();
      animFrame = setTimeout(() => requestAnimationFrame(animate), 40); // Slower, more deliberate speed
    }
  
    onMount(() => {
      canvas.getContext('2d').translate(0, 20);
      animate();
    });
  
    onDestroy(() => {
      isAnimating = false;
      clearTimeout(animFrame);
    });
  </script>
  
  <canvas 
    bind:this={canvas} 
    width={inputShape.w * CELL_SIZE + PADDING + (inputShape.w - kernelShape.w + 1) * CELL_SIZE} 
    height={inputShape.h * CELL_SIZE + 20}
  ></canvas>