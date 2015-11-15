import React from 'react';
import {Router, Route, IndexRoute} from 'react-router';

import Application from 'containers/Application.react';
import Home from 'containers/Home.react';
import AboutUs from 'components/AboutUs.react';

export default (
  <Router>
    <Route path="/"
      component={Application}>
      <IndexRoute component={Home} />
      <Route component={Home}
        path="home" />
      <Route component={AboutUs}
        path="about" />
    </Route>
  </Router>
);
