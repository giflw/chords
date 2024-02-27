import { LitElement, html } from 'lit';
import { customElement } from 'lit/decorators.js';

@customElement('nssc-hello-world')
class NSSCHelloWorldElement extends LitElement {
  override render() {
    return html`<p>Hello from NSSC.</p>`;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    'nssc-hello-world': NSSCHelloWorldElement;
  }
}
