import { mount } from 'svelte'
import './app.css'
import App from './App.svelte'
import './i18n'
// import "bootstrap-maxlength"

const app = mount(App, {
  target: document.getElementById('svelte-app')!,
})

export default app
