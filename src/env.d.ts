interface Window {
  electron: {
    send: (channel: string, data?: any) => void;
    once: (channel: string, callback: (...args: any[]) => void) => void;
    on: (channel: string, callback: (...args: any[]) => void) => (() => void) | undefined;
    invoke: (channel: string, data?: any) => Promise<any>;
  }
}