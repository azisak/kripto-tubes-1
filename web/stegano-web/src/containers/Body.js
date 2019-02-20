import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { Grid, Button, Paper, TextField, Checkbox, FormGroup, FormControlLabel } from '@material-ui/core';
import NavigationButtons from '../components/NavigationButtons';
import ReactAudioPlayer from 'react-audio-player';
import axios from 'axios';


const HOST_ADDRESS = "http://localhost:5000";
const ENCRYPT_ADDRESS = HOST_ADDRESS + "/encrypt";
const DECRYPT_ADDRESS = HOST_ADDRESS + "/decrypt";

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
	bordered: {
		border: "1px solid black"
	},
	Paper: {
		paddingBottom: "20px"
	}
};

class Body extends Component {
	constructor(props) {
		super(props);
		this.state = {
			stegoKey: "",
			randomSequence: false,
			messageEncryption: false,
			containerFileName: "",
			messageFileName: "",
			messageSrc: null,
			containerFileUpload: null,
			messageFileUpload: null,
			audioSrc: null
		}
	}

	async handleEncrypt() {
		console.log(`Encrypting.. Key:${this.state.stegoKey}; ContainerFile: ${this.state.containerFileUpload}; MessageFile: ${this.state.messageFileUpload};Encryption:${this.state.messageEncryption}; RandomSequence:${this.state.randomSequence}  `)
		if (this.state.containerFileUpload && this.state.messageFileUpload) {
			this.setState({ audioSrc: null });
			const { stegoKey, randomSequence, messageEncryption, containerFileUpload, messageFileUpload, containerFileName, messageFileName } = this.state;
			// axios.get(ENCRYPT_ADDRESS);
			var formData = new FormData();
			formData.append('stegoKey', stegoKey);
			formData.append('randomSequence', randomSequence);
			formData.append('messageEncryption', messageEncryption);
			formData.append('containerFile', containerFileUpload, containerFileName);
			formData.append('messageFile', messageFileUpload, messageFileName);
			await axios.post(ENCRYPT_ADDRESS,
				formData,
				{
					headers: {
						'Content-Type': 'multipart/form-data'
					}
				}
			).then(resp => {
				console.log("Status: ", resp.status);
				console.log("Response: ", resp.data)
				this.setState({ audioSrc: resp.data });
				// this.render();
				console.log("Data set: ", this.state.audioSrc);
			});
			console.log(`Encrypting.. Key:${this.state.stegoKey}; ContainerFile: ${this.state.containerFileUpload}; MessageFile: ${this.state.messageFileUpload};Encryption:${this.state.messageEncryption}; RandomSequence:${this.state.randomSequence}  `)
			console.log(`Encrypting.. Key:${this.state.stegoKey}; ContainerFile: ${this.state.containerFileUpload}; MessageFile: ${this.state.messageFileUpload};Encryption:${this.state.messageEncryption}; RandomSequence:${this.state.randomSequence}  `)
		}
	}

	renderPlayer() {
		if (this.state.audioSrc) {
			console.log("Src: ", this.state.audioSrc);
			return <ReactAudioPlayer
				src={this.state.audioSrc}
				controls
			/>
		}
	}
	renderDownloadMessage() {
		if (this.state.messageSrc) {
			return <div>
				<a href="https://www.w3schools.com/images/myw3schoolsimage.jpg" download>
					<Button>Download</Button>
				</a>
			</div>
		}
	}

	async handleDecrypt() {
		console.log(`Decrypting Key:${this.state.stegoKey}; ContainerFile: ${this.state.containerFileUpload};   `)
		if (this.state.containerFileUpload) {
			this.setState({ messageSrc: null });
			const { stegoKey, containerFileUpload, containerFileName } = this.state;
			var formData = new FormData();
			formData.append('stegoKey', stegoKey);
			formData.append('containerFile', containerFileUpload, containerFileName);
			await axios.post(DECRYPT_ADDRESS,
				formData,
				{
					headers: {
						'Content-Type': 'multipart/form-data'
					}
				}
			).then(resp => {
				console.log("Status: ", resp.status);
				console.log("Response: ", resp.data)
				this.setState({ messageSrc: resp.data });
			});
		}

	}

	render() {
		const { classes } = this.props;
		return (
			<div className={classes.root}>
				<Paper className={classes.Paper}>
					<Grid container alignContent="space-around" justify="space-around" direction="row" >
						<Grid item xs={12} className={classes.bordered}>
							<NavigationButtons />
						</Grid>
						<Grid item xs={12}>
							<Grid container alignItems="center" direction="column" spacing={16}>
								<Grid item xs={12}>
									<TextField
										id="outlined-name"
										label="Stego Key"
										className={classes.textField}
										value={this.state.stegoKey}
										onChange={(evt) => this.setState({ stegoKey: evt.target.value })}
										margin="normal"
										variant="outlined"
									/>
								</Grid>
								<Grid item xs={12}>
									<p>Container File:</p>
									<input type="file" onChange={(e) => {
										if (e.target.files[0]) {

											this.setState({ containerFileUpload: e.target.files[0], containerFileName: e.target.files[0].name })
										}
									}
									}
									/>
								</Grid>
								<Grid item xs={12}>
									<p>Message File:</p>
									<input type="file" onChange={(e) => {
										if (e.target.files[0]) {
											this.setState({ messageFileUpload: e.target.files[0], messageFileName: e.target.files[0].name })
										}

									}
									} />
								</Grid>
								<Grid item xs={12}>
									Options:
									<FormGroup>
										<FormControlLabel
											control={
												<Checkbox
													checked={this.state.messageEncryption}
													onChange={() => this.setState(prevState => ({ messageEncryption: !prevState.messageEncryption }))}
													color="primary"
												/>
											}
											label="Message Encryption"
										/>
										<FormControlLabel
											control={
												<Checkbox
													checked={this.state.randomSequence}
													onChange={() => this.setState(prevState => ({ randomSequence: !prevState.randomSequence }))}
													color="primary"
												/>
											}
											label="Random Sequence"
										/>
									</FormGroup>
								</Grid>
								<Grid item xs={12}>
									<Grid container spacing={16}>
										<Grid item>
											<Button onClick={() => this.handleEncrypt()} variant="outlined" color="primary" className={classes.button}>
												Encrypt
      						</Button>
										</Grid>
										<Grid item>
											<Button onClick={() => this.handleDecrypt()} variant="outlined" color="secondary" className={classes.button}>
												Decrypt
									</Button>
										</Grid>
									</Grid>
									<Grid item xs={12}>
										{this.renderPlayer()}
									</Grid>
									<Grid item xs={12}>
										{this.renderDownloadMessage()}
									</Grid>
								</Grid>
							</Grid>
						</Grid>
					</Grid>
				</Paper>
			</div>
		)
	}
}

Body.propTypes = {
	classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Body);
