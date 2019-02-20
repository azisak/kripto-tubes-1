import React, { Component } from 'react';
import NavBar from './NavBar';
import { Grid } from '@material-ui/core';
import Body from '../containers/Body';

class App extends Component {
  render() {
    return (
      <div className="App">
      <Grid container justify="space-around" alignContent="space-around" direction="row">
        <Grid item xs={10}>
          <NavBar/>
          <Body />
        </Grid>
      </Grid>
      </div>
    );
  }
}

export default App;
