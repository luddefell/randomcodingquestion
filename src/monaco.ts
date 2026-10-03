// The parts of the Monaco editor API we use. Monaco is loaded from a CDN in
// index.html, so these are hand-written instead of installing its 90 MB package.

export interface MonacoEditor {
  getValue(): string;
  setValue(value: string): void;
  getModel(): unknown;
  setPosition(pos: { lineNumber: number; column: number }): void;
  addCommand(keybinding: number, handler: () => void): void;
}

export interface Monaco {
  editor: {
    create(el: HTMLElement, options: Record<string, unknown>): MonacoEditor;
    setModelLanguage(model: unknown, language: string): void;
  };
  languages: { getLanguages(): { id: string }[] };
  KeyMod: { CtrlCmd: number };
  KeyCode: { Enter: number };
}
