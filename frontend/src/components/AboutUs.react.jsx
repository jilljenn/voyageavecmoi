import React from 'react';

import AboutRaito from 'components/AboutRaito.react';
// import AboutProgVal from 'components/AboutProgVal.react';

import Radium from 'radium';

@Radium
export default class AboutUs extends React.Component {
  render() {
    return (
      <section style={styles.container}>
        <h1 style={styles.title}>Qui sommes-nous?</h1>
        <section style={styles.grid}>
          <AboutRaito />
          {/* <AboutProgVal /> */}
        </section>
      </section>
    );
  }
}

const styles = {
  container: {
    display: 'flex',
    flexFlow: 'column wrap',
    margin: 'auto'
  },
  title: {
    margin: 'auto'
  },
  grid: {
    margin: 'auto',
    display: 'flex'
  }
}
