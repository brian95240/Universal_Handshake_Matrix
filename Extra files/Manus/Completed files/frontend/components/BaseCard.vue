&lt;template&gt;
  &lt;div class="base-card"&gt;
    &lt;div v-if="title" class="base-card__header"&gt;
      &lt;h3 class="base-card__title"&gt;{{ title }}&lt;/h3&gt;
      &lt;div v-if="$slots.headerActions" class="base-card__header-actions"&gt;
        &lt;slot name="headerActions"&gt;&lt;/slot&gt;
      &lt;/div&gt;
    &lt;/div&gt;
    &lt;div class="base-card__content"&gt;
      &lt;slot&gt;&lt;/slot&gt;
    &lt;/div&gt;
    &lt;div v-if="$slots.footer" class="base-card__footer"&gt;
      &lt;slot name="footer"&gt;&lt;/slot&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script setup lang="ts"&gt;
/**
 * BaseCard Component
 * 
 * A reusable card component that provides a consistent layout for content
 * with optional header, title, and footer sections.
 */
import { defineProps } from 'vue';

defineProps({
  /**
   * Card title displayed in the header
   */
  title: {
    type: String,
    default: ''
  },
  /**
   * Card variant for styling purposes
   */
  variant: {
    type: String,
    default: 'default',
    validator: (value: string) => ['default', 'primary', 'secondary', 'outlined'].includes(value)
  },
  /**
   * Whether to add padding to the card content
   */
  padded: {
    type: Boolean,
    default: true
  },
  /**
   * Whether to add a shadow to the card
   */
  elevated: {
    type: Boolean,
    default: true
  }
});
&lt;/script&gt;

&lt;style scoped&gt;
.base-card {
  background-color: var(--card-bg-color, #ffffff);
  border-radius: var(--card-border-radius, 8px);
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--card-border-color, rgba(0, 0, 0, 0.1));
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.base-card.elevated {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.base-card:hover.elevated {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.base-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--card-border-color, rgba(0, 0, 0, 0.1));
}

.base-card__title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--card-title-color, #333333);
}

.base-card__header-actions {
  display: flex;
  gap: 8px;
}

.base-card__content {
  flex: 1;
  padding: var(--card-content-padding, 20px);
}

.base-card__content:not(.padded) {
  padding: 0;
}

.base-card__footer {
  padding: 12px 20px;
  border-top: 1px solid var(--card-border-color, rgba(0, 0, 0, 0.1));
  background-color: var(--card-footer-bg-color, #f9f9f9);
}

/* Variants */
.base-card.primary {
  border-color: var(--primary-color, #4a6cf7);
}

.base-card.primary .base-card__header {
  background-color: var(--primary-color, #4a6cf7);
  color: white;
}

.base-card.primary .base-card__title {
  color: white;
}

.base-card.secondary {
  border-color: var(--secondary-color, #6c757d);
}

.base-card.secondary .base-card__header {
  background-color: var(--secondary-color, #6c757d);
  color: white;
}

.base-card.secondary .base-card__title {
  color: white;
}

.base-card.outlined {
  background-color: transparent;
  border: 1px solid var(--card-border-color, rgba(0, 0, 0, 0.1));
  box-shadow: none;
}

.base-card.outlined:hover {
  box-shadow: none;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .base-card__header {
    padding: 12px 16px;
  }
  
  .base-card__content {
    padding: 16px;
  }
  
  .base-card__footer {
    padding: 10px 16px;
  }
}
&lt;/style&gt;
