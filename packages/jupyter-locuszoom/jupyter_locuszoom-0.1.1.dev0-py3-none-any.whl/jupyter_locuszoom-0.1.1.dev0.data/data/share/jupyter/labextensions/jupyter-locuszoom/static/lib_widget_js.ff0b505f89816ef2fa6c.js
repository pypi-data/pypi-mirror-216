(self["webpackChunkjupyter_locuszoom"] = self["webpackChunkjupyter_locuszoom"] || []).push([["lib_widget_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".custom-widget {\n  background-color: lightseagreen;\n  padding: 0px 2px;\n}\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ (function(__unused_webpack_module, exports) {

"use strict";

var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.untilReady = void 0;
function sleep(timeout) {
    return __awaiter(this, void 0, void 0, function* () {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve();
            }, timeout);
        });
    });
}
function untilReady(isReady, maxRetrials = 10, interval = 75, intervalModifier = (i) => i) {
    return (() => __awaiter(this, void 0, void 0, function* () {
        let i = 0;
        while (isReady() !== true) {
            i += 1;
            if (maxRetrials !== -1 && i > maxRetrials) {
                throw Error('Too many retrials');
            }
            interval = intervalModifier(interval);
            yield sleep(interval);
        }
        return isReady;
    }))();
}
exports.untilReady = untilReady;


/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Michał Krassowski
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Michał Krassowski
// Distributed under the terms of the Modified BSD License.
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.LocusZoomView = exports.LocusZoomModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const coreutils_1 = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
const locuszoom_1 = __importDefault(__webpack_require__(/*! locuszoom */ "webpack/sharing/consume/default/locuszoom/locuszoom"));
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const utils_1 = __webpack_require__(/*! ./utils */ "./lib/utils.js");
// Import the CSS
__webpack_require__(/*! locuszoom/dist/locuszoom.css */ "./node_modules/locuszoom/dist/locuszoom.css");
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
class LocusZoomModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: LocusZoomModel.model_name, _model_module: LocusZoomModel.model_module, _model_module_version: LocusZoomModel.model_module_version, _view_name: LocusZoomModel.view_name, _view_module: LocusZoomModel.view_module, _view_module_version: LocusZoomModel.view_module_version, build: 'GRCh38', position: {
                chr: '1',
                start: 0,
                end: 5000000,
            }, _associations_view: {
                range: {
                    chr: '1',
                    start: 0,
                    end: 5000000,
                }
            } });
    }
}
exports.LocusZoomModel = LocusZoomModel;
LocusZoomModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
LocusZoomModel.model_name = 'LocusZoomModel';
LocusZoomModel.model_module = version_1.MODULE_NAME;
LocusZoomModel.model_module_version = version_1.MODULE_VERSION;
LocusZoomModel.view_name = 'LocusZoomView'; // Set to null if no view
LocusZoomModel.view_module = version_1.MODULE_NAME; // Set to null if no view
LocusZoomModel.view_module_version = version_1.MODULE_VERSION;
const AssociationLZ = locuszoom_1.default.Adapters.get('AssociationLZ');
class ModelAssociation extends AssociationLZ {
    constructor(config) {
        super({});
        this.model = config.model;
    }
    _performRequest(options) {
        return __awaiter(this, void 0, void 0, function* () {
            // TODO: find a way to fetch view properly
            yield utils_1.untilReady(() => {
                const view = this.model.get('_associations_view');
                const position = view.range;
                console.log(position, options, (position.chr === options.chr &&
                    position.start === options.start &&
                    position.end === options.end));
                return (position.chr === options.chr &&
                    position.start === options.start &&
                    position.end === options.end);
            });
            return this.model.get('_associations_view');
        });
    }
}
// A custom adapter should be added to the registry before using it
locuszoom_1.default.Adapters.add('ModelAssociation', ModelAssociation);
class LocusZoomView extends base_1.DOMWidgetView {
    constructor(options) {
        super(options);
        this.container = document.createElement('div');
        this.container.id = 'locus-zoom-' + coreutils_1.UUID.uuid4();
        this.el.appendChild(this.container);
    }
    _processLuminoMessage(msg, _super) {
        _super.call(this, msg);
        switch (msg.type) {
            case 'resize':
                console.log('resize message');
                window.requestAnimationFrame(() => this.plot.rescaleSVG());
                break;
        }
    }
    processPhosphorMessage(msg) {
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore
        this._processLuminoMessage(msg, super.processPhosphorMessage);
    }
    processLuminoMessage(msg) {
        this._processLuminoMessage(msg, super.processLuminoMessage);
    }
    render() {
        const apiBase = 'https://portaldev.sph.umich.edu/api/v1/';
        const build = this.model.get('build');
        const dataSources = new locuszoom_1.default.DataSources();
        dataSources
            .add('assoc', ['ModelAssociation', { model: this.model }])
            .add('ld', [
            'LDServer',
            {
                url: 'https://portaldev.sph.umich.edu/ld/',
                source: '1000G',
                build,
                population: 'ALL',
            },
        ])
            .add('gene', ['GeneLZ', { url: apiBase + 'annotation/genes/', build }])
            .add('recomb', [
            'RecombLZ',
            { url: apiBase + 'annotation/recomb/results/', build },
        ])
            .add('constraint', [
            'GeneConstraintLZ',
            { url: 'https://gnomad.broadinstitute.org/api/', build },
        ]);
        // TODO:
        //.add("phewas", ["PheWASLZ", {url: "https://portaldev.sph.umich.edu/" + "api/v1/statistic/phewas/", build: [build]}])
        const initialState = this.positionState;
        console.log(initialState);
        const layout = locuszoom_1.default.Layouts.get('plot', 'standard_association', {
            state: initialState,
        });
        // d3 assumes the node is already in the DOM and will fail if we do not attach it temporarily.
        const attached = this.el.parentElement !== null;
        if (!attached) {
            document.body.appendChild(this.el);
        }
        const plot = locuszoom_1.default.populate('#' + this.container.id, dataSources, layout);
        if (!attached) {
            document.body.removeChild(this.el);
        }
        this.plot = plot;
        plot.on('state_changed', () => {
            const position = this.model.get('position');
            if (plot.state.start === position.start &&
                plot.state.end === position.end &&
                plot.state.chr === position.chr) {
                return;
            }
            console.log('plot state changed, will set kernel state to', plot.state);
            this.model.set('position', {
                start: plot.state.start,
                end: plot.state.end,
                chr: plot.state.chr,
            });
            this.model.save_changes();
        });
        const updateState = () => {
            console.log('kernel state changed, will set state to ', this.positionState);
            plot.applyState(Object.assign(Object.assign({}, this.positionState), { ldrefvar: '' }));
        };
        // listen to changes of state in kernel and update view accordingly
        this.model.on('change:position', updateState);
        this.displayed.then(() => {
            this.plot.rescaleSVG();
        });
    }
    get positionState() {
        return this.model.get('position');
    }
}
exports.LocusZoomView = LocusZoomView;


/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"jupyter-locuszoom","version":"0.1.0","description":"Jupyter Widget for LocusZoom","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/krassowski/jupyter-locuszoom","bugs":{"url":"https://github.com/krassowski/jupyter-locuszoom/issues"},"license":"BSD-3-Clause","author":{"name":"Michał Krassowski","email":"me@me.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/krassowski/jupyter-locuszoom"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf jupyter_locuszoom/labextension","clean:nbextension":"rimraf jupyter_locuszoom/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2 || ^3 || ^4 || ^5 || ^6","locuszoom":"^0.14.0"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyter-widgets/base-manager":"^1.0.2","@jupyterlab/builder":"^3.0.0","@lumino/application":"^1.6.0","@lumino/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"jupyter_locuszoom/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.ff0b505f89816ef2fa6c.js.map