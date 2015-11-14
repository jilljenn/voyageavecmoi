import React from 'react';

import Header from 'containers/Header.react';
import Navbar from 'containers/Navbar.react';
import Footer from 'containers/Footer.react';

export default class Application extends React.Component {
  static propTypes = {
    children: React.PropTypes.any.isRequired
  }

	render() {
		return (
			<section>
				<Header />
				<Navbar />
        {this.props.children}
				<Footer />
			</section>
		);
	}
}
