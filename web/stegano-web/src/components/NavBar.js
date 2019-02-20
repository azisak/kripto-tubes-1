import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { Grid, AppBar, Toolbar, Typography } from '@material-ui/core';

const styles = {
	root: {
		flexGrow: 1,
	},
	Typography: {
		textAlign: "center",
	},
	menuButton: {
		marginLeft: -12,
		marginRight: 20,
	},
};

class NavBar extends Component {
	render() {
		const { classes } = this.props;
		return (
			<div className={classes.root}>
				<AppBar position="static">
					<Toolbar>
						<Grid container alignItems="center" alignContent="center">
							<Grid item xs={12}>
								<Typography variant="h6" color="inherit" className={classes.Typography}>
										Steganography
								</Typography>

							</Grid>
						</Grid>
					</Toolbar>
				</AppBar>
			</div>
		)
	}
}

NavBar.propTypes = {
	classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(NavBar);
