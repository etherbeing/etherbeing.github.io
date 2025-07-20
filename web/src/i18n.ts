// src/i18n.js
import { getLocaleFromNavigator, init, register } from 'svelte-i18n';

register('en', () => import('./locales/en/base.json'));
register('es', () => import('./locales/es/base.json'));
register('pt', () => import('./locales/pt/base.json'));

init({
  fallbackLocale: 'en',
  initialLocale: getLocaleFromNavigator(),
});