import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import BaseCard from '../components/BaseCard.vue';

describe('BaseCard.vue', () => {
  it('renders with default props', () => {
    const wrapper = mount(BaseCard);
    expect(wrapper.exists()).toBe(true);
    expect(wrapper.classes()).toContain('base-card');
  });

  it('renders title when provided', () => {
    const title = 'Test Card Title';
    const wrapper = mount(BaseCard, {
      props: { title }
    });
    
    expect(wrapper.find('.base-card__title').exists()).toBe(true);
    expect(wrapper.find('.base-card__title').text()).toBe(title);
  });

  it('does not render header when no title or header actions', () => {
    const wrapper = mount(BaseCard);
    expect(wrapper.find('.base-card__header').exists()).toBe(false);
  });

  it('renders content slot', () => {
    const contentText = 'Test content';
    const wrapper = mount(BaseCard, {
      slots: {
        default: contentText
      }
    });
    
    expect(wrapper.find('.base-card__content').exists()).toBe(true);
    expect(wrapper.find('.base-card__content').text()).toBe(contentText);
  });

  it('renders footer slot when provided', () => {
    const footerText = 'Test footer';
    const wrapper = mount(BaseCard, {
      slots: {
        footer: footerText
      }
    });
    
    expect(wrapper.find('.base-card__footer').exists()).toBe(true);
    expect(wrapper.find('.base-card__footer').text()).toBe(footerText);
  });

  it('does not render footer when slot not provided', () => {
    const wrapper = mount(BaseCard);
    expect(wrapper.find('.base-card__footer').exists()).toBe(false);
  });

  it('renders header actions slot when provided', () => {
    const actionText = 'Action Button';
    const wrapper = mount(BaseCard, {
      props: { title: 'Card with Actions' },
      slots: {
        headerActions: `<button>${actionText}</button>`
      }
    });
    
    expect(wrapper.find('.base-card__header-actions').exists()).toBe(true);
    expect(wrapper.find('.base-card__header-actions button').text()).toBe(actionText);
  });

  it('applies variant class when provided', () => {
    const variant = 'primary';
    const wrapper = mount(BaseCard, {
      props: { variant }
    });
    
    expect(wrapper.classes()).toContain(variant);
  });

  it('applies elevated class when elevated prop is true', () => {
    const wrapper = mount(BaseCard, {
      props: { elevated: true }
    });
    
    expect(wrapper.classes()).toContain('elevated');
  });

  it('does not apply elevated class when elevated prop is false', () => {
    const wrapper = mount(BaseCard, {
      props: { elevated: false }
    });
    
    expect(wrapper.classes()).not.toContain('elevated');
  });
});
