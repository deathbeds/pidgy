"use strict";
(self["webpackChunkjupyterlab_execute_time"] = self["webpackChunkjupyterlab_execute_time"] || []).push([["lib_index_js"],{

/***/ "./lib/ExecuteTimeWidget.js":
/*!**********************************!*\
  !*** ./lib/ExecuteTimeWidget.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.PLUGIN_NAME = void 0;
const widgets_1 = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
const coreutils_1 = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
const formatters_1 = __webpack_require__(/*! ./formatters */ "./lib/formatters.js");
const date_fns_1 = __webpack_require__(/*! date-fns */ "webpack/sharing/consume/default/date-fns/date-fns");
exports.PLUGIN_NAME = 'jupyterlab-execute-time';
const EXECUTE_TIME_CLASS = 'execute-time';
const TOOLTIP_PREFIX = 'Previous Runs:';
const PREV_DATA_EXECUTION_TIME_ATTR = 'data-prev-execution-time';
// How long do we animate the color for
const ANIMATE_TIME_MS = 1000;
const ANIMATE_CSS = `executeHighlight ${ANIMATE_TIME_MS}ms`;
class ExecuteTimeWidget extends widgets_1.Widget {
    constructor(panel, tracker, settingRegistry) {
        super();
        this._cellSlotMap = {};
        this._settings = {
            enabled: false,
            highlight: true,
            positioning: 'left',
            minTime: 0,
            textContrast: 'high',
            showLiveExecutionTime: true,
            historyCount: 5,
        };
        this._panel = panel;
        this._tracker = tracker;
        this._settingRegistry = settingRegistry;
        this.updateConnectedCell = this.updateConnectedCell.bind(this);
        settingRegistry.load(`${exports.PLUGIN_NAME}:settings`).then((settings) => {
            this._updateSettings(settings);
            settings.changed.connect(this._updateSettings.bind(this));
            // If the plugin is enabled, force recoding of timing
            // We only do this once (not on every settings update) in case the user tries to trun it off
            if (settings.get('enabled').composite) {
                this._settingRegistry
                    .load('@jupyterlab/notebook-extension:tracker')
                    .then((nbSettings) => nbSettings.set('recordTiming', true), (err) => {
                    console.error(`jupyterlab-execute-time: Could not force metadata recording: ${err}`);
                });
            }
        }, (err) => {
            console.error(`jupyterlab-execute-time: Could not load settings, so did not active ${exports.PLUGIN_NAME}: ${err}`);
        });
    }
    updateConnectedCell(cells, changed) {
        // While we could look at changed.type, it's easier to just remove all
        // oldValues and add back all new values
        changed.oldValues.forEach(this._deregisterMetadataChanges.bind(this));
        changed.newValues.forEach(this._registerMetadataChanges.bind(this));
    }
    _registerMetadataChanges(cellModel) {
        if (!(cellModel.id in this._cellSlotMap)) {
            const fn = () => this._cellMetadataChanged(cellModel);
            this._cellSlotMap[cellModel.id] = fn;
            cellModel.metadata.changed.connect(fn);
        }
        // Always re-render cells.
        // In case there was already metadata: do not highlight on first load.
        this._cellMetadataChanged(cellModel, true);
    }
    _deregisterMetadataChanges(cellModel) {
        const fn = this._cellSlotMap[cellModel.id];
        if (fn) {
            cellModel.metadata.changed.disconnect(fn);
            const codeCell = this._getCodeCell(cellModel);
            if (codeCell) {
                this._removeExecuteNode(codeCell);
            }
        }
        delete this._cellSlotMap[cellModel.id];
    }
    _cellMetadataChanged(cellModel, disableHighlight = false) {
        const codeCell = this._getCodeCell(cellModel);
        if (codeCell) {
            this._updateCodeCell(codeCell, disableHighlight);
        }
        else {
            if (cellModel.type === 'code') {
                console.error(`Could not find code cell for model: ${cellModel}`);
            }
        }
    }
    /**
     * Return a codeCell for this model if there is one. This will return null
     * in cases of non-code cells.
     *
     * @param cellModel
     * @private
     */
    _getCodeCell(cellModel) {
        if (cellModel.type === 'code') {
            const cell = this._panel.content.widgets.find((widget) => widget.model === cellModel);
            return cell;
        }
        return null;
    }
    /**
     * If there was a executeTime node added, remove it
     * @param cell
     * @private
     */
    _removeExecuteNode(cell) {
        const executionTimeNode = cell.node.querySelector(`.${EXECUTE_TIME_CLASS}`);
        if (executionTimeNode) {
            executionTimeNode.remove();
        }
    }
    /**
     * Update the code cell to reflect the metadata
     * @param cell
     * @private
     */
    _updateCodeCell(cell, disableHighlight) {
        const executionMetadata = cell.model.metadata.get('execution');
        if (executionMetadata && coreutils_1.JSONExt.isObject(executionMetadata)) {
            let executionTimeNode = cell.node.querySelector(`.${EXECUTE_TIME_CLASS}`);
            const parentNode = this._settings.positioning === 'hover'
                ? cell.inputArea.node.parentNode
                : cell.inputArea.editorWidget.node;
            if (!executionTimeNode) {
                executionTimeNode = document.createElement('div');
                executionTimeNode.appendChild(document.createElement('span'));
                // Use this over gap as hover is not a flexbox
                const spacer = document.createElement('div');
                spacer.style.minWidth = '12px';
                executionTimeNode.appendChild(spacer);
                executionTimeNode.appendChild(document.createElement('span'));
                if (!cell.inputHidden) {
                    parentNode.append(executionTimeNode);
                }
            }
            else if (executionTimeNode.parentNode !== parentNode) {
                executionTimeNode.remove();
                parentNode.append(executionTimeNode);
            }
            // Ensure that the current cell onclick actives the current cell
            executionTimeNode.onclick = () => {
                // This check makes sure that range selections (mostly) work
                // activate breaks the range selection otherwise
                if (this._tracker.activeCell !== cell) {
                    cell.activate();
                }
            };
            let positioning;
            switch (this._settings.positioning) {
                case 'left':
                    positioning = 'left';
                    break;
                case 'right':
                    positioning = 'right';
                    break;
                case 'hover':
                    positioning = 'hover';
                    break;
                default:
                    console.error(`'${positioning}' is not a valid type for the setting 'positioning'`);
            }
            const positioningClass = `${EXECUTE_TIME_CLASS}-positioning-${this._settings.positioning}`;
            const textContrastClass = `${EXECUTE_TIME_CLASS}-contrast-${this._settings.textContrast}`;
            executionTimeNode.className = `${EXECUTE_TIME_CLASS} ${positioningClass} ${textContrastClass}`;
            // More info about timing: https://jupyter-client.readthedocs.io/en/stable/messaging.html#messages-on-the-shell-router-dealer-channel
            // A cell is queued when the kernel has received the message
            // A cell is running when the kernel has started executing
            // A cell is done when the execute_reply has has finished
            const queuedTimeStr = executionMetadata['iopub.status.busy'];
            const queuedTime = queuedTimeStr ? new Date(queuedTimeStr) : null;
            const startTimeStr = (executionMetadata['shell.execute_reply.started'] ||
                executionMetadata['iopub.execute_input']);
            // Using started is more accurate, but we don't get this until after the cell has finished executing
            const startTime = startTimeStr ? new Date(startTimeStr) : null;
            // This is the time the kernel is done processing and starts replying
            const endTimeStr = executionMetadata['shell.execute_reply'];
            const endTime = endTimeStr ? new Date(endTimeStr) : null;
            // shell.execute_reply can be one of:  One of: 'ok' OR 'error' OR 'aborted'
            // We want to remove the cases where it's not 'ok', but that's not in the metadata
            // So we assume that if iopub.execute_input never happened, the cell never ran, thus not ok.
            // This is assumed to be true because per the spec below, the code being executed should be sent to all frontends
            // See: https://jupyter-client.readthedocs.io/en/stable/messaging.html#messages-on-the-shell-router-dealer-channel
            // See: https://jupyter-client.readthedocs.io/en/stable/messaging.html#code-inputs
            const isLikelyAborted = endTimeStr && !executionMetadata['iopub.execute_input'];
            let msg = '';
            if (isLikelyAborted) {
                msg = '';
            }
            else if (endTime) {
                if (this._settings.minTime <=
                    date_fns_1.differenceInMilliseconds(endTime, startTime) / 1000.0) {
                    const executionTime = formatters_1.getTimeDiff(endTime, startTime);
                    const lastExecutionTime = executionTimeNode.getAttribute(PREV_DATA_EXECUTION_TIME_ATTR);
                    // Store the last execution time in the node to be used for various options
                    executionTimeNode.setAttribute(PREV_DATA_EXECUTION_TIME_ATTR, executionTime);
                    // Only add a tooltip for all non-displayed execution times.
                    if (this._settings.historyCount > 0 && lastExecutionTime) {
                        let tooltip = executionTimeNode.getAttribute('title');
                        const executionTimes = [lastExecutionTime];
                        if (tooltip) {
                            executionTimes.push(...tooltip.substring(TOOLTIP_PREFIX.length + 1).split('\n'));
                            // JS does the right thing of having empty items if extended
                            executionTimes.length = this._settings.historyCount;
                        }
                        tooltip = `${TOOLTIP_PREFIX}\n${executionTimes.join('\n')}`;
                        executionTimeNode.setAttribute('title', tooltip);
                    }
                    executionTimeNode.children[2].textContent = '';
                    msg = `Last executed at ${formatters_1.getTimeString(endTime)} in ${executionTime}`;
                }
            }
            else if (startTime) {
                if (this._settings.showLiveExecutionTime) {
                    const lastRunTime = executionTimeNode.getAttribute('data-prev-execution-time');
                    const workingTimer = setInterval(() => {
                        if (!executionTimeNode.children[0].textContent.startsWith('Execution started at')) {
                            clearInterval(workingTimer);
                            return;
                        }
                        if (this._settings.minTime <=
                            date_fns_1.differenceInMilliseconds(new Date(), startTime) / 1000.0) {
                            const executionTime = formatters_1.getTimeDiff(new Date(), startTime);
                            executionTimeNode.children[2].textContent = `${executionTime} ${lastRunTime ? `(${lastRunTime})` : ''}`;
                        }
                    }, 100);
                }
                msg = `Execution started at ${formatters_1.getTimeString(startTime)}`;
            }
            else if (queuedTime) {
                const lastRunTime = executionTimeNode.getAttribute('data-prev-execution-time');
                if (this._settings.showLiveExecutionTime && lastRunTime) {
                    executionTimeNode.children[2].textContent = `N/A (${lastRunTime})`;
                }
                msg = `Execution queued at ${formatters_1.getTimeString(queuedTime)}`;
            }
            if (executionTimeNode.textContent !== msg) {
                executionTimeNode.children[0].textContent = msg;
                if (!disableHighlight && this._settings.highlight && endTimeStr) {
                    executionTimeNode.style.setProperty('animation', ANIMATE_CSS);
                    setTimeout(() => executionTimeNode.style.removeProperty('animation'), ANIMATE_TIME_MS);
                }
            }
        }
        else {
            // Hide it if data was removed (e.g. clear output).
            // Don't remove as element store history, which are useful for later showing past runtime.
            const executionTimeNode = cell.node.querySelector(`.${EXECUTE_TIME_CLASS}`);
            if (executionTimeNode) {
                executionTimeNode.classList.add('execute-time-hidden');
            }
        }
    }
    _updateSettings(settings) {
        this._settings.enabled = settings.get('enabled').composite;
        this._settings.highlight = settings.get('highlight').composite;
        this._settings.positioning = settings.get('positioning')
            .composite;
        this._settings.minTime = settings.get('minTime').composite;
        this._settings.textContrast = settings.get('textContrast')
            .composite;
        this._settings.showLiveExecutionTime = settings.get('showLiveExecutionTime')
            .composite;
        this._settings.historyCount = settings.get('historyCount')
            .composite;
        const cells = this._panel.context.model.cells;
        if (this._settings.enabled) {
            cells.changed.connect(this.updateConnectedCell);
            for (let i = 0; i < cells.length; ++i) {
                this._registerMetadataChanges(cells.get(i));
            }
        }
        else {
            cells.changed.disconnect(this.updateConnectedCell);
            for (let i = 0; i < cells.length; ++i) {
                this._deregisterMetadataChanges(cells.get(i));
            }
        }
    }
}
exports["default"] = ExecuteTimeWidget;


/***/ }),

/***/ "./lib/formatters.js":
/*!***************************!*\
  !*** ./lib/formatters.js ***!
  \***************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.getTimeDiff = exports.getTimeString = void 0;
const date_fns_1 = __webpack_require__(/*! date-fns */ "webpack/sharing/consume/default/date-fns/date-fns");
const getTimeString = (date) => {
    return date_fns_1.format(date, 'yyy-MM-dd HH:mm:ss');
};
exports.getTimeString = getTimeString;
const getTimeDiff = (end, start) => {
    // Human format based on loosely on ideas from:
    // https://github.com/ipython-contrib/jupyter_contrib_nbextensions/blob/master/src/jupyter_contrib_nbextensions/nbextensions/execute_time/ExecuteTime.js#L194
    const MS_IN_SEC = 1000;
    const MS_IN_MIN = 60 * MS_IN_SEC;
    const MS_IN_HR = 60 * MS_IN_MIN;
    const MS_IN_DAY = 24 * MS_IN_HR;
    let ms = date_fns_1.differenceInMilliseconds(end, start);
    if (ms < MS_IN_SEC) {
        return `${ms}ms`;
    }
    const days = Math.floor(ms / MS_IN_DAY);
    ms = ms % MS_IN_DAY;
    const hours = Math.floor(ms / MS_IN_HR);
    ms = ms % MS_IN_HR;
    const mins = Math.floor(ms / MS_IN_MIN);
    ms = ms % MS_IN_MIN;
    // We want to show this as fractional
    const secs = ms / MS_IN_SEC;
    let timeDiff = '';
    if (days) {
        timeDiff += `${days}d `;
    }
    if (days || hours) {
        timeDiff += `${hours}h `;
    }
    if (days || hours || mins) {
        timeDiff += `${mins}m `;
    }
    // Only show s if its < 1 day
    if (!days) {
        // Only show ms if is < 1 hr
        timeDiff += `${secs.toFixed(hours ? 0 : 2)}s`;
    }
    return timeDiff.trim();
};
exports.getTimeDiff = getTimeDiff;


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
const notebook_1 = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
const settingregistry_1 = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
const ExecuteTimeWidget_1 = __importStar(__webpack_require__(/*! ./ExecuteTimeWidget */ "./lib/ExecuteTimeWidget.js"));
class ExecuteTimeWidgetExtension {
    constructor(tracker, settingRegistry) {
        this._settingRegistry = settingRegistry;
        this._tracker = tracker;
    }
    // We get a notebook panel because of addWidgetExtension('Notebook', ...) below
    createNew(panel, context) {
        return new ExecuteTimeWidget_1.default(panel, this._tracker, this._settingRegistry);
    }
}
/**
 * Initialization data for the jupyterlab-execute-time extension.
 */
const extension = {
    id: ExecuteTimeWidget_1.PLUGIN_NAME,
    autoStart: true,
    requires: [notebook_1.INotebookTracker, settingregistry_1.ISettingRegistry],
    activate: (app, tracker, settingRegistry) => {
        app.docRegistry.addWidgetExtension('Notebook', new ExecuteTimeWidgetExtension(tracker, settingRegistry));
        // eslint-disable-next-line no-console
        console.log('JupyterLab extension jupyterlab-execute-time is activated!');
    },
};
exports["default"] = extension;


/***/ })

}]);
//# sourceMappingURL=lib_index_js.0eeda6718018a7df4918.js.map