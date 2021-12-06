import {
  JupyterLiteServer,
  JupyterLiteServerPlugin
} from '@jupyterlite/server';

/**
 * Initialization data for the @deathbeds/pidgy extension.
 */
const plugin: JupyterLiteServerPlugin<void> = {
  id: '@deathbeds/pidgy:plugin',
  autoStart: true,
  activate: (app: JupyterLiteServer) => {
    console.log('JupyterLite server extension @deathbeds/pidgy is activated!');
  }
};

export default plugin;
