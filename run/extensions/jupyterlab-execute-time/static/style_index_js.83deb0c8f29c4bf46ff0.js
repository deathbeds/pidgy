"use strict";
(self["webpackChunkjupyterlab_execute_time"] = self["webpackChunkjupyterlab_execute_time"] || []).push([["style_index_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, "/* Transition to highlight a cell change */\n@keyframes executeHighlight {\n  from {\n    background-color: var(--md-blue-100, #9fccff);\n  }\n  to {\n    background-color: var(--jp-cell-editor-background);\n  }\n}\n\n.execute-time {\n  background-color: var(--jp-cell-editor-background);\n  display: flex;\n  justify-content: space-between;\n  margin-top: 2px;\n  font-family: var(--jp-code-font-family, monospace);\n  font-size: 80%;\n  border-top: 1px solid var(--jp-cell-editor-border-color, #cfcfcf);\n  padding: 0 2px;\n}\n\n.execute-time.execute-time-contrast-low {\n  color: var(--jp-ui-font-color3);\n}\n\n.execute-time.execute-time-contrast-high {\n  color: var(--jp-ui-font-color1);\n}\n\n.execute-time.execute-time-positioning-left {\n  flex-direction: row;\n}\n\n.execute-time.execute-time-positioning-right {\n  flex-direction: row-reverse;\n}\n\n.execute-time.execute-time-positioning-hover {\n  display: none;\n}\n\n.jp-Cell-inputWrapper:hover .execute-time.execute-time-positioning-hover {\n  display: block;\n  position: absolute;\n  right: 0;\n  bottom: -1.25em;\n  border: 1px solid var(--jp-cell-editor-border-color, #cfcfcf);\n  border-width: 0 1px 1px 1px;\n  height: 1.25em;\n  z-index: 3;\n}\n\n.execute-time.execute-time-hidden {\n  display: none;\n}\n", "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"AAAA,0CAA0C;AAC1C;EACE;IACE,6CAA6C;EAC/C;EACA;IACE,kDAAkD;EACpD;AACF;;AAEA;EACE,kDAAkD;EAClD,aAAa;EACb,8BAA8B;EAC9B,eAAe;EACf,kDAAkD;EAClD,cAAc;EACd,iEAAiE;EACjE,cAAc;AAChB;;AAEA;EACE,+BAA+B;AACjC;;AAEA;EACE,+BAA+B;AACjC;;AAEA;EACE,mBAAmB;AACrB;;AAEA;EACE,2BAA2B;AAC7B;;AAEA;EACE,aAAa;AACf;;AAEA;EACE,cAAc;EACd,kBAAkB;EAClB,QAAQ;EACR,eAAe;EACf,6DAA6D;EAC7D,2BAA2B;EAC3B,cAAc;EACd,UAAU;AACZ;;AAEA;EACE,aAAa;AACf","sourcesContent":["/* Transition to highlight a cell change */\n@keyframes executeHighlight {\n  from {\n    background-color: var(--md-blue-100, #9fccff);\n  }\n  to {\n    background-color: var(--jp-cell-editor-background);\n  }\n}\n\n.execute-time {\n  background-color: var(--jp-cell-editor-background);\n  display: flex;\n  justify-content: space-between;\n  margin-top: 2px;\n  font-family: var(--jp-code-font-family, monospace);\n  font-size: 80%;\n  border-top: 1px solid var(--jp-cell-editor-border-color, #cfcfcf);\n  padding: 0 2px;\n}\n\n.execute-time.execute-time-contrast-low {\n  color: var(--jp-ui-font-color3);\n}\n\n.execute-time.execute-time-contrast-high {\n  color: var(--jp-ui-font-color1);\n}\n\n.execute-time.execute-time-positioning-left {\n  flex-direction: row;\n}\n\n.execute-time.execute-time-positioning-right {\n  flex-direction: row-reverse;\n}\n\n.execute-time.execute-time-positioning-hover {\n  display: none;\n}\n\n.jp-Cell-inputWrapper:hover .execute-time.execute-time-positioning-hover {\n  display: block;\n  position: absolute;\n  right: 0;\n  bottom: -1.25em;\n  border: 1px solid var(--jp-cell-editor-border-color, #cfcfcf);\n  border-width: 0 1px 1px 1px;\n  height: 1.25em;\n  z-index: 3;\n}\n\n.execute-time.execute-time-hidden {\n  display: none;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/base.css":
/*!************************!*\
  !*** ./style/base.css ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "./style/index.js":
/*!************************!*\
  !*** ./style/index.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base.css */ "./style/base.css");



/***/ })

}]);
//# sourceMappingURL=style_index_js.83deb0c8f29c4bf46ff0.js.map