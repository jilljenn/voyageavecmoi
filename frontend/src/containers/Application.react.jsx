import React from 'react';

import Header from 'containers/Header.react';
import Navbar from 'containers/Navbar.react';
import Footer from 'containers/Footer.react';

import Radium from 'radium';

@Radium
export default class Application extends React.Component {
  static propTypes = {
    children: React.PropTypes.any.isRequired
  }

	render() {
		return (
      <section style={styles.main}>
				<Header />
				<Navbar />
        {this.props.children}
				<Footer />
			</section>
		);
	}
}

const styles = {
  main: {
    display: 'flex',
    flexFlow: 'column nowrap'
  }
};
