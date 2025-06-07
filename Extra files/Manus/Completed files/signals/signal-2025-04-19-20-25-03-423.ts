import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import { createRouter, createWebHistory } from 'vue-router';
import ProgramIndexView from '../views/ProgramIndexView.vue';
import BaseCard from '../components/BaseCard.vue';
import DataTable from '../components/DataTable.vue';
import { usePrograms } from '../composables/usePrograms';

// Mock the usePrograms composable
vi.mock('../composables/usePrograms', () => ({
  usePrograms: vi.fn(() => ({
    getPrograms: vi.fn().mockResolvedValue({
      data: [
        {
          id: 'prog_1',
          name: 'Amazon Associates',
          status: 'active',
          commission: { type: 'percentage', value: 10 },
          category: ['E-commerce'],
          cookieDuration: 30,
          epc: 1.5,
          conversionRate: 2.5,
          lastUpdated: '2023-01-01T00:00:00Z'
        },
        {
          id: 'prog_2',
          name: 'ClickBank',
          status: 'inactive',
          commission: { type: 'percentage', value: 15 },
          category: ['Digital Products'],
          cookieDuration: 60,
          epc: 2.0,
          conversionRate: 3.0,
          lastUpdated: '2023-01-02T00:00:00Z'
        }
      ],
      pagination: {
        page: 1,
        limit: 10,
        total: 2,
        total_pages: 1
      }
    }),
    loading: false
  }))
}));

// Create a mock router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/programs/:id', component: { template: '<div>Program Detail</div>' } },
    { path: '/programs/:id/edit', component: { template: '<div>Edit Program</div>' } },
    { path: '/programs/new', component: { template: '<div>New Program</div>' } }
  ]
});

describe('ProgramIndexView.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the component', async () => {
    const wrapper = mount(ProgramIndexView, {
      global: {
        plugins: [router],
        stubs: {
          BaseCard: true,
          DataTable: true
        }
      }
    });
    
    await flushPromises();
    
    expect(wrapper.exists()).toBe(true);
    expect(wrapper.find('.program-index-view').exists()).toBe(true);
  });

  it('fetches programs on mount', async () => {
    const { getPrograms } = usePrograms();
    
    const wrapper = mount(ProgramIndexView, {
      global: {
        plugins: [router],
        stubs: {
          BaseCard: true,
          DataTable: true
        }
      }
    });
    
    await flushPromises();
    
    expect(getPrograms).toHaveBeenCalledTimes(1);
    expect(getPrograms).toHaveBeenCalledWith(expect.objectContaining({
      page: 1,
      limit: 10
    }));
  });

  it('renders BaseCard and DataTable components', async () => {
    const wrapper = mount(ProgramIndexView, {
      global: {
        plugins: [router],
        components: {
          BaseCard,
          DataTable
        }
      }
    });
    
    await flushPromises();
    
    expect(wrapper.findComponent(BaseCard).exists()).toBe(true);
    expect(wrapper.findComponent(DataTable).exists()).toBe(true);
  });

  it('displays program data in the table', async () => {
    const wrapper = mount(ProgramIndexView, {
      global: {
        plugins: [router],
        stubs: {
          BaseCard: false,
          DataTable: false
        }
      }
    });
    
    await flushPromises();
    
    // Check that the DataTable has the correct props
    const dataTable = wrapper.findComponent(DataTable);
    expect(dataTable.props('items').length).toBe(2);
    expect(dataTable.props('items')[0].name).toBe('Amazon Associates');
    expect(dataTable.props('items')[1].name).toBe('ClickBank');
  });

  it('navigates to program detail when a row is clicked', async () => {
    const routerPushSpy = vi.spyOn(router, 'push');
    
    const wrapper = mount(ProgramIndexView, {
      global: {
        plugins: [router],
        stubs: {
          BaseCard: false
        }
      }
    });
    
    await flushPromises();
    
    // Simulate row click by calling the handler directly
    await wrapper.vm.handleProgramClick({ id: 'prog_1' });
    
    expect(routerPushSpy).toHaveBeenCalledWith('/programs/prog_1');
  });

  it('navigates to edit program when edit button is clicked', async () => {
    const routerPushSpy = vi.spyOn(router, 'push');
    
    const wrapper = mount(ProgramIndexView, {
      global: {
        plugins: [router],
        stubs: {
          BaseCard: false
        }
      }
    });
    
    await flushPromises();
    
    // Simulate edit button click by calling the handler directly
    await wrapper.vm.editProgram({ id: 'prog_1' });
    
    expect(routerPushSpy).toHaveBeenCalledWith('/programs/prog_1/edit');
  });

  it('navigates to new program when add button is clicked', async () => {
    const routerPushSpy = vi.spyOn(router, 'push');
    
    const wrapper = mount(ProgramIndexView, {
      global: {
        plugins: [router],
        stubs: {
          BaseCard: false,
          DataTable: true
        }
      }
    });
    
    await flushPromises();
    
    // Find the Add Program button and click it
    const addButton = wrapper.find('button.btn-primary');
    await addButton.trigger('click');
    
    expect(routerPushSpy).toHaveBeenCalledWith('/programs/new');
  });

  it('updates filters and refetches data when filters change', async () => {
    const { getPrograms } = usePrograms();
    
    const wrapper = mount(ProgramIndexView, {
      global: {
        plugins: [router],
        stubs: {
          BaseCard: false,
          DataTable: true
        }
      }
    });
    
    await flushPromises();
    
    // Reset mock to clear initial call
    vi.clearAllMocks();
    
    // Update a filter
    await wrapper.setData({
      filters: {
        ...wrapper.vm.filters,
        status: 'active'
      }
    });
    
    // Trigger the filter change handler
    await wrapper.vm.handleFilterChange();
    
    // Check that getPrograms was called with updated filters
    expect(getPrograms).toHaveBeenCalledTimes(1);
    expect(getPrograms).toHaveBeenCalledWith(expect.objectContaining({
      status: 'active',
      page: 1 // Should reset to page 1
    }));
  });

  it('clears filters when clear button is clicked', async () => {
    const wrapper = mount(ProgramIndexView, {
      global: {
        plugins: [router],
        stubs: {
          BaseCard: false,
          DataTable: true
        }
      }
    });
    
    await flushPromises();
    
    // Set some filters
    await wrapper.setData({
      filters: {
        status: 'active',
        category: 'E-commerce',
        minCommission: 10
      }
    });
    
    // Call the clearFilters method
    await wrapper.vm.clearFilters();
    
    // Check that filters were cleared
    expect(wrapper.vm.filters.status).toBe('');
    expect(wrapper.vm.filters.category).toBe('');
    expect(wrapper.vm.filters.minCommission).toBeNull();
  });

  it('toggles advanced filters when button is clicked', async () => {
    const wrapper = mount(ProgramIndexView, {
      global: {
        plugins: [router],
        stubs: {
          BaseCard: false,
          DataTable: true
        }
      }
    });
    
    await flushPromises();
    
    // Check initial state
    expect(wrapper.vm.showAdvancedFilters).toBe(false);
    
    // Call the toggle method
    await wrapper.vm.toggleAdvancedFilters();
    
    // Check that state was toggled
    expect(wrapper.vm.showAdvancedFilters).toBe(true);
    
    // Call the toggle method again
    await wrapper.vm.toggleAdvancedFilters();
    
    // Check that state was toggled back
    expect(wrapper.vm.showAdvancedFilters).toBe(false);
  });

  it('handles pagination changes', async () => {
    const { getPrograms } = usePrograms();
    
    const wrapper = mount(ProgramIndexView, {
      global: {
        plugins: [router],
        stubs: {
          BaseCard: false,
          DataTable: true
        }
      }
    });
    
    await flushPromises();
    
    // Reset mock to clear initial call
    vi.clearAllMocks();
    
    // Call the page change handler
    await wrapper.vm.handlePageChange(2);
    
    // Check that pagination was updated and getPrograms was called
    expect(wrapper.vm.pagination.page).toBe(2);
    expect(getPrograms).toHaveBeenCalledTimes(1);
    expect(getPrograms).toHaveBeenCalledWith(expect.objectContaining({
      page: 2
    }));
  });

  it('handles page size changes', async () => {
    const { getPrograms } = usePrograms();
    
    const wrapper = mount(ProgramIndexView, {
      global: {
        plugins: [router],
        stubs: {
          BaseCard: false,
          DataTable: true
        }
      }
    });
    
    await flushPromises();
    
    // Reset mock to clear initial call
    vi.clearAllMocks();
    
    // Call the page size change handler
    await wrapper.vm.handlePageSizeChange(20);
    
    // Check that pagination was updated and getPrograms was called
    expect(wrapper.vm.pagination.limit).toBe(20);
    expect(wrapper.vm.pagination.page).toBe(1); // Should reset to page 1
    expect(getPrograms).toHaveBeenCalledTimes(1);
    expect(getPrograms).toHaveBeenCalledWith(expect.objectContaining({
      limit: 20,
      page: 1
    }));
  });

  it('handles sort changes', async () => {
    const { getPrograms } = usePrograms();
    
    const wrapper = mount(ProgramIndexView, {
      global: {
        plugins: [router],
        stubs: {
          BaseCard: false,
          DataTable: true
        }
      }
    });
    
    await flushPromises();
    
    // Reset mock to clear initial call
    vi.clearAllMocks();
    
    // Call the sort change handler
    await wrapper.vm.handleSortChange({ sortBy: 'name', sortOrder: 'desc' });
    
    // Check that sorting was updated and getPrograms was called
    expect(wrapper.vm.sorting.sortBy).toBe('name');
    expect(wrapper.vm.sorting.sortOrder).toBe('desc');
    expect(getPrograms).toHaveBeenCalledTimes(1);
    expect(getPrograms).toHaveBeenCalledWith(expect.objectContaining({
      sort: 'name',
      order: 'desc'
    }));
  });

  it('refreshes data when refresh button is clicked', async () => {
    const { getPrograms } = usePrograms();
    
    const wrapper = mount(ProgramIndexView, {
      global: {
        plugins: [router],
        stubs: {
          BaseCard: false,
          DataTable: true
        }
      }
    });
    
    await flushPromises();
    
    // Reset mock to clear initial call
    vi.clearAllMocks();
    
    // Find the refresh button and click it
    const refreshButton = wrapper.find('button.btn-secondary');
    await refreshButton.trigger('click');
    
    // Check that getPrograms was called
    expect(getPrograms).toHaveBeenCalledTimes(1);
  });
});
