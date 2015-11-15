import React from 'react';

import {Link, IndexLink} from 'react-router';

export default class Footer extends React.Component {
	render() {
		return (
      <footer>
        <Link to="about">À propos de nous</Link> <br />
        <IndexLink to="home">Page d'accueil</IndexLink>
			</footer>
		);
	}
}
