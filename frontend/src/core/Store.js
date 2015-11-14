import {createStore, applyMiddleware} from 'redux';
import thunkMiddleware from 'redux-thunk';
import travelApp from 'reducers/Reducers.js';

const createStoreWithMiddleware = applyMiddleware(
  thunkMiddleware
)(createStore);

export default createStoreWithMiddleware(travelApp);
