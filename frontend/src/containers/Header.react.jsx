import React from 'react';

import GitHubForkRibbon from 'react-github-fork-ribbon';

export default class Header extends React.Component {
	render() {
		return (
      <header>
        <GitHubForkRibbon
          href="//github.com/jilljenn/voyageavecmoi"
          target="_blank"
          position="right">
          Scissionnez-moi sur GitHub!
        </GitHubForkRibbon>
			</header>
		);
	}
}
