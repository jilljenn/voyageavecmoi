import React from 'react';
import {render} from 'react-dom';
import {Provider} from 'react-redux';
import Store from 'core/Store';
import Routes from 'core/Routes';

import { DevTools, DebugPanel, LogMonitor } from 'redux-devtools/lib/react';

function runApplication() {
  render(
    <Provider store={Store}>
      <section>
        {Routes}
        <DebugPanel
          top
          right
          bottom
        >
          <DevTools
            store={Store}
            monitor={LogMonitor}
          />
        </DebugPanel>
      </section>
    </Provider>, document.getElementById('application'));
}

runApplication();
