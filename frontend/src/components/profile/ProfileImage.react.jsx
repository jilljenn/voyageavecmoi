import React from 'react';

import Radium from 'radium';

@Radium
export default class ProfileImage extends React.Component {
  static propTypes = {
    image: React.PropTypes.string.isRequired
  }
  render() {
    return (
      <section style={styles.container}>
        <img
          style={styles.image}
          src={this.props.image}
          alt="Profile image"
        />
      </section>
    );
  }
}

const styles = {
  container: {
    width: '80px',
    height: '80px',
    order: '-1',
    padding: '20px'
  },
  image: {
    borderRadius: '10px'
  }
}
