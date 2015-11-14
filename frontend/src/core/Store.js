import {createStore, compose, applyMiddleware} from 'redux';
import {devTools, persistState} from 'redux-devtools';
import thunkMiddleware from 'redux-thunk';
import createLogger from 'redux-logger';
import travelApp from 'reducers/Reducers.js';

const logger = createLogger();

const enhancedCreateStore = compose(
  applyMiddleware(
    logger,
    thunkMiddleware),
  devTools(),
  persistState(window.location.href.match(/[?&]debug_session=([^&]+)\b/))
)(createStore);

export default enhancedCreateStore(travelApp);
