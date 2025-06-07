&lt;template&gt;
  &lt;div class="data-table-container"&gt;
    &lt;div v-if="title || $slots.tableActions" class="data-table-header"&gt;
      &lt;h3 v-if="title" class="data-table-title"&gt;{{ title }}&lt;/h3&gt;
      &lt;div v-if="$slots.tableActions" class="data-table-actions"&gt;
        &lt;slot name="tableActions"&gt;&lt;/slot&gt;
      &lt;/div&gt;
    &lt;/div&gt;

    &lt;div v-if="$slots.filters" class="data-table-filters"&gt;
      &lt;slot name="filters"&gt;&lt;/slot&gt;
    &lt;/div&gt;

    &lt;div class="data-table-wrapper"&gt;
      &lt;table class="data-table" :class="{ 'data-table--loading': loading, 'data-table--hoverable': hoverable, 'data-table--bordered': bordered }"&gt;
        &lt;thead&gt;
          &lt;tr&gt;
            &lt;th v-for="column in visibleColumns" :key="column.key" 
                :class="[
                  column.sortable ? 'sortable' : '',
                  sortBy === column.key ? `sorted ${sortOrder}` : ''
                ]"
                @click="column.sortable ? handleSort(column.key) : null"&gt;
              {{ column.label }}
              &lt;span v-if="column.sortable" class="sort-icon"&gt;
                &lt;span class="sort-icon__up"&gt;▲&lt;/span&gt;
                &lt;span class="sort-icon__down"&gt;▼&lt;/span&gt;
              &lt;/span&gt;
            &lt;/th&gt;
            &lt;th v-if="$slots.rowActions" class="row-actions-header"&gt;Actions&lt;/th&gt;
          &lt;/tr&gt;
        &lt;/thead&gt;
        &lt;tbody&gt;
          &lt;template v-if="loading"&gt;
            &lt;tr v-for="i in loadingRows" :key="`loading-${i}`" class="loading-row"&gt;
              &lt;td v-for="column in visibleColumns" :key="`loading-${i}-${column.key}`" class="loading-cell"&gt;
                &lt;div class="loading-placeholder"&gt;&lt;/div&gt;
              &lt;/td&gt;
              &lt;td v-if="$slots.rowActions" class="loading-cell"&gt;
                &lt;div class="loading-placeholder"&gt;&lt;/div&gt;
              &lt;/td&gt;
            &lt;/tr&gt;
          &lt;/template&gt;
          &lt;template v-else-if="items.length === 0"&gt;
            &lt;tr class="empty-row"&gt;
              &lt;td :colspan="visibleColumns.length + ($slots.rowActions ? 1 : 0)" class="empty-message"&gt;
                &lt;slot name="emptyState"&gt;
                  &lt;div class="empty-state"&gt;
                    &lt;span class="empty-icon"&gt;📋&lt;/span&gt;
                    &lt;p&gt;{{ emptyMessage }}&lt;/p&gt;
                  &lt;/div&gt;
                &lt;/slot&gt;
              &lt;/td&gt;
            &lt;/tr&gt;
          &lt;/template&gt;
          &lt;template v-else&gt;
            &lt;tr v-for="(item, index) in items" :key="getItemKey(item, index)" @click="$emit('row-click', item)"&gt;
              &lt;td v-for="column in visibleColumns" :key="`${getItemKey(item, index)}-${column.key}`"&gt;
                &lt;slot :name="`cell-${column.key}`" :item="item" :value="getItemValue(item, column.key)"&gt;
                  {{ formatValue(getItemValue(item, column.key), column.format) }}
                &lt;/slot&gt;
              &lt;/td&gt;
              &lt;td v-if="$slots.rowActions" class="row-actions-cell"&gt;
                &lt;slot name="rowActions" :item="item" :index="index"&gt;&lt;/slot&gt;
              &lt;/td&gt;
            &lt;/tr&gt;
          &lt;/template&gt;
        &lt;/tbody&gt;
      &lt;/table&gt;
    &lt;/div&gt;

    &lt;div v-if="pagination && totalItems > 0" class="data-table-pagination"&gt;
      &lt;div class="pagination-info"&gt;
        Showing {{ paginationInfo.from }}-{{ paginationInfo.to }} of {{ totalItems }} items
      &lt;/div&gt;
      &lt;div class="pagination-controls"&gt;
        &lt;button 
          class="pagination-button" 
          :disabled="currentPage === 1" 
          @click="handlePageChange(currentPage - 1)"&gt;
          Previous
        &lt;/button&gt;
        
        &lt;div class="pagination-pages"&gt;
          &lt;button 
            v-for="page in paginationPages" 
            :key="page" 
            class="pagination-page" 
            :class="{ active: page === currentPage }"
            @click="handlePageChange(page)"&gt;
            {{ page }}
          &lt;/button&gt;
        &lt;/div&gt;
        
        &lt;button 
          class="pagination-button" 
          :disabled="currentPage === totalPages" 
          @click="handlePageChange(currentPage + 1)"&gt;
          Next
        &lt;/button&gt;
      &lt;/div&gt;
      
      &lt;div class="pagination-size"&gt;
        &lt;label for="page-size"&gt;Items per page:&lt;/label&gt;
        &lt;select id="page-size" v-model="pageSize" @change="handlePageSizeChange"&gt;
          &lt;option v-for="size in pageSizeOptions" :key="size" :value="size"&gt;{{ size }}&lt;/option&gt;
        &lt;/select&gt;
      &lt;/div&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script setup lang="ts"&gt;
/**
 * DataTable Component
 * 
 * A reusable data table component that supports sorting, pagination,
 * custom cell rendering, and row actions.
 */
import { computed, ref, watch } from 'vue';

export interface Column {
  key: string;
  label: string;
  sortable?: boolean;
  visible?: boolean;
  format?: string;
}

const props = defineProps({
  /**
   * Array of items to display in the table
   */
  items: {
    type: Array,
    required: true
  },
  /**
   * Array of column definitions
   */
  columns: {
    type: Array as () => Column[],
    required: true
  },
  /**
   * Property to use as the unique key for each item
   */
  itemKey: {
    type: String,
    default: 'id'
  },
  /**
   * Table title
   */
  title: {
    type: String,
    default: ''
  },
  /**
   * Whether the table is in a loading state
   */
  loading: {
    type: Boolean,
    default: false
  },
  /**
   * Number of loading placeholder rows to show
   */
  loadingRows: {
    type: Number,
    default: 5
  },
  /**
   * Message to display when there are no items
   */
  emptyMessage: {
    type: String,
    default: 'No data available'
  },
  /**
   * Whether to enable row hover effect
   */
  hoverable: {
    type: Boolean,
    default: true
  },
  /**
   * Whether to show borders between cells
   */
  bordered: {
    type: Boolean,
    default: false
  },
  /**
   * Whether to enable pagination
   */
  pagination: {
    type: Boolean,
    default: true
  },
  /**
   * Current page number (1-based)
   */
  currentPage: {
    type: Number,
    default: 1
  },
  /**
   * Number of items per page
   */
  pageSize: {
    type: Number,
    default: 10
  },
  /**
   * Total number of items (for server-side pagination)
   */
  totalItems: {
    type: Number,
    default: 0
  },
  /**
   * Available page size options
   */
  pageSizeOptions: {
    type: Array as () => number[],
    default: () => [10, 20, 50, 100]
  },
  /**
   * Field to sort by
   */
  sortBy: {
    type: String,
    default: ''
  },
  /**
   * Sort order (asc or desc)
   */
  sortOrder: {
    type: String,
    default: 'asc',
    validator: (value: string) => ['asc', 'desc'].includes(value)
  }
});

const emit = defineEmits([
  'update:currentPage',
  'update:pageSize',
  'update:sortBy',
  'update:sortOrder',
  'page-change',
  'sort-change',
  'row-click'
]);

// Computed properties
const visibleColumns = computed(() => {
  return props.columns.filter(column => column.visible !== false);
});

const totalPages = computed(() => {
  return Math.ceil(props.totalItems / props.pageSize);
});

const paginationInfo = computed(() => {
  const from = (props.currentPage - 1) * props.pageSize + 1;
  const to = Math.min(props.currentPage * props.pageSize, props.totalItems);
  return { from, to };
});

const paginationPages = computed(() => {
  const pages = [];
  const maxVisiblePages = 5;
  
  if (totalPages.value <= maxVisiblePages) {
    // Show all pages if there are few
    for (let i = 1; i <= totalPages.value; i++) {
      pages.push(i);
    }
  } else {
    // Show a subset of pages with current page in the middle
    let startPage = Math.max(1, props.currentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(totalPages.value, startPage + maxVisiblePages - 1);
    
    // Adjust if we're near the end
    if (endPage === totalPages.value) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }
    
    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }
  }
  
  return pages;
});

// Methods
const getItemKey = (item: any, index: number) => {
  return item[props.itemKey] || `item-${index}`;
};

const getItemValue = (item: any, key: string) => {
  // Handle nested properties with dot notation (e.g., "user.name")
  if (key.includes('.')) {
    return key.split('.').reduce((obj, prop) => obj && obj[prop], item);
  }
  return item[key];
};

const formatValue = (value: any, format?: string) => {
  if (value === undefined || value === null) {
    return '';
  }
  
  if (!format) {
    return value;
  }
  
  switch (format) {
    case 'date':
      return new Date(value).toLocaleDateString();
    case 'datetime':
      return new Date(value).toLocaleString();
    case 'currency':
      return typeof value === 'number' 
        ? value.toLocaleString('en-US', { style: 'currency', currency: 'USD' })
        : value;
    case 'percent':
      return typeof value === 'number'
        ? `${value.toFixed(2)}%`
        : value;
    default:
      return value;
  }
};

const handleSort = (key: string) => {
  let newSortOrder = 'asc';
  
  if (props.sortBy === key) {
    // Toggle sort order if already sorting by this column
    newSortOrder = props.sortOrder === 'asc' ? 'desc' : 'asc';
  }
  
  emit('update:sortBy', key);
  emit('update:sortOrder', newSortOrder);
  emit('sort-change', { sortBy: key, sortOrder: newSortOrder });
};

const handlePageChange = (page: number) => {
  if (page < 1 || page > totalPages.value) {
    return;
  }
  
  emit('update:currentPage', page);
  emit('page-change', page);
};

const handlePageSizeChange = () => {
  emit('update:pageSize', props.pageSize);
  // Reset to first page when changing page size
  emit('update:currentPage', 1);
  emit('page-change', 1);
};
&lt;/script&gt;

&lt;style scoped&gt;
.data-table-container {
  width: 100%;
  overflow: hidden;
  border-radius: var(--table-border-radius, 8px);
  background-color: var(--table-bg-color, #ffffff);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.data-table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--table-border-color, rgba(0, 0, 0, 0.1));
}

.data-table-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--table-title-color, #333333);
}

.data-table-actions {
  display: flex;
  gap: 8px;
}

.data-table-filters {
  padding: 12px 20px;
  border-bottom: 1px solid var(--table-border-color, rgba(0, 0, 0, 0.1));
  background-color: var(--table-filter-bg-color, #f9f9f9);
}

.data-table-wrapper {
  overflow-x: auto;
  width: 100%;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.data-table th {
  padding: 12px 16px;
  font-weight: 600;
  color: var(--table-header-color, #555555);
  background-color: var(--table-header-bg-color, #f5f5f5);
  border-bottom: 2px solid var(--table-border-color, rgba(0, 0, 0, 0.1));
  position: sticky;
  top: 0;
  z-index: 1;
}

.data-table td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--table-border-color, rgba(0, 0, 0, 0.05));
  color: var(--table-cell-color, #333333);
}

.data-table--bordered th,
.data-table--bordered td {
  border: 1px solid var(--table-border-color, rgba(0, 0, 0, 0.1));
}

.data-table--hoverable tbody tr:hover {
  background-color: var(--table-hover-color, rgba(0, 0, 0, 0.02));
  cursor: pointer;
}

.data-table th.sortable {
  cursor: pointer;
  user-select: none;
}

.data-table th.sortable:hover {
  background-color: var(--table-header-hover-color, #eeeeee);
}

.sort-icon {
  display: inline-block;
  margin-left: 4px;
  position: relative;
  width: 12px;
  height: 12px;
}

.sort-icon__up,
.sort-icon__down {
  position: absolute;
  font-size: 8px;
  opacity: 0.3;
}

.sort-icon__up {
  top: -2px;
}

.sort-icon__down {
  bottom: -2px;
}

th.sorted.asc .sort-icon__up,
th.sorted.desc .sort-icon__down {
  opacity: 1;
}

.row-actions-header {
  width: 100px;
  text-align: center;
}

.row-actions-cell {
  text-align: center;
  white-space: nowrap;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: var(--table-empty-color, #999999);
}

.empty-icon {
  font-size: 2rem;
  margin-bottom: 12px;
}

.loading-placeholder {
  height: 16px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading-pulse 1.5s infinite;
  border-radius: 4px;
}

@keyframes loading-pulse {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.data-table-pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  border-top: 1px solid var(--table-border-color, rgba(0, 0, 0, 0.1));
  background-color: var(--table-pagination-bg-color, #f9f9f9);
  flex-wrap: wrap;
  gap: 12px;
}

.pagination-info {
  color: var(--table-pagination-info-color, #666666);
  font-size: 0.9rem;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pagination-button {
  padding: 6px 12px;
  border: 1px solid var(--table-pagination-button-border, #d0d0d0);
  background-color: var(--table-pagination-button-bg, #ffffff);
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.pagination-button:hover:not(:disabled) {
  background-color: var(--table-pagination-button-hover-bg, #f0f0f0);
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-pages {
  display: flex;
  gap: 4px;
}

.pagination-page {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--table-pagination-page-border, #d0d0d0);
  background-color: var(--table-pagination-page-bg, #ffffff);
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.pagination-page:hover:not(.active) {
  background-color: var(--table-pagination-page-hover-bg, #f0f0f0);
}

.pagination-page.active {
  background-color: var(--table-pagination-page-active-bg, #4a6cf7);
  color: white;
  border-color: var(--table-pagination-page-active-border, #4a6cf7);
}

.pagination-size {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  color: var(--table-pagination-size-color, #666666);
}

.pagination-size select {
  padding: 4px 8px;
  border: 1px solid var(--table-pagination-select-border, #d0d0d0);
  border-radius: 4px;
  background-color: var(--table-pagination-select-bg, #ffffff);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .data-table-pagination {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .pagination-controls {
    width: 100%;
    justify-content: center;
  }
  
  .pagination-size {
    width: 100%;
    justify-content: flex-end;
  }
}
&lt;/style&gt;
