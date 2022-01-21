export * from './_pypi';

/**
 * The default CDN fallback for Pyodide
 */
export const PYODIDE_CDN_URL =
  'https://cdn.jsdelivr.net/pyodide/v0.19.0/full/pyodide.js';

/**
 * The id for the upstream extension, and key in the litePlugins.
 */

export const UPSTREAM_PLUGIN_ID =
  '@jupyterlite/pyolite-kernel-extension:kernel';

/**
 * The id for the extension.
 */

export const PLUGIN_ID = '@deathbeds/pidgy:kernel';
