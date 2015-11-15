import React from 'react';
import {Router, Route, IndexRoute} from 'react-router';

import Application from 'containers/Application.react';
import Home from 'containers/Home.react';
import AboutUs from 'components/AboutUs.react';

import createBrowserHistory from 'history/lib/createBrowserHistory';

const routes = (
  <Route path="/"
    component={Application}>
    <IndexRoute component={Home} />
    <Route component={Home}
      path="home" />
    <Route component={AboutUs}
      path="about" />
  </Route>
);

let router = null;
if (__DEV__) {
  router = (
    <Router>
      {routes}
    </Router>
  );
} else {
  router = (
    <Router history={createBrowserHistory()}>
      {routes}
    </Router>
  );
}


export default router;
