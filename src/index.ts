import { app, BrowserWindow, ipcMain } from 'electron';
import { machineIdSync } from 'node-machine-id';

declare const MAIN_WINDOW_WEBPACK_ENTRY: string;
declare const MAIN_WINDOW_PRELOAD_WEBPACK_ENTRY: string;


if (require('electron-squirrel-startup')) {
  app.quit();
}

const createWindow = (): void => {
  const mainWindow = new BrowserWindow({
    height: 600,
    width: 800,
    webPreferences: {
      preload: MAIN_WINDOW_PRELOAD_WEBPACK_ENTRY,
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  mainWindow.loadURL(MAIN_WINDOW_WEBPACK_ENTRY);

  mainWindow.webContents.openDevTools();
};

app.on('ready', () => {
  setupIpcHandlers();
  createWindow();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

const setupIpcHandlers = () => {
  ipcMain.handle('get-equipment-id', async () => {
    const equipmentId = getEquipmentId();
    console.log('Equipment ID généré:', equipmentId);
    return equipmentId;
  });

  ipcMain.handle('login-attempt', async (event, data) => {
    console.log('Tentative de connexion reçue:');
    console.log('Email:', data.email);
    console.log('Password:', data.password);
    console.log('Equipment ID:', data.equipmentId);

    // Ici, vous pouvez :
    // 1. Valider les identifiants avec votre backend
    // 2. Faire une requête API
    // 3. Stocker l'equipment ID dans votre base de données
    
    try {
      // TODO: Remplacer par votre logique de validation
      // Exemple de requête API :
      // const response = await fetch('https://votre-api.com/login', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(data)
      // });
      // const result = await response.json();
      
      // Simuler une réponse réussie pour le moment
      return {
        success: true,
        message: 'Connexion réussie',
        equipmentId: data.equipmentId,
        user: {
          email: data.email
        }
      };
    } catch (error) {
      console.error('Erreur de connexion:', error);
      return {
        success: false,
        message: 'Échec de la connexion',
        error: error instanceof Error ? error.message : 'Erreur inconnue'
      };
    }
  });
};

function getEquipmentId(): string {
  try {
    const machineId = machineIdSync();
    return `EQ-${machineId.substring(0, 8).toUpperCase()}`;
  } catch (error) {
    console.error('Erreur lors de la génération de machine ID:', error);
    return `EQ-${Math.random().toString(36).substring(2, 10).toUpperCase()}`;
  }
}