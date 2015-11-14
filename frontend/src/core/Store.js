import {createStore, compose, applyMiddleware} from 'redux';
import {devTools, persistState} from 'redux-devtools';
import thunkMiddleware from 'redux-thunk';
import travelApp from 'reducers/Reducers.js';

const enhancedCreateStore = compose(
  applyMiddleware(
    thunkMiddleware),
  devTools(),
  persistState(window.location.href.match(/[?&]debug_session=([^&]+)\b/))
)(createStore);

export default enhancedCreateStore(travelApp);
