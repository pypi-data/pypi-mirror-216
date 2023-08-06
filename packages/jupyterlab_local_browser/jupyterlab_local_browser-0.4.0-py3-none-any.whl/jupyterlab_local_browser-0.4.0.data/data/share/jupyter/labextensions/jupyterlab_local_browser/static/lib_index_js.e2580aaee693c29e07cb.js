"use strict";
(self["webpackChunkjupyterlab_local_browser"] = self["webpackChunkjupyterlab_local_browser"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var uuid__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! uuid */ "webpack/sharing/consume/default/uuid/uuid");
/* harmony import */ var uuid__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(uuid__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");






/**
 * Initialization data for the jupyterlab_local_browser extension.
 */
const plugin = {
    id: 'jupyterlab_local_browser:plugin',
    description: 'JupyterLab Local Browser',
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__.ILauncher, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_3__.IStateDB],
    autoStart: true,
    activate: (app, palette, launcher, restorer, statedb) => {
        // Add the command to open the local browser
        const command = 'jupyterlab_local_browser:open';
        app.commands.addCommand(command, {
            label: (args) => (args['isPalette'] ? 'New Local Browser' : 'Local Browser'),
            caption: 'Start a new Local Browser',
            execute: (args) => {
                // Create the widget
                const uuid = args && args.uuid ? args.uuid : 'lb-' + (0,uuid__WEBPACK_IMPORTED_MODULE_4__.v4)();
                const widget = new _widget__WEBPACK_IMPORTED_MODULE_5__.LocalBrowserWidget({ uuid: uuid, statedb: statedb });
                // Track the state of the widget for later restoration
                tracker.add(widget);
                app.shell.add(widget, 'main');
                widget.content.update();
                // Activate the widget
                app.shell.activateById(widget.id);
            }
        });
        // Add the command to the palette.
        palette.addItem({ command, category: 'Local Browser' });
        // Add the command to the launcher.
        launcher.add({
            command,
            category: 'Notebook',
            rank: 1,
        });
        // Track and restore the widget state
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: 'local_browser'
        });
        restorer.restore(tracker, {
            command,
            name: obj => obj.node.id,
            args: obj => {
                return { uuid: obj.node.id };
            }
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   LocalBrowserWidget: () => (/* binding */ LocalBrowserWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_4__);





/**
 * A widget providing a browser for local servers.
 */
class LocalBrowserWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget {
    constructor(options) {
        super({
            content: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IFrame({
                sandbox: ['allow-same-origin', 'allow-scripts']
            }),
        });
        this._loadPortsInterval = -1;
        this.id = options.uuid;
        this.title.label = 'Local Browser';
        this.title.closable = true;
        this.content.addClass('lb-localBrowser');
        this._portsWidget = new SelectWidget({
            onChange: () => {
                this.toolbarChanged();
            },
            value: '_placeholder'
        });
        this.toolbar.addItem('ports', this._portsWidget);
        this._pathWidget = new PathWidget({
            onChange: () => {
                this.toolbarChanged();
            },
            value: ''
        });
        this.toolbar.addItem('path', this._pathWidget);
        const reloadButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.refreshIcon,
            iconLabel: 'Reload',
            onClick: () => {
                this.toolbarChanged();
            }
        });
        this.toolbar.addItem('reload', reloadButton);
        this._statedb = options.statedb;
        this._serverSettings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeSettings();
        this.content.url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__.URLExt.join(this._serverSettings.baseUrl, 'jupyterlab-local-browser', 'public', 'index.html');
        options.statedb.fetch(options.uuid).then((data) => {
            if (data) {
                this._portsWidget.value = data.port;
                this._pathWidget.value =
                    data.pathname.charAt(0) === '/'
                        ? data.pathname.substring(1)
                        : data.pathname;
                const url = '/' +
                    data.mode +
                    '/' +
                    data.port +
                    data.pathname +
                    data.search +
                    data.hash;
                this.content.url = url;
            }
        });
        this.content.node.children[0].addEventListener('load', this);
        this._loadPortsInterval = setInterval(() => {
            this._evtLoadPortsTimer();
        }, 10000);
        this._evtLoadPortsTimer();
    }
    handleEvent(evt) {
        if (evt.type === 'load') {
            this._evtIFrameLoad();
        }
        else {
            console.log(evt);
        }
    }
    toolbarChanged() {
        if (this._portsWidget.value === '_placeholder') {
            this.content.url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__.URLExt.join(this._serverSettings.baseUrl, 'jupyterlab-local-browser', 'public', 'index.html');
        }
        else {
            this.content.url =
                '/proxy/' + this._portsWidget.value + '/' + this._pathWidget.value;
        }
    }
    onCloseRequest(msg) {
        this.content.node.children[0].removeEventListener('load', this);
        clearInterval(this._loadPortsInterval);
        super.onCloseRequest(msg);
    }
    _evtIFrameLoad() {
        const contentDocument = this.content.node.children[0]
            .contentDocument;
        if (contentDocument) {
            this.title.label = contentDocument.title;
            const iFrameLocation = contentDocument.location;
            if (iFrameLocation.pathname.indexOf('/jupyterlab-local-browser/public/index.html') >= 0) {
                this._statedb.remove(this.id);
            }
            else {
                let pathname = iFrameLocation.pathname.substring(1);
                const mode = pathname.substring(0, pathname.indexOf('/'));
                pathname = pathname.substring(pathname.indexOf('/') + 1);
                const port = pathname.substring(0, pathname.indexOf('/'));
                pathname = pathname.substring(pathname.indexOf('/'));
                this._statedb.save(this.id, {
                    mode: mode,
                    port: port,
                    pathname: pathname,
                    search: iFrameLocation.search,
                    hash: iFrameLocation.hash
                });
                this._pathWidget.value =
                    pathname.charAt(0) === '/' ? pathname.substring(1) : pathname;
            }
        }
    }
    _evtLoadPortsTimer() {
        const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__.URLExt.join(this._serverSettings.baseUrl, 'jupyterlab-local-browser', 'open-ports');
        _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeRequest(requestUrl, {}, this._serverSettings).then(response => {
            response.json().then((data) => {
                const baseUrl = new URL(this._serverSettings.baseUrl);
                const basePort = baseUrl.port;
                const values = data
                    .map(([port, label]) => {
                    if (port !== basePort) {
                        return [port, label];
                    }
                    else {
                        return null;
                    }
                })
                    .filter(value => value !== null);
                values.splice(0, 0, ['_placeholder', 'Select a Port']);
                this._portsWidget.values = values;
            });
        });
    }
}
class SelectWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(options) {
        super();
        this._values = [];
        this._value = options.value ? options.value : '';
        this._onChange = options.onChange;
    }
    set values(value) {
        this._values = value;
        this.update();
    }
    get value() {
        return this._value;
    }
    set value(value) {
        this._value = value;
        this.update();
    }
    onChange(evt) {
        this._value = evt.target.value;
        this._onChange();
        this.update();
    }
    render() {
        const values = [];
        for (const [value, label] of this._values) {
            values.push(react__WEBPACK_IMPORTED_MODULE_4___default().createElement("option", { value: value, selected: value === this._value }, label));
        }
        return react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.HTMLSelect, { onChange: evt => this.onChange(evt) }, values);
    }
}
class PathWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(options) {
        super();
        this._onChange = options.onChange;
        this._value = options.value ? options.value : '';
    }
    get value() {
        return this._value;
    }
    set value(value) {
        this._value = value;
        this.update();
    }
    onChange(evt) {
        this._value = evt.target.value;
        this._onChange();
        this.update();
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_4___default().createElement("input", { type: "text", value: this._value, onChange: evt => this.onChange(evt), className: "jp-Default" }));
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.e2580aaee693c29e07cb.js.map