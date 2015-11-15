import React from 'react';
import {render} from 'react-dom';
import {Provider} from 'react-redux';
import Store from 'core/Store';
import Routes from 'core/Routes';

import { DevTools, DebugPanel, LogMonitor } from 'redux-devtools/lib/react';

function runApplication() {
  render(
    <Provider store={Store}>
    {(() => {
      if (__DEV__) {
        return (
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
        );
      } else {
        return Routes;
      }
    })()}
    </Provider>, document.getElementById('application'));
}

runApplication();
