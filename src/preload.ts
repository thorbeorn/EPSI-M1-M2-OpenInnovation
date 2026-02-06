import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electron', {
  send: (channel: string, data?: any) => {
    const validChannels = ['login-attempt', 'get-equipment-id'];
    if (validChannels.includes(channel)) {
      ipcRenderer.send(channel, data);
    }
  },

  once: (channel: string, callback: (...args: any[]) => void) => {
    const validChannels = ['equipment-id-response', 'login-response'];
    if (validChannels.includes(channel)) {
      ipcRenderer.once(channel, (_, ...args) => callback(...args));
    }
  },

  on: (channel: string, callback: (...args: any[]) => void) => {
    const validChannels = ['equipment-id-response', 'login-response'];
    if (validChannels.includes(channel)) {
      const subscription = (_: any, ...args: any[]) => callback(...args);
      ipcRenderer.on(channel, subscription);

      return () => {
        ipcRenderer.removeListener(channel, subscription);
      };
    }
  },

  invoke: (channel: string, data?: any) => {
    const validChannels = ['get-equipment-id', 'login-attempt'];
    if (validChannels.includes(channel)) {
      return ipcRenderer.invoke(channel, data);
    }
  }
});