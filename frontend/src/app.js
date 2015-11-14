import {render} from 'react-dom';
import Routes from 'core/Routes';

function runApplication() {
  render(Routes, document.getElementById('application'));
}

runApplication();
