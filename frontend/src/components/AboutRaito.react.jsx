import React from 'react';

import Profile from 'components/profile/Profile.react';
import ProfileImage from 'components/profile/ProfileImage.react';

export default class AboutRaito extends React.Component {
  render() {
    return (
      <Profile title="Raito Bezarius" twitterHandle="Ra1t0_Bezar1us">
        <ProfileImage image='http://gravatar.com/avatar/71120e525a8b177bbe690caf54464425' />
      </Profile>
    );
  }
}
