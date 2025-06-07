&lt;template&gt;
  &lt;div class="program-index-view"&gt;
    &lt;BaseCard title="Affiliate Programs" class="program-list-card"&gt;
      &lt;template #headerActions&gt;
        &lt;button class="btn btn-primary" @click="handleAddProgram"&gt;
          &lt;span class="btn-icon"&gt;+&lt;/span&gt; Add Program
        &lt;/button&gt;
        &lt;button class="btn btn-secondary" @click="handleRefresh"&gt;
          &lt;span class="btn-icon"&gt;↻&lt;/span&gt; Refresh
        &lt;/button&gt;
      &lt;/template&gt;
      
      &lt;div class="program-filters"&gt;
        &lt;div class="filter-row"&gt;
          &lt;div class="filter-group"&gt;
            &lt;label for="search" class="filter-label"&gt;Search:&lt;/label&gt;
            &lt;input 
              id="search" 
              v-model="filters.search" 
              type="text" 
              class="filter-input" 
              placeholder="Search programs..."
              @input="handleFilterChange"
            /&gt;
          &lt;/div&gt;
          
          &lt;div class="filter-group"&gt;
            &lt;label for="status" class="filter-label"&gt;Status:&lt;/label&gt;
            &lt;select 
              id="status" 
              v-model="filters.status" 
              class="filter-select"
              @change="handleFilterChange"
            &gt;
              &lt;option value=""&gt;All Statuses&lt;/option&gt;
              &lt;option value="active"&gt;Active&lt;/option&gt;
              &lt;option value="inactive"&gt;Inactive&lt;/option&gt;
              &lt;option value="pending"&gt;Pending&lt;/option&gt;
            &lt;/select&gt;
          &lt;/div&gt;
          
          &lt;div class="filter-group"&gt;
            &lt;label for="category" class="filter-label"&gt;Category:&lt;/label&gt;
            &lt;select 
              id="category" 
              v-model="filters.category" 
              class="filter-select"
              @change="handleFilterChange"
            &gt;
              &lt;option value=""&gt;All Categories&lt;/option&gt;
              &lt;option v-for="category in availableCategories" :key="category" :value="category"&gt;
                {{ category }}
              &lt;/option&gt;
            &lt;/select&gt;
          &lt;/div&gt;
        &lt;/div&gt;
        
        &lt;div class="filter-row"&gt;
          &lt;div class="filter-group"&gt;
            &lt;label for="min-commission" class="filter-label"&gt;Min Commission:&lt;/label&gt;
            &lt;input 
              id="min-commission" 
              v-model.number="filters.minCommission" 
              type="number" 
              class="filter-input" 
              min="0"
              @change="handleFilterChange"
            /&gt;
          &lt;/div&gt;
          
          &lt;div class="filter-group"&gt;
            &lt;label for="min-epc" class="filter-label"&gt;Min EPC:&lt;/label&gt;
            &lt;input 
              id="min-epc" 
              v-model.number="filters.minEpc" 
              type="number" 
              class="filter-input" 
              min="0"
              @change="handleFilterChange"
            /&gt;
          &lt;/div&gt;
          
          &lt;div class="filter-group filter-actions"&gt;
            &lt;button class="btn btn-outline" @click="clearFilters"&gt;Clear Filters&lt;/button&gt;
            &lt;button class="btn btn-outline" @click="toggleAdvancedFilters"&gt;
              {{ showAdvancedFilters ? 'Hide Advanced' : 'Show Advanced' }}
            &lt;/button&gt;
          &lt;/div&gt;
        &lt;/div&gt;
        
        &lt;div v-if="showAdvancedFilters" class="filter-row advanced-filters"&gt;
          &lt;div class="filter-group"&gt;
            &lt;label for="source" class="filter-label"&gt;Source:&lt;/label&gt;
            &lt;select 
              id="source" 
              v-model="filters.source" 
              class="filter-select"
              @change="handleFilterChange"
            &gt;
              &lt;option value=""&gt;All Sources&lt;/option&gt;
              &lt;option v-for="source in availableSources" :key="source" :value="source"&gt;
                {{ source }}
              &lt;/option&gt;
            &lt;/select&gt;
          &lt;/div&gt;
          
          &lt;div class="filter-group"&gt;
            &lt;label for="min-conversion" class="filter-label"&gt;Min Conversion:&lt;/label&gt;
            &lt;input 
              id="min-conversion" 
              v-model.number="filters.minConversionRate" 
              type="number" 
              class="filter-input" 
              min="0"
              @change="handleFilterChange"
            /&gt;
          &lt;/div&gt;
          
          &lt;div class="filter-group"&gt;
            &lt;label for="tag" class="filter-label"&gt;Tag:&lt;/label&gt;
            &lt;select 
              id="tag" 
              v-model="filters.tag" 
              class="filter-select"
              @change="handleFilterChange"
            &gt;
              &lt;option value=""&gt;All Tags&lt;/option&gt;
              &lt;option v-for="tag in availableTags" :key="tag" :value="tag"&gt;
                {{ tag }}
              &lt;/option&gt;
            &lt;/select&gt;
          &lt;/div&gt;
        &lt;/div&gt;
      &lt;/div&gt;
      
      &lt;DataTable
        :items="programs"
        :columns="columns"
        :loading="loading"
        :total-items="totalItems"
        :current-page="pagination.page"
        :page-size="pagination.limit"
        :sort-by="sorting.sortBy"
        :sort-order="sorting.sortOrder"
        @update:current-page="handlePageChange"
        @update:page-size="handlePageSizeChange"
        @update:sort-by="sorting.sortBy = $event"
        @update:sort-order="sorting.sortOrder = $event"
        @sort-change="handleSortChange"
        @row-click="handleProgramClick"
      &gt;
        &lt;template #cell-status="{ value }"&gt;
          &lt;span class="status-badge" :class="value"&gt;{{ value }}&lt;/span&gt;
        &lt;/template&gt;
        
        &lt;template #cell-commission="{ item }"&gt;
          &lt;span v-if="item.commission.type === 'percentage'"&gt;
            {{ item.commission.value }}%
          &lt;/span&gt;
          &lt;span v-else-if="item.commission.type === 'fixed'"&gt;
            ${{ item.commission.value }}
          &lt;/span&gt;
          &lt;span v-else&gt;
            Tiered
          &lt;/span&gt;
        &lt;/template&gt;
        
        &lt;template #cell-category="{ value }"&gt;
          &lt;div class="category-tags"&gt;
            &lt;span v-for="(cat, index) in value" :key="index" class="category-tag"&gt;
              {{ cat }}
            &lt;/span&gt;
          &lt;/div&gt;
        &lt;/template&gt;
        
        &lt;template #rowActions="{ item }"&gt;
          &lt;div class="row-actions"&gt;
            &lt;button class="action-button view" @click.stop="viewProgram(item)"&gt;
              View
            &lt;/button&gt;
            &lt;button class="action-button edit" @click.stop="editProgram(item)"&gt;
              Edit
            &lt;/button&gt;
          &lt;/div&gt;
        &lt;/template&gt;
        
        &lt;template #emptyState&gt;
          &lt;div class="empty-programs"&gt;
            &lt;div class="empty-icon"&gt;🔍&lt;/div&gt;
            &lt;h3&gt;No programs found&lt;/h3&gt;
            &lt;p&gt;Try adjusting your filters or add a new program&lt;/p&gt;
            &lt;button class="btn btn-primary" @click="handleAddProgram"&gt;
              Add Program
            &lt;/button&gt;
          &lt;/div&gt;
        &lt;/template&gt;
      &lt;/DataTable&gt;
    &lt;/BaseCard&gt;
    
    &lt;div v-if="showMetricsCards" class="metrics-section"&gt;
      &lt;h2 class="section-title"&gt;Program Metrics&lt;/h2&gt;
      &lt;div class="metrics-grid"&gt;
        &lt;BaseCard title="Top Performing Programs" class="metrics-card"&gt;
          &lt;div class="metrics-content"&gt;
            &lt;div v-if="loading" class="metrics-loading"&gt;Loading...&lt;/div&gt;
            &lt;div v-else class="metrics-list"&gt;
              &lt;div v-for="program in topPrograms" :key="program.id" class="metrics-item"&gt;
                &lt;div class="metrics-item-name"&gt;{{ program.name }}&lt;/div&gt;
                &lt;div class="metrics-item-value"&gt;
                  ${{ program.metrics?.revenue.toFixed(2) }}
                &lt;/div&gt;
              &lt;/div&gt;
            &lt;/div&gt;
          &lt;/div&gt;
        &lt;/BaseCard&gt;
        
        &lt;BaseCard title="Program Categories" class="metrics-card"&gt;
          &lt;div class="metrics-content"&gt;
            &lt;div v-if="loading" class="metrics-loading"&gt;Loading...&lt;/div&gt;
            &lt;div v-else class="metrics-chart"&gt;
              &lt;!-- Placeholder for category chart --&gt;
              &lt;div class="chart-placeholder"&gt;
                Category distribution chart will be displayed here
              &lt;/div&gt;
            &lt;/div&gt;
          &lt;/div&gt;
        &lt;/BaseCard&gt;
        
        &lt;BaseCard title="Recent Activity" class="metrics-card"&gt;
          &lt;div class="metrics-content"&gt;
            &lt;div v-if="loading" class="metrics-loading"&gt;Loading...&lt;/div&gt;
            &lt;div v-else class="activity-list"&gt;
              &lt;div v-for="(activity, index) in recentActivity" :key="index" class="activity-item"&gt;
                &lt;div class="activity-icon" :class="activity.type"&gt;&lt;/div&gt;
                &lt;div class="activity-details"&gt;
                  &lt;div class="activity-message"&gt;{{ activity.message }}&lt;/div&gt;
                  &lt;div class="activity-time"&gt;{{ formatTime(activity.timestamp) }}&lt;/div&gt;
                &lt;/div&gt;
              &lt;/div&gt;
            &lt;/div&gt;
          &lt;/div&gt;
        &lt;/BaseCard&gt;
      &lt;/div&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script setup lang="ts"&gt;
/**
 * Program Index View
 * 
 * This view displays a list of affiliate programs with filtering, sorting,
 * and pagination capabilities. It also shows program metrics and recent activity.
 */
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import BaseCard from '../components/BaseCard.vue';
import DataTable from '../components/DataTable.vue';
import { usePrograms } from '../composables/usePrograms';
import type { Program } from '../contracts/typescript/interfaces';

// Router for navigation
const router = useRouter();

// Use the programs composable
const { 
  getPrograms, 
  loading: programsLoading 
} = usePrograms();

// Table columns definition
const columns = [
  { key: 'name', label: 'Program Name', sortable: true },
  { key: 'status', label: 'Status', sortable: true },
  { key: 'commission', label: 'Commission', sortable: true },
  { key: 'category', label: 'Categories' },
  { key: 'cookieDuration', label: 'Cookie (Days)', sortable: true },
  { key: 'epc', label: 'EPC', sortable: true },
  { key: 'conversionRate', label: 'Conv. Rate', sortable: true, format: 'percent' },
  { key: 'lastUpdated', label: 'Last Updated', sortable: true, format: 'date' }
];

// State
const loading = ref(false);
const programs = ref<Program[]>([]);
const totalItems = ref(0);
const showAdvancedFilters = ref(false);
const showMetricsCards = ref(true);

// Pagination state
const pagination = reactive({
  page: 1,
  limit: 10
});

// Sorting state
const sorting = reactive({
  sortBy: 'name',
  sortOrder: 'asc' as 'asc' | 'desc'
});

// Filters state
const filters = reactive({
  search: '',
  status: '',
  category: '',
  source: '',
  tag: '',
  minCommission: null as number | null,
  minEpc: null as number | null,
  minConversionRate: null as number | null
});

// Available filter options (would be fetched from API in a real implementation)
const availableCategories = ref(['E-commerce', 'Finance', 'Health', 'Technology', 'Travel']);
const availableSources = ref(['Manual', 'API', 'Import']);
const availableTags = ref(['High Commission', 'Fast Payout', 'Recurring', 'Exclusive']);

// Top performing programs (would be fetched from API in a real implementation)
const topPrograms = ref([
  { id: 'prog_1', name: 'Amazon Associates', metrics: { revenue: 5240.50 } },
  { id: 'prog_2', name: 'ClickBank', metrics: { revenue: 3120.75 } },
  { id: 'prog_3', name: 'ShareASale', metrics: { revenue: 2890.30 } },
  { id: 'prog_4', name: 'CJ Affiliate', metrics: { revenue: 2150.25 } },
  { id: 'prog_5', name: 'Rakuten Marketing', metrics: { revenue: 1980.60 } }
]);

// Recent activity (would be fetched from API in a real implementation)
const recentActivity = ref([
  { type: 'sync', message: 'Amazon Associates program synced', timestamp: new Date(Date.now() - 3600000) },
  { type: 'update', message: 'ClickBank commission updated to 12%', timestamp: new Date(Date.now() - 7200000) },
  { type: 'add', message: 'Added new program: Shopify Affiliates', timestamp: new Date(Date.now() - 86400000) },
  { type: 'status', message: 'ShareASale program status changed to active', timestamp: new Date(Date.now() - 172800000) }
]);

// Fetch programs on component mount
onMounted(async () => {
  await fetchPrograms();
});

// Watch for changes in pagination, sorting, or filters
watch([pagination, sorting, filters], async () => {
  await fetchPrograms();
}, { deep: true });

// Methods
const fetchPrograms = async () => {
  loading.value = true;
  
  try {
    // In a real implementation, this would call the API with all filters, sorting, and pagination
    const response = await getPrograms({
      page: pagination.page,
      limit: pagination.limit,
      sort: sorting.sortBy,
      order: sorting.sortOrder,
      status: filters.status,
      category: filters.category,
      tag: filters.tag,
      source: filters.source,
      search: filters.search,
      min_commission: filters.minCommission,
      min_epc: filters.minEpc,
      min_conversion_rate: filters.minConversionRate
    });
    
    programs.value = response.data;
    totalItems.value = response.pagination.total;
  } catch (error) {
    console.error('Error fetching programs:', error);
    // In a real implementation, this would show an error notification
  } finally {
    loading.value = false;
  }
};

const handleFilterChange = () => {
  // Reset to first page when filters change
  pagination.page = 1;
};

const clearFilters = () => {
  // Reset all filters
  Object.keys(filters).forEach(key => {
    if (typeof filters[key as keyof typeof filters] === 'string') {
      (filters[key as keyof typeof filters] as string) = '';
    } else {
      (filters[key as keyof typeof filters] as number | null) = null;
    }
  });
  
  // Reset pagination
  pagination.page = 1;
};

const toggleAdvancedFilters = () => {
  showAdvancedFilters.value = !showAdvancedFilters.value;
};

const handlePageChange = (page: number) => {
  pagination.page = page;
};

const handlePageSizeChange = (size: number) => {
  pagination.limit = size;
  pagination.page = 1; // Reset to first page
};

const handleSortChange = ({ sortBy, sortOrder }: { sortBy: string, sortOrder: 'asc' | 'desc' }) => {
  sorting.sortBy = sortBy;
  sorting.sortOrder = sortOrder;
};

const handleProgramClick = (program: Program) => {
  router.push(`/programs/${program.id}`);
};

const viewProgram = (program: Program) => {
  router.push(`/programs/${program.id}`);
};

const editProgram = (program: Program) => {
  router.push(`/programs/${program.id}/edit`);
};

const handleAddProgram = () => {
  router.push('/programs/new');
};

const handleRefresh = async () => {
  await fetchPrograms();
};

const formatTime = (date: Date) => {
  // Format relative time (e.g., "2 hours ago")
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffSec = Math.round(diffMs / 1000);
  const diffMin = Math.round(diffSec / 60);
  const diffHour = Math.round(diffMin / 60);
  const diff
(Content truncated due to size limit. Use line ranges to read in chunks)