import React from 'react';
import {Router, Route, IndexRoute} from 'react-router';

import Application from 'containers/Application.react';
import Home from 'containers/Home.react';

import createHashHistory from 'history/lib/createBrowserHistory'

export default (
  <Router history={createHashHistory()}>
    <Route path="/"
      component={Application}>
      <IndexRoute component={Home} />
      <Route component={Home}
        path="home" />
    </Route>
  </Router>
);
