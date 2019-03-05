import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { VideoLibrary, Audiotrack } from '@material-ui/icons';
import {  BottomNavigation, BottomNavigationAction } from '@material-ui/core';

const styles = {
  root: {
  },
};

class NavigationButtons extends React.Component {
  state = {
    value: 0,
  };

  handleChange = (event, value) => {
    this.setState({ value });
  };

  render() {
    const { classes } = this.props;
    const { value } = this.state;

    return (
      <BottomNavigation
        value={value}
        onChange={this.handleChange}
        showLabels={true}
        className={classes.root}
      >
            <BottomNavigationAction label="WAV" icon={<Audiotrack />} />
            <BottomNavigationAction label="AVI" icon={<VideoLibrary />} />
      </BottomNavigation>
    );
  }
}

NavigationButtons.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(NavigationButtons);