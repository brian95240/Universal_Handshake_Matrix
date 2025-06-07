import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import DataTable from '../components/DataTable.vue';

describe('DataTable.vue', () => {
  const mockColumns = [
    { key: 'id', label: 'ID', sortable: true },
    { key: 'name', label: 'Name', sortable: true },
    { key: 'status', label: 'Status' },
    { key: 'date', label: 'Date', sortable: true, format: 'date' }
  ];

  const mockItems = [
    { id: '1', name: 'Item 1', status: 'active', date: '2023-01-01T00:00:00Z' },
    { id: '2', name: 'Item 2', status: 'inactive', date: '2023-01-02T00:00:00Z' },
    { id: '3', name: 'Item 3', status: 'pending', date: '2023-01-03T00:00:00Z' }
  ];

  it('renders with default props', () => {
    const wrapper = mount(DataTable, {
      props: {
        items: [],
        columns: mockColumns
      }
    });
    expect(wrapper.exists()).toBe(true);
    expect(wrapper.classes()).toContain('data-table-container');
  });

  it('renders table headers correctly', () => {
    const wrapper = mount(DataTable, {
      props: {
        items: mockItems,
        columns: mockColumns
      }
    });
    
    const headers = wrapper.findAll('th');
    expect(headers.length).toBe(mockColumns.length);
    
    mockColumns.forEach((column, index) => {
      expect(headers[index].text()).toContain(column.label);
    });
  });

  it('renders table rows correctly', () => {
    const wrapper = mount(DataTable, {
      props: {
        items: mockItems,
        columns: mockColumns
      }
    });
    
    const rows = wrapper.findAll('tbody tr');
    expect(rows.length).toBe(mockItems.length);
    
    // Check first row cells
    const firstRowCells = rows[0].findAll('td');
    expect(firstRowCells.length).toBe(mockColumns.length);
    expect(firstRowCells[0].text()).toBe(mockItems[0].id);
    expect(firstRowCells[1].text()).toBe(mockItems[0].name);
    expect(firstRowCells[2].text()).toBe(mockItems[0].status);
  });

  it('renders empty state when no items', () => {
    const emptyMessage = 'No data available';
    const wrapper = mount(DataTable, {
      props: {
        items: [],
        columns: mockColumns,
        emptyMessage
      }
    });
    
    expect(wrapper.find('.empty-message').exists()).toBe(true);
    expect(wrapper.find('.empty-message').text()).toContain(emptyMessage);
  });

  it('renders loading state when loading prop is true', () => {
    const wrapper = mount(DataTable, {
      props: {
        items: mockItems,
        columns: mockColumns,
        loading: true,
        loadingRows: 3
      }
    });
    
    expect(wrapper.find('.data-table--loading').exists()).toBe(true);
    const loadingRows = wrapper.findAll('.loading-row');
    expect(loadingRows.length).toBe(3);
  });

  it('formats date values correctly', () => {
    const wrapper = mount(DataTable, {
      props: {
        items: mockItems,
        columns: mockColumns
      }
    });
    
    const rows = wrapper.findAll('tbody tr');
    const dateCell = rows[0].findAll('td')[3];
    
    // Check that the date is formatted (not in ISO format)
    expect(dateCell.text()).not.toBe(mockItems[0].date);
    expect(dateCell.text()).toMatch(/\d{1,2}\/\d{1,2}\/\d{4}/);
  });

  it('emits row-click event when row is clicked', async () => {
    const wrapper = mount(DataTable, {
      props: {
        items: mockItems,
        columns: mockColumns
      }
    });
    
    const firstRow = wrapper.findAll('tbody tr')[0];
    await firstRow.trigger('click');
    
    expect(wrapper.emitted('row-click')).toBeTruthy();
    expect(wrapper.emitted('row-click')[0][0]).toEqual(mockItems[0]);
  });

  it('emits sort-change event when sortable header is clicked', async () => {
    const wrapper = mount(DataTable, {
      props: {
        items: mockItems,
        columns: mockColumns,
        sortBy: '',
        sortOrder: 'asc'
      }
    });
    
    // Find the first sortable header (ID)
    const sortableHeader = wrapper.find('th.sortable');
    await sortableHeader.trigger('click');
    
    expect(wrapper.emitted('update:sortBy')).toBeTruthy();
    expect(wrapper.emitted('update:sortOrder')).toBeTruthy();
    expect(wrapper.emitted('sort-change')).toBeTruthy();
    
    // Check that the correct sort parameters were emitted
    expect(wrapper.emitted('update:sortBy')[0][0]).toBe('id');
    expect(wrapper.emitted('update:sortOrder')[0][0]).toBe('asc');
    expect(wrapper.emitted('sort-change')[0][0]).toEqual({ sortBy: 'id', sortOrder: 'asc' });
  });

  it('toggles sort order when same header is clicked twice', async () => {
    const wrapper = mount(DataTable, {
      props: {
        items: mockItems,
        columns: mockColumns,
        sortBy: 'id',
        sortOrder: 'asc'
      }
    });
    
    // Find the ID header (already sorted asc)
    const sortableHeader = wrapper.find('th.sortable.sorted.asc');
    await sortableHeader.trigger('click');
    
    // Check that the sort order was toggled to desc
    expect(wrapper.emitted('update:sortOrder')[0][0]).toBe('desc');
  });

  it('renders pagination when enabled', () => {
    const wrapper = mount(DataTable, {
      props: {
        items: mockItems,
        columns: mockColumns,
        pagination: true,
        totalItems: 10,
        currentPage: 1,
        pageSize: 5
      }
    });
    
    expect(wrapper.find('.data-table-pagination').exists()).toBe(true);
    expect(wrapper.find('.pagination-info').text()).toContain('Showing 1-5 of 10 items');
  });

  it('emits page-change event when pagination button is clicked', async () => {
    const wrapper = mount(DataTable, {
      props: {
        items: mockItems,
        columns: mockColumns,
        pagination: true,
        totalItems: 20,
        currentPage: 1,
        pageSize: 5
      }
    });
    
    // Find the "Next" pagination button
    const nextButton = wrapper.find('.pagination-button:last-child');
    await nextButton.trigger('click');
    
    expect(wrapper.emitted('update:currentPage')).toBeTruthy();
    expect(wrapper.emitted('page-change')).toBeTruthy();
    expect(wrapper.emitted('update:currentPage')[0][0]).toBe(2);
  });

  it('renders custom cell content using scoped slots', () => {
    const wrapper = mount(DataTable, {
      props: {
        items: mockItems,
        columns: mockColumns
      },
      slots: {
        'cell-status': `<template #cell-status="{ value }"><span class="custom-status">{{ value.toUpperCase() }}</span></template>`
      }
    });
    
    const statusCell = wrapper.find('.custom-status');
    expect(statusCell.exists()).toBe(true);
    expect(statusCell.text()).toBe('ACTIVE'); // First item's status, uppercase
  });

  it('renders row actions when rowActions slot is provided', () => {
    const wrapper = mount(DataTable, {
      props: {
        items: mockItems,
        columns: mockColumns
      },
      slots: {
        rowActions: '<template #rowActions="{ item }"><button class="action-btn">Edit</button></template>'
      }
    });
    
    expect(wrapper.find('th.row-actions-header').exists()).toBe(true);
    expect(wrapper.findAll('.action-btn').length).toBe(mockItems.length);
  });
});
