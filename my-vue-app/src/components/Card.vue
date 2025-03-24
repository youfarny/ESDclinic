<!-- src/components/Card.vue -->
<template>
  <div 
    class="card" 
    :class="{ 'interactive': isInteractive }"
    :tabindex="isInteractive ? 0 : undefined"
    @click="handleClick"
    @keydown.enter="handleClick"
    @keydown.space="handleClick"
    role="region"
    :aria-labelledby="titleId"
  >
    <h2 :id="titleId" class="card-title">{{ title }}</h2>
    <div class="card-content">
      <p>{{ content }}</p>
      <slot></slot>
    </div>
    <div v-if="$slots.actions" class="card-actions">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  content: {
    type: String,
    default: ''
  },
  isInteractive: {
    type: Boolean,
    default: false
  },
  id: {
    type: String,
    default: () => `card-${Math.random().toString(36).substring(2, 9)}`
  }
});

const emit = defineEmits(['click']);

const titleId = computed(() => `title-${props.id}`);

function handleClick(event) {
  if (props.isInteractive) {
    emit('click', event);
  }
}
</script>

<style scoped>
.card {
  border: 1px solid #6c6464;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: #d1eef3;
  margin-bottom: 1.5rem;
  transition: all 0.2s ease;
}

.card-title {
  font-size: 1.25rem;
  margin-top: 0;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.card-content {
  color: #333;
  font-size: 1rem;
  line-height: 1.6;
}

.card-actions {
  margin-top: 1.5rem;
  display: flex;
  gap: 0.75rem;
}

.interactive {
  cursor: pointer;
}

.interactive:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.interactive:focus {
  outline: 2px solid #42b883;
  outline-offset: 2px;
}

/* High contrast mode adjustments */
@media (forced-colors: active) {
  .card {
    border: 2px solid CanvasText;
  }
  
  .interactive:focus {
    outline: 3px solid Highlight;
  }
}
</style>
