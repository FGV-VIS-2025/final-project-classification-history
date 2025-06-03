<script>
  let stepEl;
  let observer;

  function handleIntersection(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        stepEl.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  }

  import { onMount, onDestroy } from "svelte";
  onMount(() => {
    observer = new IntersectionObserver(handleIntersection, { threshold: 0.01 });
    if (stepEl) observer.observe(stepEl);
  });
  onDestroy(() => {
    if (observer && stepEl) observer.unobserve(stepEl);
  });
</script>

<div class="step" bind:this={stepEl}>
    <slot/>
</div>

<style>
    .step {
        min-height: 100vh;
        width: 100%;
        padding: 20px;
    }
</style>