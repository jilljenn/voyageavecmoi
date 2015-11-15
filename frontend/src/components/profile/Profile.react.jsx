import React from 'react';
import Radium from 'radium';

import {Card} from 'belle';

@Radium
export default class Profile extends React.Component {
  static propTypes = {
    children: React.PropTypes.any.isRequired,
    title: React.PropTypes.string.isRequired,
    twitterHandle: React.PropTypes.string.isRequired
  }

  render() {
    const {title, twitterHandle} = this.props;
    return (
      <Card>
        <section style={styles.container}>
          <h1 style={styles.title}>{title} (<a target="_blank" href={`https://twitter.com/${twitterHandle}`}>@{twitterHandle}</a>)</h1>
          {this.props.children}
        </section>
      </Card>
    );
  }
}

const styles = {
  container: {
    display: 'flex'
  },
  title: {
    fontSize: '20px'
  }
}
