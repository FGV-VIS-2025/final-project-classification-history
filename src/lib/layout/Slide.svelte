<script>
  let slideEl;
  let observer;

  // Scroll to top when this slide enters the viewport
  function handleIntersection(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        slideEl.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  }

  import { onMount, onDestroy } from "svelte";
  onMount(() => {
    observer = new IntersectionObserver(handleIntersection, { threshold: 0.01 });
    if (slideEl) observer.observe(slideEl);
  });
  onDestroy(() => {
    if (observer && slideEl) observer.unobserve(slideEl);
  });
</script>

<div class="slide" bind:this={slideEl}>
  <slot/>
</div>

<style>
  .slide {
    display: flex;
    flex-direction: row;
    gap: 20px;
    width: 100%;
    height: 100vh;
  }
</style>
